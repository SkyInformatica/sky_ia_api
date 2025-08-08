# Configuração do Trae para Navegação de Código

Este documento explica como configurar adequadamente o Trae AI para navegação de código no projeto Sky IA API.

## Problema Resolvido

O problema de "go to definition" não funcionar no Trae geralmente ocorre devido a:

1. **Falta de configuração do Language Server Protocol (LSP)**
2. **Caminhos de módulos Python não configurados corretamente**
3. **Ambiente virtual não reconhecido pelo IDE**

## Arquivos de Configuração Criados

### 1. `pyrightconfig.json`

Arquivo de configuração do Pyright (Language Server para Python) que:
- Define o caminho correto dos módulos (`src`)
- Configura a versão do Python (3.13)
- Habilita indexação e auto-importação
- Define regras de type checking

### 2. `.vscode/settings.json`

Configurações específicas do workspace que:
- Define o caminho do interpretador Python (`./.venv/bin/python`)
- Configura caminhos extras para análise (`./src`)
- Habilita indexação automática
- Define configurações de linting e formatação

### 3. `.python-version`

Especifica a versão exata do Python (3.13.5) para ferramentas que dependem desta informação.

## Como Verificar se Está Funcionando

1. **Reinicie o Trae** após aplicar as configurações
2. **Aguarde a indexação** (pode levar alguns segundos)
3. **Teste a navegação**:
   - Clique com botão direito em `processar_arquivos_upload`
   - Selecione "Go to Definition"
   - Deve navegar para `src/app/services/document_service.py:75`

## Comandos de Verificação

```bash
# Verificar se o ambiente está correto
uv run python --version

# Verificar se a importação funciona
uv run python -c "from src.app.services.document_service import processar_arquivos_upload; print('OK')"

# Sincronizar dependências
uv sync
```

## Estrutura de Imports

O projeto usa imports relativos a partir da pasta `src`:

```python
# No arquivo qualificacao_router.py
from ..services.document_service import processar_arquivos_upload
```

A função está definida em:
- **Arquivo**: `src/app/services/document_service.py`
- **Linha**: 75
- **Função**: `async def processar_arquivos_upload(chave_api_openai: str, arquivos: List[UploadFile]) -> List[Documento]`

## Dicas Adicionais

1. **Cache do LSP**: Se ainda não funcionar, tente fechar e reabrir o arquivo
2. **Indexação**: Aguarde alguns segundos após abrir o projeto para a indexação completa
3. **Logs**: Verifique os logs do Trae para mensagens de erro do Language Server
4. **Dependências**: Certifique-se de que todas as dependências estão instaladas com `uv sync`

## Troubleshooting

Se o "go to definition" ainda não funcionar:

1. Verifique se o arquivo `pyrightconfig.json` está na raiz do projeto
2. Confirme que o ambiente virtual está ativo
3. Reinicie completamente o Trae
4. Verifique se não há erros de sintaxe nos arquivos Python

## Comandos Úteis

```bash
# Verificar estrutura do projeto
find src -name "*.py" | head -10

# Verificar imports
uv run python -c "import sys; print('\n'.join(sys.path))"

# Testar navegação programaticamente
uv run python -c "import inspect; from src.app.services.document_service import processar_arquivos_upload; print(inspect.getfile(processar_arquivos_upload))"
```

Com essas configurações, o Trae deve conseguir navegar corretamente entre as definições de funções e classes no projeto.