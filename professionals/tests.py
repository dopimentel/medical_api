"""
Testes unitários para a aplicação professionals.
"""
import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from professionals.models import Professional
from tests.factories import ProfessionalFactory, UserFactory

User = get_user_model()


@pytest.mark.api
class ProfessionalAPITestCase(APITestCase):
    """Testes para a API de profissionais."""

    def setUp(self):
        """Configuração inicial para cada teste."""
        self.user = UserFactory()
        self.professional_data = {
            "preferred_name": "Dr. João Silva",
            "profession": "Cardiologista",
            "address": "Rua das Flores, 123, São Paulo - SP",
            "contact": "11987654321"
        }
        self.url_list = reverse("professional-list")

    def test_criar_profissional_valido(self):
        """Testa a criação de um profissional com dados válidos."""
        response = self.client.post(self.url_list, self.professional_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 1)

        professional = Professional.objects.first()
        self.assertEqual(professional.preferred_name, "Dr. João Silva")
        self.assertEqual(professional.profession, "Cardiologista")
        self.assertEqual(professional.contact, "11987654321")

    def test_criar_profissional_contato_invalido(self):
        """Testa a validação do campo contato com formato inválido."""
        dados_invalidos = [
            {"contact": "123456789"},  # Menos de 11 dígitos
            {"contact": "123456789012"},  # Mais de 11 dígitos
            {"contact": "11999999abc"},  # Caracteres não numéricos
            {"contact": "+5511999999999"},  # Com caracteres especiais
            {"contact": ""},  # Vazio
        ]

        for dados in dados_invalidos:
            with self.subTest(contact=dados["contact"]):
                data = self.professional_data.copy()
                data.update(dados)

                response = self.client.post(self.url_list, data)
                self.assertEqual(
                    response.status_code,
                    status.HTTP_400_BAD_REQUEST
                )
                self.assertIn("contact", response.data)

    def test_listar_profissionais(self):
        """Testa a listagem de profissionais."""
        # Cria alguns profissionais usando factory
        ProfessionalFactory.create_batch(3)

        response = self.client.get(self.url_list)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_buscar_profissional_por_nome(self):
        """Testa a busca de profissionais por nome."""
        prof1 = ProfessionalFactory(
            preferred_name="Dr. Ana Cardiologista",
            profession="Cardiologia",
            address="Rua das Flores, 123",
            contact="11999999001"
        )
        ProfessionalFactory(
            preferred_name="Dr. João Neurologista",
            profession="Neurologia",
            address="Av. Brasil, 456",
            contact="11999999002"
        )
        ProfessionalFactory(
            preferred_name="Dra. Maria Dermatologista",
            profession="Dermatologia",
            address="Rua do Sol, 789",
            contact="11999999003"
        )

        # Busca por "Ana" - deve retornar apenas 1 resultado
        response = self.client.get(self.url_list, {"search": "Ana"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["id"], prof1.id)

    def test_buscar_profissional_por_profissao(self):
        """Testa a busca de profissionais por profissão."""
        ProfessionalFactory(profession="Cardiologista")
        ProfessionalFactory(profession="Cardiologista")
        ProfessionalFactory(profession="Neurologista")

        # Busca por "Cardiologista"
        response = self.client.get(
            self.url_list,
            {"search": "Cardiologista"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_ordenacao_profissionais(self):
        """Testa a ordenação de profissionais."""
        prof1 = ProfessionalFactory(preferred_name="Zé Silva")
        prof2 = ProfessionalFactory(preferred_name="Ana Costa")
        prof3 = ProfessionalFactory(preferred_name="Bruno Santos")

        # Ordenação crescente por nome
        response = self.client.get(
            self.url_list,
            {"ordering": "preferred_name"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]["id"], prof2.id)  # Ana
        self.assertEqual(response.data[1]["id"], prof3.id)  # Bruno
        self.assertEqual(response.data[2]["id"], prof1.id)  # Zé

    def test_recuperar_profissional_especifico(self):
        """Testa a recuperação de um profissional específico."""
        professional = ProfessionalFactory()
        url_detail = reverse(
            "professional-detail",
            kwargs={"pk": professional.pk}
        )

        response = self.client.get(url_detail)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], professional.id)
        self.assertEqual(
            response.data["preferred_name"],
            professional.preferred_name
        )

    def test_atualizar_profissional_completo(self):
        """Testa a atualização completa de um profissional (PUT)."""
        professional = ProfessionalFactory()
        url_detail = reverse(
            "professional-detail",
            kwargs={"pk": professional.pk}
        )

        dados_atualizacao = {
            "preferred_name": "Dr. Pedro Atualizado",
            "profession": "Oftalmologista",
            "address": "Nova Rua, 456, Rio de Janeiro - RJ",
            "contact": "21987654321"
        }

        response = self.client.put(url_detail, dados_atualizacao)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(
            professional.preferred_name,
            "Dr. Pedro Atualizado"
        )
        self.assertEqual(professional.profession, "Oftalmologista")

    def test_atualizar_profissional_parcial(self):
        """Testa a atualização parcial de um profissional (PATCH)."""
        professional = ProfessionalFactory(preferred_name="Dr. Original")
        url_detail = reverse(
            "professional-detail",
            kwargs={"pk": professional.pk}
        )

        dados_atualizacao = {"preferred_name": "Dr. Atualizado"}

        response = self.client.patch(url_detail, dados_atualizacao)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        professional.refresh_from_db()
        self.assertEqual(professional.preferred_name, "Dr. Atualizado")

    def test_deletar_profissional(self):
        """Testa a exclusão de um profissional."""
        professional = ProfessionalFactory()
        url_detail = reverse(
            "professional-detail",
            kwargs={"pk": professional.pk}
        )

        response = self.client.delete(url_detail)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_profissional_inexistente(self):
        """Testa o acesso a um profissional que não existe."""
        url_detail = reverse("professional-detail", kwargs={"pk": 999})

        response = self.client.get(url_detail)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


@pytest.mark.unit
class ProfessionalModelTestCase(APITestCase):
    """Testes unitários para o modelo Professional."""

    def test_str_representation(self):
        """Testa a representação string do modelo."""
        professional = ProfessionalFactory(
            preferred_name="Dr. Ana Silva",
            profession="Cardiologista"
        )

        expected = "Dr. Ana Silva - Cardiologista"
        self.assertEqual(str(professional), expected)

    def test_campos_obrigatorios(self):
        """Testa que todos os campos obrigatórios estão presentes."""
        professional = Professional()

        # Tenta salvar sem dados obrigatórios
        with self.assertRaises(Exception):
            professional.full_clean()

    def test_validacao_contato_modelo(self):
        """Testa a validação do contato diretamente no modelo."""
        professional = Professional(
            preferred_name="Dr. Teste",
            profession="Médico",
            address="Endereço Teste",
            contact="invalid_phone"
        )

        with self.assertRaises(Exception):
            professional.full_clean()

    def test_meta_ordering(self):
        """Testa a ordenação padrão do modelo."""
        prof1 = ProfessionalFactory(preferred_name="Zé Silva")
        prof2 = ProfessionalFactory(preferred_name="Ana Costa")

        professionals = Professional.objects.all()
        self.assertEqual(professionals.first(), prof2)  # Ana vem primeiro
        self.assertEqual(professionals.last(), prof1)   # Zé vem por último

    def test_timestamps(self):
        """Testa se os campos de timestamp são criados automaticamente."""
        professional = ProfessionalFactory()

        self.assertIsNotNone(professional.created_at)
        self.assertIsNotNone(professional.updated_at)

        # Testa se updated_at é atualizado
        original_updated_at = professional.updated_at
        professional.preferred_name = "Nome Atualizado"
        professional.save()

        professional.refresh_from_db()
        self.assertGreater(professional.updated_at, original_updated_at)