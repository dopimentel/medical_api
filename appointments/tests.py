"""
Testes unitários para a aplicação appointments.
"""
import pytest
from datetime import datetime, timedelta, timezone
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from appointments.models import Appointment
from tests.factories import AppointmentFactory, ProfessionalFactory

User = get_user_model()


@pytest.mark.django_db
class AppointmentAPITestCase(APITestCase):
    """Testes para a API de consultas."""

    def setUp(self):
        """Configuração inicial para os testes."""
        self.url_list = reverse("appointment-list")
        self.professional = ProfessionalFactory()

    @pytest.mark.api
    def test_listar_consultas(self):
        """Testa a listagem de consultas."""
        AppointmentFactory.create_batch(3)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    @pytest.mark.api
    def test_criar_consulta_valida(self):
        """Testa a criação de uma consulta válida."""
        dados_consulta = {
            "professional": self.professional.id,
            "date": "2025-06-15T10:30:00Z"
        }

        response = self.client.post(self.url_list, dados_consulta)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 1)
        self.assertIn("professional_data", response.data)

    @pytest.mark.api
    def test_criar_consulta_campos_obrigatorios(self):
        """Testa a criação de consulta sem campos obrigatórios."""
        dados_incompletos = {"professional": self.professional.id}

        response = self.client.post(self.url_list, dados_incompletos)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("date", response.data)

    @pytest.mark.api
    def test_recuperar_consulta_especifica(self):
        """Testa a recuperação de uma consulta específica."""
        appointment = AppointmentFactory()
        url_detail = reverse(
            "appointment-detail",
            kwargs={"pk": appointment.pk}
        )

        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], appointment.id)
        self.assertIn("professional_data", response.data)

    @pytest.mark.api
    def test_filtrar_consultas_por_profissional(self):
        """Testa a filtragem de consultas por profissional."""
        prof1 = ProfessionalFactory()
        prof2 = ProfessionalFactory()

        AppointmentFactory(professional=prof1)
        AppointmentFactory(professional=prof2)

        response = self.client.get(
            self.url_list,
            {"professional": prof1.id}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        
        appointment_data = response.data[0]
        self.assertEqual(appointment_data["professional"], prof1.id)

    @pytest.mark.api
    def test_filtrar_consultas_por_data(self):
        """Testa a filtragem de consultas por data específica."""
        data_especifica = datetime(
            year=2025, month=12, day=25,
            hour=10, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        appointment = AppointmentFactory(date=data_especifica)
        AppointmentFactory(
            date=data_especifica + timedelta(days=1)
        )

        response = self.client.get(
            self.url_list,
            {"date": data_especifica.date().isoformat()}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], appointment.id)

    @pytest.mark.api
    def test_filtrar_consultas_por_periodo(self):
        """Testa a filtragem de consultas por período."""
        base_date = datetime(
            year=2025, month=6, day=15,
            hour=10, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        # Dentro do período
        AppointmentFactory(date=base_date)
        AppointmentFactory(date=base_date + timedelta(days=1))

        # Fora do período
        AppointmentFactory(date=base_date - timedelta(days=5))
        AppointmentFactory(date=base_date + timedelta(days=10))

        start_date = (base_date - timedelta(days=1)).date().isoformat()
        end_date = (base_date + timedelta(days=5)).date().isoformat()

        response = self.client.get(
            self.url_list,
            {"start_date": start_date, "end_date": end_date}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    @pytest.mark.api
    def test_ordenacao_consultas(self):
        """Testa a ordenação das consultas por data (mais recente primeiro)."""
        data_antiga = datetime(
            year=2025, month=5, day=10,
            hour=9, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )
        data_recente = datetime(
            year=2025, month=6, day=15,
            hour=14, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        appointment_antigo = AppointmentFactory(date=data_antiga)
        appointment_recente = AppointmentFactory(date=data_recente)

        response = self.client.get(self.url_list)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        consultas = response.data
        self.assertEqual(consultas[0]["id"], appointment_recente.id)
        self.assertEqual(consultas[1]["id"], appointment_antigo.id)

    @pytest.mark.api
    def test_atualizar_consulta(self):
        """Testa a atualização de uma consulta existente."""
        appointment = AppointmentFactory()
        url_detail = reverse(
            "appointment-detail",
            kwargs={"pk": appointment.pk}
        )

        nova_data = "2025-07-15T14:30:00Z"
        novos_dados = {
            "professional": appointment.professional.id,
            "date": nova_data
        }

        response = self.client.put(url_detail, novos_dados)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        appointment.refresh_from_db()
        self.assertEqual(
            appointment.date.isoformat(),
            nova_data.replace('Z', '+00:00')
        )

    @pytest.mark.api
    def test_deletar_consulta(self):
        """Testa a exclusão de uma consulta."""
        appointment = AppointmentFactory()
        url_detail = reverse(
            "appointment-detail",
            kwargs={"pk": appointment.pk}
        )

        response = self.client.delete(url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(
            Appointment.objects.filter(id=appointment.id).exists()
        )

    @pytest.mark.api
    def test_validacao_consulta_duplicada(self):
        """Testa se a validação impede consultas duplicadas."""
        professional = ProfessionalFactory()
        data_consulta = datetime(
            year=2025, month=7, day=20,
            hour=15, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        # Primeira consulta
        AppointmentFactory(professional=professional, date=data_consulta)

        # Tentativa de criar segunda consulta no mesmo horário
        dados_duplicados = {
            "professional": professional.id,
            "date": data_consulta.isoformat()
        }

        response = self.client.post(self.url_list, dados_duplicados)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @pytest.mark.api
    def test_dados_profissional_no_serializer(self):
        """Testa se os dados do profissional estão incluídos na resposta."""
        appointment = AppointmentFactory()
        url_detail = reverse(
            "appointment-detail",
            kwargs={"pk": appointment.pk}
        )

        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        professional_data = response.data["professional_data"]
        self.assertEqual(professional_data["id"], appointment.professional.id)
        self.assertEqual(
            professional_data["preferred_name"],
            appointment.professional.preferred_name
        )
        self.assertEqual(
            professional_data["profession"],
            appointment.professional.profession
        )

    @pytest.mark.api
    def test_atualizar_mesma_data_sem_erro(self):
        """
        Testa que é possível atualizar uma consulta mantendo a mesma data.
        """
        appointment = AppointmentFactory()
        url_detail = reverse(
            "appointment-detail",
            kwargs={"pk": appointment.pk}
        )

        dados_atualizacao = {
            "professional": appointment.professional.id,
            "date": appointment.date.isoformat()
        }

        response = self.client.put(url_detail, dados_atualizacao)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


@pytest.mark.django_db
class AppointmentModelTestCase(APITestCase):
    """Testes para o modelo Appointment."""

    @pytest.mark.unit
    def test_str_representation(self):
        """Testa a representação string do modelo."""
        professional = ProfessionalFactory(preferred_name="Dr. João")
        data_consulta = datetime(
            year=2025, month=6, day=15,
            hour=14, minute=30, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        appointment = AppointmentFactory(
            professional=professional,
            date=data_consulta
        )

        expected_str = "Consulta com Dr. João em 15/06/2025 14:30"
        self.assertEqual(str(appointment), expected_str)

    @pytest.mark.unit
    def test_meta_ordering(self):
        """Testa a ordenação padrão do modelo."""
        data1 = datetime(
            year=2025, month=5, day=10,
            hour=9, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )
        data2 = datetime(
            year=2025, month=6, day=15,
            hour=14, minute=0, second=0,
            microsecond=0, tzinfo=timezone.utc
        )

        appointment1 = AppointmentFactory(date=data1)
        appointment2 = AppointmentFactory(date=data2)

        appointments = list(Appointment.objects.all())
        # Mais recente primeiro
        self.assertEqual(appointments[0], appointment2)
        self.assertEqual(appointments[1], appointment1)


@pytest.mark.django_db
class AppointmentIntegrationTestCase(APITestCase):
    """Testes de integração para appointments."""

    @pytest.mark.integration
    def test_relacionamento_professional_appointments(self):
        """Testa o relacionamento entre Professional e suas consultas."""
        professional = ProfessionalFactory()

        appointment1 = AppointmentFactory(professional=professional)
        appointment2 = AppointmentFactory(professional=professional)

        appointments = professional.appointments.all()
        self.assertEqual(appointments.count(), 2)
        self.assertIn(appointment1, appointments)
        self.assertIn(appointment2, appointments)

    @pytest.mark.integration
    def test_deletar_profissional_com_consultas(self):
        """
        Testa que ao deletar um profissional, suas consultas também são
        deletadas.
        """
        professional = ProfessionalFactory()
        AppointmentFactory(professional=professional)
        AppointmentFactory(professional=professional)

        initial_count = Appointment.objects.count()
        self.assertEqual(initial_count, 2)

        professional.delete()

        final_count = Appointment.objects.count()
        self.assertEqual(final_count, 0)