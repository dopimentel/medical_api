"""
Configurações para ambiente de desenvolvimento
"""
from .base import *

DEBUG = True
ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0"]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME", default="medical_api_dev"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASSWORD", default="postgres"),
        "HOST": config("DB_HOST", default="localhost"),
        "PORT": config("DB_PORT", default=5432, cast=int),
    }
}


# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}

# Debug toolbar (opcional)
if DEBUG:
    try:
        import debug_toolbar
        INSTALLED_APPS += ["debug_toolbar"]
        MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]
        INTERNAL_IPS = ["127.0.0.1"]
    except ImportError:
        pass