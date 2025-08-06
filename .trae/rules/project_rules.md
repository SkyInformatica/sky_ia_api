# Regras do Projeto - Python API

## Stack Tecnológica

### Frameworks e Bibliotecas Principais

- **FastAPI**: Framework web principal para APIs REST
- **OpenAI**: Integração com modelos de IA da OpenAI
- **Pydantic**: Validação de dados e serialização
- **uv**: Gerenciador de pacotes e dependências (substituto do pip)
- **Uvicorn**: Servidor ASGI para desenvolvimento

### Gerenciamento de Dependências

- Use **uv** como gerenciador de pacotes principal
- Mantenha `pyproject.toml` atualizado com todas as dependências
- Use versões específicas para dependências críticas
- Comandos principais:
  - `uv add <pacote>` para adicionar dependências
  - `uv sync` para sincronizar ambiente
  - `uv run <comando>` para executar scripts

## Estilo de Código Python

### Convenções de Nomenclatura

- **SEMPRE** use snake_case para:
  - Nomes de variáveis: `openai_api_key`, `dados_cliente`
  - Nomes de funções: `enviar_para_openai()`, `processar_documentos()`
  - Nomes de métodos: `extrair_json_da_resposta()`, `obter_prompts()`
  - Nomes de arquivos: `openai_service.py`, `document_service.py`

### Estrutura e Organização

- Use nomes descritivos e significativos para variáveis e funções
- Evite abreviações desnecessárias (exceto convenções estabelecidas como `cfg`, `resp`)
- Prefira clareza sobre brevidade
- Utilize sempre verbo de ação, quando possivel, no imperativo (Ex. Validar, Obter, Definir)

## Configuração do Ambiente

### Variáveis de Ambiente

- Use `python-dotenv` para carregar variáveis de ambiente
- Mantenha chaves de API seguras (nunca no código)
- Use `pydantic-settings` para configurações tipadas

### Desenvolvimento Local

- Use `uv run uvicorn sky_ia_api:app --host 0.0.0.0 --port 8000 --reload --workers 1 --log-level info --use-colors` para desenvolvimento
- Configure hot-reload para desenvolvimento eficiente

### Exemplo de Boas Práticas:

```python
# ✅ BOM - FastAPI com type hints e documentação
@router.post("/processar_documentos")
async def processar_documentos_usuario(
    openai_api_key: str = Form(..., description="Chave da API OpenAI"),
    arquivos_upload: List[UploadFile] = File(..., description="Documentos para análise")
) -> QualificacaoResponse:
    log(f"Processando {len(arquivos_upload)} documentos")
    resultado_processamento = await process_uploaded_files(arquivos_upload, openai_api_key)
    return resultado_processamento

# ❌ EVITAR - Sem type hints e documentação
def procDocs(key, files):
    r = process(files, key)
    return r
```

## Estrutura de Projeto FastAPI

### Organização de Diretórios

```
/
├── pyproject.toml
├── README.md
├── .env.example
├── src/
│   └── app/                # pacote principal da aplicação
│       ├── __init__.py
│       ├── main.py         # instancia FastAPI + include_routers
│       ├── core/           # configuração e utilidades centrais
│       │   ├── __init__.py
│       │   ├── config.py   # settings via pydantic.BaseSettings
│       │   └── security.py # auth, JWT, OAuth2 helpers
│       ├── models/         # modelos de domínio (DB) e pydantic
│       │   ├── __init__.py
│       │   ├── user.py
│       │   └── item.py
│       ├── services/       # regras de negócio / casos de uso
│       │   ├── __init__.py
│       │   └── user_service.py
│       ├── repositories/   # abstrações de persistência (DAO)
│       │   ├── __init__.py
│       │   └── user_repo.py
│       ├── routers/        # controladores (camada API)
│       │   ├── __init__.py
│       │   ├── user_router.py
│       │   └── item_router.py
│       ├── schemas/        # modelos pydantic de entrada/saída
│       │   ├── __init__.py
│       │   ├── user_schema.py
│       │   └── item_schema.py
│       ├── tasks/          # jobs assíncronos / Celery / RQ
│       │   └── send_email.py
│       ├── helpers/        # funções utilitárias genéricas
│       │   ├── __init__.py
│       │   └── slugify.py
│       ├── templates/      # Jinja2 HTML (quando usar server-side)
│       │   └── emails/
│       │       └── welcome.html.jinja
│       └── static/         # arquivos estáticos (CSS, JS, imagens)
│           ├── css/
│           │   └── style.css
│           └── js/
│               └── main.js
├── tests/                  # pytest espelhando src/app
│   ├── __init__.py
│   ├── conftest.py
│   └── routers/
│       └── test_user.py
└── docker/
    └── Dockerfile
```

