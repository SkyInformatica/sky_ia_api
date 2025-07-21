#!/usr/bin/env bash
# Envia arquivos via multipart para /qualificacao/upload

set -euo pipefail

API_URL="${SKY_API_URL:-http://127.0.0.1:8000}"
OPENAI_API_KEY="${SKY_OPENAI_KEY:?Variável SKY_OPENAI_KEY não definida}"

curl -v -X POST "${API_URL%/}/qualificacao/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "openai_api_key=${OPENAI_API_KEY}" \
  -F files=@doc1.png \
  -F files=@doc2.png \
  -F files=@luz.pdf
