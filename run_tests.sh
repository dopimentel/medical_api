#!/bin/bash
# filepath: /home/wbj-280-marcos/medical_api/run_tests.sh

# Verifica se Docker está em execução
if ! command -v docker &> /dev/null || ! docker info &> /dev/null
then
    echo "Docker não está em execução. Iniciando os testes localmente..."
    echo "Usando SQLite em memória para os testes."
    python manage.py test --settings=core.test_settings
    exit $?
fi

# Determina qual comando do Docker Compose usar (v1 ou v2)
if command -v docker-compose &> /dev/null
then
    DOCKER_COMPOSE="docker-compose"
else
    DOCKER_COMPOSE="docker compose"
fi

# Verifica se os containers estão rodando
if ! $DOCKER_COMPOSE ps | grep -q "web.*running"
then
    echo "O container web não está rodando. Iniciando os testes localmente..."
    echo "Usando SQLite em memória para os testes."
    python manage.py test --settings=core.test_settings
    exit $?
fi

echo "Executando testes no container Docker..."
$DOCKER_COMPOSE exec -T web python manage.py test --settings=core.test_settings
