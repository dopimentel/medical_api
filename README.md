# Medical API

API RESTful para gerenciamento de profissionais da saúde e consultas médicas.

## Recursos

- Cadastro, edição, exclusão e listagem de profissionais da saúde
- Cadastro e edição de consultas médicas com vínculo ao profissional
- Busca por consultas utilizando o ID do profissional
- Segurança e validação de dados

## Tecnologias utilizadas

- Django 5.2.2
- Django REST Framework
- PostgreSQL
- Docker e Docker Compose
- Poetry para gerenciamento de dependências

## Configuração do ambiente

### Usando o script automatizado

1. Clone o repositório
2. Execute o script de configuração:

```bash
# Execução interativa com confirmações
./setup.sh

# Execução com configurações padrão (sem confirmações)
./setup.sh -y

# Mostrar opções de ajuda
./setup.sh -h
```

O script oferece duas opções de configuração:

1. **Docker (recomendado)**: Inicia os containers e configura todo o ambiente
2. **Local com Poetry**: Instala dependências e configura o ambiente local

Funcionalidades do script:

- Verifica se o arquivo `.env` existe e o cria a partir do exemplo se necessário
- Detecta automaticamente o Docker Compose V2 ou V1
- Oferece opção para resetar o banco de dados e carregar dados iniciais
- Permite criar um superusuário para acesso ao admin
- Aguarda a inicialização do banco de dados para evitar erros
- Exibe links úteis para acessar a API e o painel administrativo

O script é compatível com Docker Compose V2 (comando `docker compose`) e Docker Compose V1 (comando `docker-compose`).

### Configuração manual

1. Clone o repositório
2. Crie um arquivo `.env` baseado no `.env.example`:

```bash
cp .env.example .env
```

3. Edite o arquivo `.env` com suas configurações
4. Instale as dependências:

```bash
poetry install
```

5. Execute as migrações:

```bash
poetry run python manage.py migrate
```

6. Crie um superusuário:

```bash
poetry run python manage.py createsuperuser
```

7. Inicie o servidor:

```bash
poetry run python manage.py runserver
```

### Usando Docker Compose

1. Clone o repositório
2. Crie um arquivo `.env` baseado no `.env.example`
3. Execute:

```bash
# Para Docker Compose V2
docker compose up -d

# OU para Docker Compose V1
docker-compose up -d
```

4. Crie um superusuário para acessar o admin:

```bash
# Para Docker Compose V2
docker compose exec web python manage.py createsuperuser

# OU para Docker Compose V1
docker-compose exec web python manage.py createsuperuser
```

### Configuração do Superusuário

Para facilitar o acesso ao painel administrativo, você pode configurar um superusuário automático no arquivo `.env`:

```bash
# Configurações do superusuário automático
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=minhasenhasegura
```

Essas configurações são usadas em dois cenários:

1. Ao resetar o banco de dados com o comando `python manage.py reset_db`
2. Ao criar um superusuário via script `setup.sh` usando a opção "Usar valores do arquivo .env"

**Nota de segurança**: Para ambientes de produção, utilize sempre senhas fortes e únicas.

## Resetando o banco de dados

### Usando Docker (Recomendado)

Para resetar o banco de dados e carregar dados iniciais quando estiver usando Docker:

```bash
# Executar o script auxiliar que gerencia o processo através do Docker
./reset_docker_db.sh

# Para pular a confirmação
./reset_docker_db.sh -y

# Para ver ajuda
./reset_docker_db.sh -h
```

Este script irá:

1. Verificar se o Docker e Docker Compose estão instalados
2. Detectar automaticamente a versão do Docker Compose (V1 ou V2)
3. Verificar se os containers estão rodando e iniciá-los se necessário
4. Executar o comando de reset do banco de dados dentro do container
5. Carregar dados iniciais

O script é compatível com Docker Compose V2 (comando `docker compose`) e Docker Compose V1 (comando `docker-compose`).

### Comando direto

Se você estiver dentro do container ou configurou o ambiente manualmente:

```bash
# Comando básico
python manage.py reset_db

# Sem confirmação
python manage.py reset_db --no-input

# Sem carregar dados iniciais
python manage.py reset_db --no-seed
```

O reset do banco de dados:

1. Remove todas as tabelas
2. Recria as migrações
3. Cria um superusuário admin (senha definida em .env)
4. Cria 5 profissionais de exemplo
5. Cria 3 consultas para cada profissional

## Documentação da API

A documentação da API está disponível em:

