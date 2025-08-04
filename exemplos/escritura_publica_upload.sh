#!/usr/bin/env bash
# Envia arquivos via multipart para /escritura_publica

set -euo pipefail

API_URL="${SKY_API_URL:-http://127.0.0.1:8000}"
OPENAI_API_KEY="${SKY_OPENAI_KEY:?Variável SKY_OPENAI_KEY não definida}"

curl -v -X POST "${API_URL%/}/escritura_publica" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "openai_api_key=${OPENAI_API_KEY}" \
  -F files=@escritura-aliencacao-fiduciaria.pdf
