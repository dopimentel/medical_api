#!/bin/bash

# Garante que o script pare se qualquer comando falhar
set -e

# ADICIONA O DIRETÓRIO DO POETRY AO PATH DO SISTEMA
export PATH=$PATH:/root/.local/bin


# O Elastic Beanstalk exporta as variáveis de ambiente para um arquivo.
# Carregar este arquivo garante que todas as variáveis (DB_HOST, etc.)
# estejam disponíveis para os comandos seguintes.
source /opt/elasticbeanstalk/deployment/env

# Executa os comandos do Django usando 'poetry run', que ativa o venv
# Os Platform Hooks rodam por padrão no diretório /var/app/staging.
echo "Running Django migrations..."
poetry run python manage.py migrate --noinput

echo "Running collectstatic..."
poetry run python manage.py collectstatic --noinput

echo "Django commands executed successfully."