- `/api/docs/` - Interface Swagger
- `/api/redoc/` - Interface ReDoc
- `/api/schema/` - Schema OpenAPI

## Estrutura dos dados

### Profissionais

- `preferred_name` - Nome social
- `profession` - Profissão
- `address` - Endereço
- `contact` - Contato

### Consultas

- `date` - Data e hora da consulta
- `professional` - Profissional vinculado (chave estrangeira)

## Desenvolvimento

### Requisitos do sistema

- Python 3.12+
- Poetry 1.7.1+
- Docker e Docker Compose (recomendado)
- PostgreSQL (se não estiver usando Docker)

### Configuração do ambiente de desenvolvimento

Para um ambiente de desenvolvimento ideal, recomendamos usar o Docker:

```bash
# Instale o código e inicie os containers
./setup.sh

# Selecione a opção 1 (Docker)
```

### Comandos úteis para desenvolvimento

#### Com Docker

```bash
# Iniciar os containers
docker compose up -d

# Ver logs em tempo real
docker compose logs -f

# Executar comando dentro do container web
docker compose exec web python manage.py comando

# Parar os containers
docker compose down

# Parar e remover volumes (apaga dados do banco)
docker compose down -v
```

#### Sem Docker (ambiente local)

```bash
# Ativar ambiente virtual do Poetry
poetry shell

# Instalar dependências
poetry install

# Executar migrations
python manage.py migrate

# Iniciar servidor de desenvolvimento
python manage.py runserver

# Criar superusuário
python manage.py createsuperuser
```

## Solução de Problemas

### Problemas com Docker Compose

#### Comando `docker-compose` não encontrado, mas tenho Docker instalado

Se você instalou o Docker recentemente, provavelmente está usando o Docker Compose V2, que é integrado ao Docker CLI. Use:

```bash
docker compose
```

em vez de

```bash
docker-compose
```

O script `setup.sh` detecta automaticamente qual versão você está usando.

#### Erro ao conectar com o banco de dados

Verifique se:

1. O banco de dados está rodando:

```bash
docker compose ps
```

2. As configurações no arquivo `.env` correspondem às do `docker-compose.yml`

3. O container do banco de dados inicializou completamente (pode levar alguns segundos)

#### Erros de migração ou ModuleNotFoundError

Execute o script de reset do banco de dados:

```bash
./reset_docker_db.sh -y
```

### Problemas com Poetry

#### Comando `poetry` não encontrado

Instale o Poetry seguindo a [documentação oficial](https://python-poetry.org/docs/#installation).

#### Dependências não instaladas corretamente

```bash
# Limpe o cache e reinstale
poetry cache clear --all pypi
poetry install --no-cache
```

## Superusuário Admin

Por padrão, o projeto cria um superusuário durante o reset do banco de dados, usando as configurações do arquivo `.env`. Para personalizar o superusuário, adicione as seguintes variáveis ao seu arquivo `.env`:

```
# Configurações do superusuário automático
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@example.com
DJANGO_SUPERUSER_PASSWORD=sua_senha_segura
```

Estas configurações serão usadas:

1. Durante a execução do script `./reset_docker_db.sh`
2. Quando o comando `python manage.py reset_db` for executado
3. Durante a instalação inicial com `./setup.sh`

**Nota:** Se a variável `DJANGO_SUPERUSER_PASSWORD` não estiver definida, o superusuário não será criado automaticamente.

## Estrutura do Projeto

A API está organizada em três aplicações Django principais:

### core

Contém configurações globais do projeto:

- `settings.py`: Configurações do Django
- `urls.py`: Roteamento principal da API
- `management/commands/reset_db.py`: Script para resetar o banco de dados

### professionals

Gerencia os profissionais da saúde:

- `models.py`: Define o modelo Professional
- `serializers.py`: Serializa dados do modelo para JSON
- `views.py`: Define o ProfessionalViewSet com filtros
- `urls.py`: Configura as rotas da API para profissionais
- `admin.py`: Configura a interface administrativa

### appointments

Gerencia as consultas médicas:

- `models.py`: Define o modelo Appointment
- `serializers.py`: Serializa dados do modelo para JSON
- `views.py`: Define o AppointmentViewSet com filtros
- `urls.py`: Configura as rotas da API para consultas
- `admin.py`: Configura a interface administrativa

### Scripts de Utilitário

- `setup.sh`: Configura o ambiente inicial
- `reset_docker_db.sh`: Reseta o banco de dados no Docker
- `docker-compose.yml`: Configuração dos serviços Docker
