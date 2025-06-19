# 🧪 Sistema de Testes - Medical API

Este documento explica como usar o novo sistema de testes que automaticamente escolhe entre execução local (SQLite) ou em container (PostgreSQL).

## 🚀 Execução Rápida

```bash
# Executar testes (automático)
./run_tests.sh

# Forçar execução local
./run_tests.sh --local

# Ver ajuda
./run_tests.sh --help
```

## 🔄 Como Funciona

### Detecção Automática de Ambiente

O script `run_tests.sh` detecta automaticamente qual ambiente usar:

1. **Docker disponível + containers rodando**: 
   - ✅ Executa no container com PostgreSQL
   - ✅ Cria banco de teste temporário
   - ✅ Executa migrações e seeders
   - ✅ Remove banco após os testes

2. **Docker indisponível ou containers parados**:
   - ✅ Executa localmente com SQLite em memória
   - ✅ Mais rápido para desenvolvimento

### Pipeline de Teste no Container

Quando executa no container, o script segue estes passos:

```
1. 🔍 Verificar se containers estão rodando
2. 📊 Criar banco de teste temporário (test_medical_api)
3. 🔧 Executar migrações no banco de teste
4. 🌱 Popular com dados iniciais (opcional)
5. 🧪 Executar testes com pytest
6. 🧹 Remover banco de teste (cleanup automático)
```

## 📁 Configurações de Teste

### Para Container (PostgreSQL)
- **Arquivo**: `core/settings/development.py`
- **Banco**: PostgreSQL no container Docker
- **Database**: `test_medical_api` (temporário)
- **Vantagem**: Mesmo ambiente que desenvolvimento

### Para Local (SQLite)  
- **Arquivo**: `core/settings/testing.py`
- **Banco**: SQLite em memória (`:memory:`)
- **Vantagem**: Mais rápido, sem dependências

## 🛠️ Scripts Auxiliares

### Reset Completo do Banco Docker
```bash
./reset_docker_db.sh
```
Reseta o banco principal (não o de teste) e carrega dados iniciais.

### Factories para Testes
O projeto usa **Factory Boy** para criar dados de teste dinamicamente:

```python
# Exemplo de uso nas classes de teste
from tests.factories import ProfessionalFactory, AppointmentFactory

# Criar dados únicos automaticamente
professional = ProfessionalFactory()

# Customizar campos específicos
professional = ProfessionalFactory(
    preferred_name="Dr. João Silva",
    profession="Cardiologista"
)

# Criar múltiplos registros
professionals = ProfessionalFactory.create_batch(5)
```

## 🎯 Comandos Específicos

### Testes com Django Test Runner
```bash
# No container
docker compose exec web python manage.py test --settings=core.settings.development

# Local
python manage.py test --settings=core.settings.testing
```

### Testes com Pytest
```bash
# No container 
docker compose exec web pytest --tb=short

# Local
DJANGO_SETTINGS_MODULE=core.settings.testing pytest
```

### Testes com Coverage
```bash
# No container
docker compose exec web pytest --cov=. --cov-report=html

# Local  
DJANGO_SETTINGS_MODULE=core.settings.testing pytest --cov=. --cov-report=html
```

## 🔧 Variáveis de Ambiente

O script usa as seguintes variáveis do arquivo `.env`:

- `DB_USER`: Usuário do PostgreSQL
- `DB_PASSWORD`: Senha do PostgreSQL  
- `DB_NAME`: Nome do banco principal
- `DB_HOST`: Host do banco (geralmente `db`)
- `DB_PORT`: Porta do banco (geralmente `5432`)

## 🚨 Solução de Problemas

### Containers não iniciam
```bash
# Verificar status
docker compose ps

# Ver logs
docker compose logs web

# Reiniciar
docker compose down && docker compose up -d
```

### Banco de teste não é criado
```bash
# Verificar se PostgreSQL está acessível
docker compose exec db psql -U $DB_USER -l

# Verificar permissões
docker compose exec db psql -U $DB_USER -c "SELECT current_user;"
```

### Testes falham por dependências
```bash
# Instalar dependências no container
docker compose exec web pip install -r requirements.txt

# Ou rebuildar imagem
docker compose build web
```

## 📊 Exemplo de Saída

```
🏥 Medical API - Script de Testes
=====================================
🚀 Containers Docker disponíveis. Executando testes no ambiente Docker...
📊 Criando banco de dados de teste: test_medical_api
✅ Banco de teste criado com sucesso!
🔧 Executando migrações no banco de teste...
✅ Migrações executadas com sucesso!
🌱 Populando banco de teste com dados iniciais...
✅ Banco de teste populado!
🐳 Executando testes no container Docker com PostgreSQL...
✅ Todos os testes passaram!
🧹 Limpando banco de dados de teste...
✅ Banco de teste removido com sucesso!
```

## 🎉 Vantagens

- ✅ **Automático**: Escolhe o melhor ambiente automaticamente
- ✅ **Isolado**: Banco de teste separado, sem afetar dados de desenvolvimento
- ✅ **Limpo**: Remove banco de teste automaticamente
- ✅ **Flexível**: Pode forçar execução local quando necessário
- ✅ **Realista**: Testa com PostgreSQL igual produção
- ✅ **Rápido**: Fallback para SQLite quando Docker não disponível
- ✅ **Simples**: Usa apenas Factories, sem fixtures desnecessárias
