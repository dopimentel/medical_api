#!/bin/bash
# Script para execução de testes da Medical API

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Variáveis
TEST_DB_NAME="test_medical_api"
CONTAINER_NAME="medical_api-web-1"

# Função para verificar se Docker está rodando
check_docker() {
    if ! command -v docker &> /dev/null || ! docker info &> /dev/null; then
        return 1
    fi
    return 0
}

# Função para verificar se containers estão rodando
check_containers() {
    if docker ps | grep -q "medical_api.*web" || docker ps | grep -q "_web.*Up"; then
        return 0
    fi
    return 1
}

# Função para executar testes localmente com SQLite
run_local_tests() {
    echo -e "${YELLOW}Executando testes localmente com SQLite em memória...${NC}"
    python manage.py test --settings=core.settings.testing
    return $?
}

# Função para criar banco de teste
create_test_database() {
    echo -e "${BLUE}Criando banco de dados de teste: ${TEST_DB_NAME}${NC}"
    
    # Criar banco de teste
    docker compose exec -T db psql -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $TEST_DB_NAME;" 2>/dev/null || true
    docker compose exec -T db psql -U "$DB_USER" -d postgres -c "CREATE DATABASE $TEST_DB_NAME;"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Banco de teste criado com sucesso!${NC}"
        return 0
    else
        echo -e "${RED}Erro ao criar banco de teste${NC}"
        return 1
    fi
}

# Função para executar migrações no banco de teste
run_test_migrations() {
    echo -e "${BLUE}Executando migrações no banco de teste...${NC}"
    
    # Configurar variável de ambiente para banco de teste
    docker compose exec -T web bash -c "
        export DJANGO_SETTINGS_MODULE=core.settings.development
        export DB_NAME=$TEST_DB_NAME
        python manage.py migrate --no-input
    "
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Migrações executadas com sucesso!${NC}"
        return 0
    else
        echo -e "${RED}Erro ao executar migrações${NC}"
        return 1
    fi
}

# Função para popular banco de teste com seeders
seed_test_database() {
    echo -e "${BLUE}Populando banco de teste com dados iniciais...${NC}"
    
    # Note: Os testes usam Factories para criar dados dinamicamente
    # Não precisamos popular o banco previamente, pois cada teste cria seus próprios dados
    
    echo -e "${GREEN}Banco de teste pronto para uso com Factories!${NC}"
}

# Função para executar testes no container
run_container_tests() {
    echo -e "${BLUE}Executando testes no container Docker com PostgreSQL...${NC}"
    
    # Executar testes
    docker compose exec -T web bash -c "
        export DJANGO_SETTINGS_MODULE=core.settings.development
        export DB_NAME=$TEST_DB_NAME
        pytest -v --tb=short
    "
    
    local test_result=$?
    
    if [ $test_result -eq 0 ]; then
        echo -e "${GREEN}Todos os testes passaram!${NC}"
    else
        echo -e "${RED}Alguns testes falharam${NC}"
    fi
    
    return $test_result
}

# Função para limpar banco de teste
cleanup_test_database() {
    echo -e "${YELLOW}Limpando banco de dados de teste...${NC}"
    
    docker compose exec -T db psql -U "$DB_USER" -d postgres -c "DROP DATABASE IF EXISTS $TEST_DB_NAME;" 2>/dev/null || true
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Banco de teste removido com sucesso!${NC}"
    else
        echo -e "${YELLOW}Banco de teste pode não ter sido removido completamente${NC}"
    fi
}

# Função principal
main() {
    echo -e "${BLUE}Medical API - Script de Testes${NC}"
    echo -e "${BLUE}=====================================${NC}"
    
    # Verificar se Docker está disponível
    if ! check_docker; then
        echo -e "${YELLOW}Docker não está disponível. Executando testes localmente...${NC}"
        run_local_tests
        exit $?
    fi
    
    # Determinar comando do Docker Compose
    if command -v docker-compose &> /dev/null; then
        DOCKER_COMPOSE="docker-compose"
    else
        DOCKER_COMPOSE="docker compose"
    fi
    
    # Verificar se containers estão rodando
    if ! check_containers; then
        echo -e "${YELLOW}Containers não estão rodando. Tentando iniciar...${NC}"
        $DOCKER_COMPOSE up -d
        
        # Aguardar containers iniciarem
        echo -e "${YELLOW}Aguardando containers iniciarem...${NC}"
        sleep 10
        
        # Verificar novamente
        if ! check_containers; then
            echo -e "${YELLOW}Não foi possível iniciar containers. Executando testes localmente...${NC}"
            run_local_tests
            exit $?
        fi
    fi
    
    # Carregar variáveis de ambiente do .env
    if [ -f .env ]; then
        export $(grep -v '^#' .env | xargs)
    fi
    
    echo -e "${GREEN}Containers Docker disponíveis. Executando testes no ambiente Docker...${NC}"
    
    # Configurar armadilha para cleanup
    trap cleanup_test_database EXIT
    
    # Executar pipeline de testes
    if create_test_database && run_test_migrations; then
        seed_test_database
        run_container_tests
        test_exit_code=$?
    else
        echo -e "${RED}Erro na configuração do ambiente de teste${NC}"
        test_exit_code=1
    fi
    
    # Cleanup será executado automaticamente pela trap
    exit $test_exit_code
}

# Verificar argumentos
case "${1:-}" in
    -h|--help)
        echo "Uso: $0 [opções]"
        echo "Opções:"
        echo "  -h, --help     Mostrar esta ajuda"
        echo "  --local        Forçar execução local com SQLite"
        echo ""
        echo "Comportamento:"
        echo "  - Se Docker disponível: executa no container com PostgreSQL"
        echo "  - Se Docker indisponível: executa localmente com SQLite"
        echo "  - Cria banco de teste temporário e remove após execução"
        exit 0
        ;;
    --local)
        echo -e "${YELLOW}Execução local forçada pelo usuário${NC}"
        run_local_tests
        exit $?
        ;;
esac

# Executar função principal
main 
