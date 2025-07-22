#!/usr/bin/env bash
# qualificacao.sh
# Este exemplo mostra como enviar documentos para a rota de qualificação
# do endpoint de qualificação, que aceita documentos via JSON.

# exemplo payload para a rota de qualificação
#{
#  "openai_api_key": "sk-...",
#  "documents": [
#    {
#      "base64": "<string>",
#      "mime_type": "image/png"
#    },
#    {
#      "base64": "<string>",
#      "mime_type": "application/pdf",
#      "filename": "contrato.pdf"
#    }
#  ]
#}

set -euo pipefail
set -x

API_URL="${SKY_API_URL:-http://127.0.0.1:8000}"
OPENAI_API_KEY="${SKY_OPENAI_KEY:?Variável SKY_OPENAI_KEY não definida}"

b64() { openssl base64 -A -in "$1"; }

doc1_b64=$(b64 doc1.png)
doc2_b64=$(b64 doc2.png)
doc3_b64=$(b64 luz.pdf)

cat > payload.json <<EOF
{
  "openai_api_key": "${OPENAI_API_KEY}",
  "documents": [
    { "filename": "doc1.png", "base64": "${doc1_b64}", "mime_type": "image/png" },
    { "filename": "luz.pdf",  "base64": "${doc3_b64}", "mime_type": "application/pdf" }
  ]
}
EOF


echo "Enviando documentos para $API_URL/qualificacao"

curl -v -X POST "${API_URL%/}/qualificacao" \
     -H "Content-Type: application/json" \
     --data @payload.json 

