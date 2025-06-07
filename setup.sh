#!/bin/bash

# Script para configurar o ambiente inicial para Medical API

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

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
    echo "  -y, --yes     Pular confirmações"
    echo "  -h, --help    Mostrar esta ajuda"
    exit 0
fi

echo -e "${YELLOW}Configurando ambiente para Medical API...${NC}"

# Verificar se .env existe, se não, criar a partir do exemplo
if [ ! -f .env ]; then
    echo -e "${YELLOW}Arquivo .env não encontrado. Criando a partir do exemplo...${NC}"
    if [ -f .env.example ]; then
        cp .env.example .env
        echo -e "${GREEN}Arquivo .env criado com sucesso!${NC}"
        echo -e "${YELLOW}Edite o arquivo .env com suas configurações antes de continuar.${NC}"
        if [ "$SKIP_CONFIRM" = false ]; then
            echo "Pressione Enter para continuar ou Ctrl+C para cancelar..."
            read
        fi
    else
        echo -e "${RED}Arquivo .env.example não encontrado. Não foi possível criar o .env.${NC}"
        exit 1
    fi
fi

# Perguntar como deseja executar o projeto
echo -e "${YELLOW}Como deseja executar o projeto?${NC}"
echo "1) Com Docker (recomendado)"
echo "2) Localmente com Poetry"
read -p "Escolha uma opção (1/2): " execution_option

if [ "$execution_option" = "1" ]; then
    # Verificar se o Docker está instalado
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}Docker não encontrado. Instale-o primeiro.${NC}"
        exit 1
    fi
    
    # Verificar Docker Compose (v2 é parte do Docker CLI)
    if ! docker compose version &> /dev/null; then
        echo -e "${RED}Docker Compose não encontrado. Instale-o primeiro.${NC}"
        exit 1
    fi
    
    # Iniciar os containers Docker
    echo -e "${YELLOW}Iniciando containers Docker...${NC}"
    docker compose up -d
    
    # Esperar um momento para o banco de dados inicializar
    echo -e "${YELLOW}Aguardando o banco de dados inicializar...${NC}"
    sleep 5
    
    # Verificar se os containers estão rodando
    # O Docker Compose V2 usa formato de nome diferente
    if ! docker ps | grep -q "medical_api-web" && ! docker ps | grep -q "_web"; then
        echo -e "${RED}Não foi possível iniciar os containers. Verifique os logs.${NC}"
        echo "docker compose logs"
        exit 1
    fi
    
    echo -e "${GREEN}Containers Docker iniciados com sucesso!${NC}"
    if [ "$SKIP_CONFIRM" = false ]; then
        echo -e "${YELLOW}Deseja resetar o banco de dados? [y/N]${NC}"
        read reset_db
    fi
    
    if [[ $reset_db =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Executando script de reset do banco de dados...${NC}"
        ./reset_docker_db.sh
    fi
    
    # Perguntar se deseja criar um superusuário
    if [ "$SKIP_CONFIRM" = false ]; then
        echo -e "${YELLOW}Deseja criar um superusuário para acesso ao admin? [y/N]${NC}"
        read create_superuser
    fi
    
    if [[ $create_superuser =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Criando superusuário...${NC}"
        echo -e "${YELLOW}Siga as instruções para definir nome de usuário, e-mail e senha:${NC}"
        docker compose exec web python manage.py createsuperuser
        echo -e "${GREEN}Superusuário criado com sucesso!${NC}"
    fi
    
    echo -e "${GREEN}Ambiente Docker configurado com sucesso!${NC}"
    echo -e "${YELLOW}Acesse a API em: ${NC}http://localhost:8000/api/docs/"
    echo -e "${YELLOW}Para administrar o banco: ${NC}http://localhost:8000/admin/"
    echo -e "${YELLOW}Para verificar os logs: ${NC}docker compose logs -f"
    
else
    # Verificar se o Poetry está instalado
    if ! command -v poetry &> /dev/null; then
        echo -e "${YELLOW}Poetry não encontrado. Instalando...${NC}"
        curl -sSL https://install.python-poetry.org | python3 -
        echo -e "${GREEN}Poetry instalado com sucesso!${NC}"
    fi
    
    # Instalar dependências
    echo -e "${YELLOW}Instalando dependências...${NC}"
    poetry install
    echo -e "${GREEN}Dependências instaladas com sucesso!${NC}"
    
    # Configurar banco de dados local - aviso sobre Docker
    echo -e "${YELLOW}ATENÇÃO: O projeto está configurado para usar PostgreSQL em Docker.${NC}"
    echo -e "${YELLOW}Certifique-se de ajustar as configurações em .env para seu banco local.${NC}"
    
    # Perguntar se deseja aplicar migrações
    if [ "$SKIP_CONFIRM" = false ]; then
        echo -e "${YELLOW}Deseja aplicar migrações no banco de dados local? [y/N]${NC}"
        read apply_migrations
    fi
    
    if [[ $apply_migrations =~ ^[Yy]$ ]]; then
        echo -e "${YELLOW}Executando migrações...${NC}"
        poetry run python manage.py migrate
        echo -e "${GREEN}Migrações aplicadas com sucesso!${NC}"
        
        # Perguntar se deseja limpar o banco de dados e criar dados iniciais
        if [ "$SKIP_CONFIRM" = false ]; then
            echo -e "${YELLOW}Deseja resetar o banco de dados e criar dados iniciais? [y/N]${NC}"
            read reset_local_db
        fi
        
        if [[ $reset_local_db =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Resetando o banco de dados local...${NC}"
            poetry run python manage.py reset_db --no-input
            echo -e "${GREEN}Banco de dados resetado com sucesso!${NC}"
        fi
        
        # Perguntar se deseja criar um superusuário
        if [ "$SKIP_CONFIRM" = false ]; then
            echo -e "${YELLOW}Deseja criar um superusuário para acesso ao admin? [y/N]${NC}"
            read create_superuser
        fi
        
        if [[ $create_superuser =~ ^[Yy]$ ]]; then
            echo -e "${YELLOW}Criando superusuário...${NC}"
            echo -e "${YELLOW}Siga as instruções para definir nome de usuário, e-mail e senha:${NC}"
            poetry run python manage.py createsuperuser
            echo -e "${GREEN}Superusuário criado com sucesso!${NC}"
        fi
    fi
    
    echo -e "${GREEN}Ambiente local configurado com sucesso!${NC}"
    echo -e "${YELLOW}Para rodar o servidor de desenvolvimento: ${NC}poetry run python manage.py runserver"
    echo -e "${YELLOW}Acesse a API em: ${NC}http://localhost:8000/api/docs/"
    echo -e "${YELLOW}Para administrar o banco: ${NC}http://localhost:8000/admin/"
fi
