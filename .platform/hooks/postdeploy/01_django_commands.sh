#!/bin/bash

# Garante que o script pare se qualquer comando falhar
set -e

# ADICIONA O DIRETÓRIO DO POETRY AO PATH DO SISTEMA
export PATH=$PATH:/root/.local/bin


# O Elastic Beanstalk exporta as variáveis de ambiente para um arquivo.
# Carregar este arquivo garante que todas as variáveis (DB_HOST, etc.)
# estejam disponíveis para os comandos seguintes.
source /opt/elasticbeanstalk/deployment/env

# Imprime marcadores para facilitar a busca no log
echo "--- INÍCIO DO SCRIPT DE DEBUG 01_django_commands.sh ---"

echo "PASSO 1: Verificando o usuário atual"
whoami

echo "PASSO 2: Verificando o diretório de trabalho atual"
pwd

echo "PASSO 3: Listando o conteúdo de /var/app/current/"
ls -la /var/app/current/

echo "PASSO 4: Verificando se o arquivo de variáveis de ambiente existe"
if [ -f /opt/elasticbeanstalk/deployment/env ]; then
    echo "Arquivo 'env' encontrado. Carregando variáveis..."
    source /opt/elasticbeanstalk/deployment/env
else
    echo "ERRO CRÍTICO: Arquivo /opt/elasticbeanstalk/deployment/env NÃO ENCONTRADO."
    exit 1
fi

echo "PASSO 5: Verificando se o Poetry está no PATH"
export PATH=$PATH:/root/.local/bin
which poetry

echo "PASSO 6: Tentando rodar o migrate (o erro deve aparecer abaixo se falhar)"
poetry run python manage.py migrate --noinput

echo "PASSO 7: Tentando rodar o collectstatic"
poetry run python manage.py collectstatic --noinput

echo "--- FIM DO SCRIPT DE DEBUG 01_django_commands.sh (SUCESSO) ---"