import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework.test import APIClient
from tests.factories import UserFactory, ProfessionalFactory, AppointmentFactory

User = get_user_model()


@pytest.fixture
def api_client():
    """Cliente API para testes."""
    return APIClient()


@pytest.fixture
def user():
    """Usuário de teste."""
    return UserFactory()


@pytest.fixture
def admin_user():
    """Usuário admin para testes."""
    return UserFactory(is_staff=True, is_superuser=True)


@pytest.fixture
def client():
    """Cliente Django para testes."""
    return Client()


@pytest.fixture
def professional():
    """Profissional de teste."""
    return ProfessionalFactory()


@pytest.fixture
def appointment(professional):
    """Consulta de teste."""
    return AppointmentFactory(professional=professional)