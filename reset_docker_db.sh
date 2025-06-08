#!/bin/bash

# Script para resetar o banco de dados através do Docker

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Verificar se o Docker e o Docker Compose estão instalados
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker não encontrado. Por favor, instale o Docker antes de continuar.${NC}"
    exit 1
fi

# Verificar Docker Compose (v2 é parte do Docker CLI)
if ! docker compose version &> /dev/null; then
    echo -e "${RED}Docker Compose não encontrado. Por favor, instale o Docker Compose antes de continuar.${NC}"
    exit 1
fi

# Processar argumentos de linha de comando
SKIP_CONFIRM=false
HELP=false

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -y|--yes) SKIP_CONFIRM=true ;;
        -h|--help) HELP=true ;;
        *) echo "Argumento desconhecido: $1"; exit 1 ;;
    esac
    shift
done

if [ "$HELP" = true ]; then
    echo "Uso: $0 [opções]"
    echo "Opções:"
    echo "  -y, --yes     Pular confirmação"
    echo "  -h, --help    Mostrar esta ajuda"
    exit 0
fi

echo -e "${YELLOW}Verificando se o Docker está em execução...${NC}"

# Verificar se os containers estão rodando
# O Docker Compose V2 usa formato de nome diferente
if ! docker ps | grep -q "medical_api-web" && ! docker ps | grep -q "_web"; then
    echo -e "${YELLOW}Iniciando os containers...${NC}"
    docker compose up -d
    
    # Esperar um momento para o banco de dados inicializar
    echo -e "${YELLOW}Aguardando o banco de dados inicializar...${NC}"
    sleep 5
fi

echo -e "${YELLOW}Resetando o banco de dados no container...${NC}"
echo -e "${RED}ATENÇÃO: Isso irá apagar todos os dados existentes!${NC}"

# Verificar se deve pular a confirmação
if [ "$SKIP_CONFIRM" = true ]; then
    answer="y"
else
    read -p "Continuar? (y/n): " answer
fi

if [[ $answer =~ ^[Yy]$ ]]; then
    echo -e "${YELLOW}Tentando executar comando no container...${NC}"
    
    # Executar o comando de reset dentro do container
    # Usando --no-input para evitar perguntas adicionais
    docker compose exec -T web python manage.py reset_db --no-input
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Banco de dados resetado com sucesso!${NC}"
    else
        echo -e "${RED}Erro ao resetar o banco de dados.${NC}"
        echo -e "${YELLOW}Tentando comando alternativo...${NC}"
        
        # Tentativa alternativa caso o primeiro comando falhe
        docker compose exec web python manage.py migrate zero
        docker compose exec web python manage.py migrate
        docker compose exec web python manage.py reset_db --no-input
        
        if [ $? -eq 0 ]; then
            echo -e "${GREEN}Banco de dados resetado com sucesso na segunda tentativa!${NC}"
        else
            echo -e "${RED}Falha ao resetar o banco de dados. Verifique os logs do container para mais detalhes.${NC}"
            echo -e "${YELLOW}Execute: ${NC}docker compose logs web"
        fi
    fi
else
    echo -e "${YELLOW}Operação cancelada pelo usuário.${NC}"
fi
