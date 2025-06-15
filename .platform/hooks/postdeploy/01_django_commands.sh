#!/bin/bash

# O 'set -e' garante que o script pare imediatamente se algum comando falhar.
set -e

# Ativa o ambiente virtual da aplicação.
# No hook 'postdeploy', o código já está em /var/app/current.
source /var/app/current/venv/bin/activate

# Executa os comandos do Django.
# A variável DJANGO_SETTINGS_MODULE é lida das propriedades do ambiente EB.
echo "Running Django migrations..."
django-admin migrate --noinput

echo "Running collectstatic..."
django-admin collectstatic --noinput

echo "Django commands executed successfully."