"""
Configurações específicas para testes.
Importa todas as configurações do settings.py e sobrescreve o banco de dados para usar SQLite em memória.
"""

from .settings import *

# Substitui a configuração do banco de dados para usar SQLite em memória durante os testes
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Desativa DEBUG para testes
DEBUG = False

# Acelera os testes de senha
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.MD5PasswordHasher",
]

# Minimiza o uso de cache
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}
