"""
Configurações do Django por ambiente.
"""
import os
from decouple import config

# Determinar qual ambiente usar
ENVIRONMENT = config('DJANGO_SETTINGS_MODULE', default='core.settings.development')

if 'testing' in ENVIRONMENT:
    from .testing import *
elif 'production' in ENVIRONMENT:
    from .production import *
else:
    from .development import *