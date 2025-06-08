"""
Configurações para ambiente de testes
"""
from .base import *

DEBUG = False
ALLOWED_HOSTS = ["testserver"]

# Database em memória para testes mais rápidos
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Desabilitar migrações para testes mais rápidos
class DisableMigrations:
    def __contains__(self, item):
        return True
    
    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Cache em memória para testes
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
    }
}

# Configurações de senha simples para testes
AUTH_PASSWORD_VALIDATORS = []

# Email backend para testes
EMAIL_BACKEND = "django.core.mail.backends.locmem.EmailBackend"

# Logging mínimo para testes
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "level": "CRITICAL",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "CRITICAL",
    },
}