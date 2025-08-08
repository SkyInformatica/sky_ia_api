#!/usr/bin/env bash
# Envia arquivos via multipart para /qualificacao

set -euo pipefail

# Configurações
API_URL="${SKY_API_URL:-http://127.0.0.1:8000}"
OPENAI_API_KEY="${SKY_OPENAI_KEY:?Variável SKY_OPENAI_KEY não definida}"

curl -v -X POST "${API_URL%/}/qualificacao" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "chave_api_openai=${OPENAI_API_KEY}" \
  -F arquivos=@doc1.png \
  -F arquivos=@doc2.png \
  -F arquivos=@luz.pdf