### Justificativa de cada diretório

- core/ Configurações globais, inicialização de extensões, segurança.
- models/ Entidades de domínio (ORM ou SQLModel) sem lógica pesada.
- schemas/ Objetos Pydantic usados em request/response.
- services/ Camada de negócio (application service / use case). Mantém regras isoladas dos frameworks.
- repositories/ Interface de persistência; possibilita troca de banco ou mock em testes.
- routers/ Endpoints FastAPI. Cada arquivo agrupa rotas por contexto de domínio.
- helpers/ Funções genéricas (slug, hashing, utils de data).
- templates/ HTML Jinja2 para emails ou páginas simples.
- static/ Recursos front-end (CSS, JS, imagens).
- tasks/ Processamento assíncrono (Celery, RQ, APScheduler).
- tests/ Espelha a estrutura do código; facilita descoberta automática do pytest.

### Padrões de Rotas FastAPI

- Use `APIRouter` para organizar endpoints por funcionalidade
- Defina prefixos e tags para agrupamento lógico
- Sempre inclua `summary` e `description` nos endpoints
- Use type hints em todos os parâmetros e retornos

### Exemplo de Estrutura de Rota:

```python
router = APIRouter(prefix="/qualificacao", tags=["qualificacao"])

@router.post(
    "",
    response_model=QualificacaoResponse,
    summary="Descrição concisa do endpoint",
    description="Descrição detalhada com exemplos"
)
async def nome_funcao_descritiva(
    parametro_obrigatorio: str = Form(..., description="Descrição do parâmetro"),
    arquivo_opcional: UploadFile = File(None, description="Arquivo opcional")
):
    # Implementação
    pass
```

### Imports e Dependências

- Organize imports seguindo PEP 8
- Use imports absolutos quando possível
- Agrupe imports: stdlib, terceiros, locais
- Exemplo de ordem:

```python
# Biblioteca padrão
import json
import logging
from typing import List, Dict, Any

# Terceiros
from fastapi import APIRouter, HTTPException
from openai import OpenAI
from pydantic import BaseModel

# Locais
from models.qualificacao import QualificacaoRequest
from services.openai_service import enviar_para_openai
```

## Modelos Pydantic

### Convenções para Modelos

- Use sufixos descritivos: `Request`, `Response`, `Config`
- Defina validações específicas quando necessário
- Use `Field()` para documentação e validação avançada
- Exemplo:

```python
class QualificacaoRequest(BaseModel):
    openai_api_key: str = Field(..., description="Chave da API OpenAI")
    documentos: List[str] = Field(..., description="Lista de documentos")

    class Config:
        json_schema_extra = {
            "example": {
                "openai_api_key": "sk-...",
                "documentos": ["documento1.pdf"]
            }
        }
```

## Integração com OpenAI

### Padrões para Serviços OpenAI

- Use funções específicas para cada tipo de operação
- Implemente tratamento de erros robusto
- Use logging para rastreabilidade
- Exemplo de função:

```python
def enviar_para_openai(
    openai_api_key: str,
    contents: List[dict],
    alias: str,
    expected_format: str = "text"
) -> Any:
    # Implementação com tratamento de erros
    pass
```

## Logging e Monitoramento

### Padrões de Logging

- Use a função `log()` padronizada do projeto
- Registre operações importantes e erros
- Use logger do uvicorn para consistência

```python
def log(message: str):
    logger = logging.getLogger("uvicorn")
    logger.info(message)
```

### Comentários e Documentação

- Escreva comentários em português brasileiro
- Use docstrings em português para funções e classes usando padrão Google
- Documente endpoints FastAPI com `summary` e `description`
- Explique o "porquê", não apenas o "o que"

### Tratamento de Erros

- Use `HTTPException` para erros de API
- Implemente logging adequado em português
- Trate erros específicos da OpenAI separadamente
- Exemplo:

```python
try:
    resultado = client.chat.completions.create(...)
except OpenAIError as e:
    log(f"Erro na OpenAI: {str(e)}")
    raise HTTPException(500, "Erro ao processar com IA")
```
