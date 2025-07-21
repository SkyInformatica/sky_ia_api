# qualificacao.sh
# Este exemplo mostra como enviar documentos para a rota de qualificação
# do endpoint de qualificação, que aceita documentos via JSON.

#!/usr/bin/env bash

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

API_URL="${SKY_API_URL:-http://127.0.0.1:8000}"
OPENAI_API_KEY="${SKY_OPENAI_KEY:?Variável SKY_OPENAI_KEY não definida}"

b64() { openssl base64 -A -in "$1"; }

doc1_b64=$(b64 doc1.png)
doc2_b64=$(b64 doc2.png)
doc3_b64=$(b64 luz.pdf)

read -r -d '' payload <<EOF
{
  "openai_api_key": "$OPENAI_API_KEY",
  "documents": [
    { "filename": "doc1.png", "base64": "$doc1_b64", "mime_type": "image/png" },
    { "filename": "doc2.png", "base64": "$doc2_b64", "mime_type": "image/png" },
    { "filename": "luz.pdf",  "base64": "$doc3_b64", "mime_type": "application/pdf" }
  ]
}
EOF

curl -sS -w '\nStatus: %{http_code}\n' \
     -H "Content-Type: application/json" \
     -d "$payload" \
     "${API_URL%/}/qualificacao"
