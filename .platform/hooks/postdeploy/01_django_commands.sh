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

echo "Running collectstatic..."
python manage.py collectstatic --noinput

echo "Django commands executed successfully."
