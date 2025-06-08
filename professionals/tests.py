from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Professional


class ProfessionalAPITestCase(APITestCase):
    """
    Testes para a API de Profissionais.
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

    def test_list_professionals(self):
        """
        Testa a listagem de profissionais.
        """
        url = reverse('professional-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['preferred_name'], "Dr. Teste")

    def test_create_professional_valid(self):
        """
        Testa a criação de um profissional com dados válidos.
        """
        url = reverse('professional-list')
        data = {
            'preferred_name': 'Dra. Nova',
            'profession': 'Neurologista',
            'address': 'Avenida Paulista, 1000',
            'contact': '11987654321'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Professional.objects.count(), 2)
        self.assertEqual(Professional.objects.last().preferred_name, 'Dra. Nova')
        self.assertEqual(Professional.objects.last().contact, '11987654321')

    def test_create_professional_invalid_contact(self):
        """
        Testa a validação de contato inválido.
        """
        url = reverse('professional-list')
        # Testa com contato com formato incorreto (menos de 11 dígitos)
        data = {
            'preferred_name': 'Dra. Teste Erro',
            'profession': 'Pediatra',
            'address': 'Rua de Teste, 456',
            'contact': '1234567'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact', response.data)
        
        # Testa com contato contendo caracteres não-numéricos
        data['contact'] = '+11 9876-5432'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact', response.data)
        
        # Testa com contato contendo mais de 11 dígitos
        data['contact'] = '123456789012'
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('contact', response.data)
        
    def test_retrieve_professional(self):
        """
        Testa a recuperação de um profissional específico.
        """
        url = reverse('professional-detail', args=[self.professional.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['preferred_name'], self.professional.preferred_name)
        self.assertEqual(response.data['contact'], self.professional.contact)

    def test_update_professional(self):
        """
        Testa a atualização de um profissional.
        """
        url = reverse('professional-detail', args=[self.professional.id])
        data = {
            'preferred_name': 'Dr. Atualizado',
            'profession': 'Ortopedista',
            'address': 'Endereço Atualizado',
            'contact': '11912345678'
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.professional.refresh_from_db()
        self.assertEqual(self.professional.preferred_name, 'Dr. Atualizado')
        self.assertEqual(self.professional.contact, '11912345678')

    def test_delete_professional(self):
        """
        Testa a exclusão de um profissional.
        """
        url = reverse('professional-detail', args=[self.professional.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Professional.objects.count(), 0)

    def test_search_professional(self):
        """
        Testa a busca de profissionais.
        """
        # Cria outro profissional para testar a busca
        Professional.objects.create(
            preferred_name="Dra. Outra",
            profession="Dermatologista",
            address="Endereço Outro",
            contact="11987654321"
        )
        
        url = reverse('professional-list') + '?search=Teste'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['preferred_name'], 'Dr. Teste')
        
        url = reverse('professional-list') + '?search=Dermat'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['preferred_name'], 'Dra. Outra')
