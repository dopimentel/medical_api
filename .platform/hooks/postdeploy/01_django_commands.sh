#!/bin/bash

# Garante que o script pare se qualquer comando falhar
set -e

# O Elastic Beanstalk exporta as variáveis de ambiente para um arquivo.
# Carregar este arquivo garante que todas as variáveis (DB_HOST, etc.)
# estejam disponíveis para os comandos seguintes.
source /opt/elasticbeanstalk/deployment/env

# Ativa o ambiente virtual do Python criado pelo EB
source /var/app/venv/*/bin/activate

# Navega para o diretório da aplicação
cd /var/app/current

# Executa os comandos do Django
echo "Running Django migrations..."
python manage.py migrate --noinput

echo "Running createsuperuser..."
if ! python manage.py shell -c "from django.contrib.auth import get_user_model; User = get_user_model(); exit(0) if User.objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() else exit(1)"; then
    python manage.py createsuperuser --noinput --username "$DJANGO_SUPERUSER_USERNAME" --email "$DJANGO_SUPERUSER_EMAIL"
else
    echo "Superuser \"$DJANGO_SUPERUSER_USERNAME\" already exists. Skipping createsuperuser."
fi

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Django commands executed successfully."
