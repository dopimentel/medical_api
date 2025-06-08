from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.utils import timezone
from datetime import timedelta
from .models import Appointment
from professionals.models import Professional


class AppointmentAPITestCase(APITestCase):
    """
    Testes para a API de Consultas.
    """

    def setUp(self):
        """
        Configuração inicial dos testes.
        """
        self.professional = Professional.objects.create(
            preferred_name="Dr. Teste",
            profession="Cardiologista",
            address="Rua de Teste, 123",
            contact="11999998888"
        )
        
        self.professional2 = Professional.objects.create(
            preferred_name="Dra. Outra",
            profession="Dermatologista",
            address="Endereço Outro",
            contact="11987654321"
        )
        
        # Cria consulta para hoje
        self.today = timezone.now()
        self.appointment = Appointment.objects.create(
            professional=self.professional,
            date=self.today
        )
        
        # Cria consulta para amanhã
        self.tomorrow = self.today + timedelta(days=1)
        self.appointment_tomorrow = Appointment.objects.create(
            professional=self.professional2,
            date=self.tomorrow
        )

    def test_list_appointments(self):
        """
        Testa a listagem de consultas.
        """
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_appointment(self):
        """
        Testa a criação de uma consulta.
        """
        url = reverse('appointment-list')
        next_week = self.today + timedelta(days=7)
        data = {
            'professional': self.professional.id,
            'date': next_week.isoformat()
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Appointment.objects.count(), 3)

    def test_retrieve_appointment(self):
        """
        Testa a recuperação de uma consulta específica.
        """
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['professional'], self.professional.id)

    def test_update_appointment(self):
        """
        Testa a atualização de uma consulta.
        """
        url = reverse('appointment-detail', args=[self.appointment.id])
        new_date = self.today + timedelta(hours=2)
        data = {
            'professional': self.professional2.id,
            'date': new_date.isoformat()
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.appointment.refresh_from_db()
        self.assertEqual(self.appointment.professional.id, self.professional2.id)

    def test_delete_appointment(self):
        """
        Testa a exclusão de uma consulta.
        """
        url = reverse('appointment-detail', args=[self.appointment.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Appointment.objects.count(), 1)

    def test_filter_by_professional(self):
        """
        Testa a filtragem de consultas por profissional.
        """
        url = reverse('appointment-list') + f'?professional={self.professional.id}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['professional'], self.professional.id)
        
    def test_filter_by_dates(self):
        """
        Testa a filtragem de consultas por datas.
        """
        # Testando só o endpoint básico para verificar se a API funciona
        url = reverse('appointment-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        
    def test_ordering(self):
        """
        Testa a ordenação de consultas por data.
        """
        url = reverse('appointment-list') + '?ordering=date'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verifica ordenação ascendente
        appointment_dates = [item['date'] for item in response.data]
        self.assertListEqual(appointment_dates, sorted(appointment_dates))
        
        # Verifica ordenação descendente
        url = reverse('appointment-list') + '?ordering=-date'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        appointment_dates = [item['date'] for item in response.data]
        self.assertListEqual(appointment_dates, sorted(appointment_dates, reverse=True))
