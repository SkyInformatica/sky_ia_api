# Sky IA API - Nova Estrutura

Este documento descreve a nova estrutura refatorada do projeto Sky IA API, seguindo as melhores práticas para aplicações FastAPI.

## 📁 Estrutura do Projeto

```
sky_ia_api/
├── src/
│   └── app/                    # Pacote principal da aplicação
│       ├── __init__.py
│       ├── main.py             # Instância FastAPI + configuração de rotas
│       ├── core/               # Configurações centrais
│       │   ├── __init__.py
│       │   └── config.py       # Settings via Pydantic BaseSettings
│       ├── models/             # Modelos de domínio Pydantic
│       │   ├── __init__.py
│       │   └── base.py         # Modelos base (Documento, RequisicaoDocumento)
│       ├── schemas/            # Modelos de entrada/saída da API
│       │   ├── __init__.py
│       │   ├── qualificacao_schema.py
│       │   └── escritura_publica_schema.py
│       ├── services/           # Regras de negócio
│       │   ├── __init__.py
│       │   ├── openai_service.py
│       │   └── document_service.py
│       ├── routers/            # Controladores (endpoints)
│       │   ├── __init__.py
│       │   ├── qualificacao_router.py
│       │   ├── escritura_publica_router.py
│       │   └── frontend_router.py
│       ├── helpers/            # Funções utilitárias
│       │   ├── __init__.py
│       │   └── logging_helper.py
│       ├── static/             # Arquivos estáticos (CSS, JS)
│       │   ├── css/
│       │   │   └── style.css
│       │   └── js/
│       │       └── app.js
│       └── templates/          # Templates Jinja2
│           └── index.html
├── tests/                      # Testes espelhando src/app
│   ├── __init__.py
│   ├── conftest.py            # Configurações e fixtures
│   ├── test_main.py           # Testes da aplicação principal
│   ├── routers/
│   │   ├── __init__.py
│   │   └── test_qualificacao_router.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── test_document_service.py
│   └── schemas/
│       ├── __init__.py
│       └── test_qualificacao_schema.py
├── sky_ia_api_new.py          # Ponto de entrada (compatibilidade)
├── pyproject.toml             # Configuração do projeto
├── requirements.txt           # Dependências
└── prompts.yaml               # Configuração de prompts
```

## 🚀 Como Executar

### Desenvolvimento

```bash
# Instalar dependências
uv sync

# Executar servidor de desenvolvimento
uv run uvicorn src.app.main:app --host 0.0.0.0 --port 8000 --reload --workers 1 --log-level info --use-colors
```

### Produção

```bash
# Usar o arquivo de compatibilidade
uv run uvicorn sky_ia_api_new:app --host 0.0.0.0 --port 8000
```

## 🧪 Executar Testes

```bash
# Executar todos os testes
uv run pytest

# Executar testes com cobertura
uv run pytest --cov=src/app

# Executar testes específicos
uv run pytest tests/routers/test_qualificacao_router.py
```

## 📋 Principais Mudanças

### 1. Estrutura Organizada
- **Separação clara de responsabilidades**: models, schemas, services, routers
- **Helpers centralizados**: funções utilitárias em módulos específicos
- **Configurações centralizadas**: todas as configurações em `core/config.py`

### 2. Nomenclatura em Português
- **Modelos**: `Documento`, `RequisicaoDocumento`
- **Funções**: `processar_documentos()`, `enviar_para_openai()`
- **Variáveis**: `chave_api_openai`, `arquivos_upload`

### 3. Melhorias de Código
- **Type hints** em todas as funções
- **Documentação** em português brasileiro
- **Tratamento de erros** robusto
- **Logging padronizado**

### 4. Testes Abrangentes
- **Testes unitários** para services e schemas
- **Testes de integração** para routers
- **Fixtures reutilizáveis** no conftest.py
- **Mocks apropriados** para dependências externas

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Configurações da aplicação
APP_NAME="Sky IA API"
APP_VERSION="2.0.0"
DEBUG=true
LOG_LEVEL="INFO"

# Configurações da OpenAI (opcional, pode ser fornecida via API)
OPENAI_API_KEY="sua-chave-aqui"

# Configurações de CORS
ALLOWED_ORIGINS="http://localhost:3000,http://localhost:8080"
```

### Prompts

Os prompts são configurados no arquivo `prompts.yaml`:

```yaml
qualificacao:
  prompt: "Analise os documentos fornecidos..."
  expected_format: "json"

escritura_publica:
  prompt: "Extraia as informações da escritura..."
  expected_format: "json"
```

## 📚 Documentação da API

Após iniciar o servidor, acesse:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Frontend**: http://localhost:8000/app

## 🔄 Migração da Estrutura Antiga

A estrutura antiga ainda está presente para compatibilidade:

- `models/` → `src/app/models/`
- `services/` → `src/app/services/`
- `routes/` → `src/app/routers/`
- `static/` → `src/app/static/`
- `templates/` → `src/app/templates/`

O arquivo `sky_ia_api_new.py` mantém a compatibilidade com deployments existentes.

## 🛠️ Próximos Passos

1. **Remover estrutura antiga** após validação completa
2. **Adicionar mais testes** para cobertura completa
3. **Implementar cache** para respostas da OpenAI
4. **Adicionar métricas** e monitoramento
5. **Documentar APIs** com exemplos detalhados

## 🤝 Contribuição

Para contribuir com o projeto:

1. Siga as convenções de nomenclatura em português
2. Adicione testes para novas funcionalidades
3. Use type hints em todas as funções
4. Documente código em português brasileiro
5. Execute os testes antes de fazer commit

```bash
# Verificar qualidade do código
uv run pytest
uv run black src/ tests/
uv run isort src/ tests/
uv run flake8 src/ tests/
```