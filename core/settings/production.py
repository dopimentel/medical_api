"""Configurações para ambiente de produção."""
from .base import *

DEBUG = False
ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS", 
    default="", 
    cast=lambda v: [s.strip() for s in v.split(",")]
)

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DB_NAME"),
        "USER": config("DB_USER"),
        "PASSWORD": config("DB_PASSWORD"),
        "HOST": config("DB_HOST"),
        "PORT": config("DB_PORT", cast=int),
        "CONN_MAX_AGE": 60,
        "OPTIONS": {
            "sslmode": "require",
        },
    }
}

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Logging
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": (
                "{levelname} {asctime} {module} {process:d} "
                "{thread:d} {message}"
            ),
            "style": "{",
        },
    },
    "handlers": {
        "file": {
            "level": "INFO",
            "class": "logging.FileHandler",
            "filename": "/var/log/django/medical_api.log",
            "formatter": "verbose",
        },
        "console": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["file", "console"],
        "level": "INFO",
    },
}

REST_FRAMEWORK.update(
    {
        "DEFAULT_RENDERER_CLASSES": [
            "rest_framework.renderers.JSONRenderer",
        ],
        "DEFAULT_AUTHENTICATION_CLASSES": [
            "rest_framework.authentication.SessionAuthentication",
            "rest_framework.authentication.BasicAuthentication",
        ],
        "DEFAULT_PERMISSION_CLASSES": [
            "rest_framework.permissions.IsAuthenticated",
        ],
        "DEFAULT_PAGINATION_CLASS": (
            "rest_framework.pagination.PageNumberPagination"
        ),
        "PAGE_SIZE": 20,
    }
)
SPECTACULAR_SETTINGS.update(
    {
        "SERVE_INCLUDE_SCHEMA": True,
        "SWAGGER_UI_SETTINGS": {
            "deepLinking": True,
            "displayOperationId": True,
            "defaultModelsExpandDepth": -1,
            "defaultModelExpandDepth": 1,
            "docExpansion": "none",
        },
        "REDOC_SETTINGS": {
            "LAZY_RENDERING": True,
            "FAVICON_URL": "/static/favicon.ico",
        },
    }
)