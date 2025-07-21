#!/usr/bin/env bash
# arquivo: qualificacao.sh

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

API_URL="http://127.0.0.1:8000/qualificacao"
OPENAI_API_KEY="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"

# Converte cada arquivo para Base64 (linha única)
doc1_b64=$(openssl base64 -A -in doc1.png)
doc2_b64=$(openssl base64 -A -in doc2.png)
doc3_b64=$(openssl base64 -A -in luz.pdf)


# --- Monta JSON num subshell cat <<EOF ---
payload=$(cat <<EOF
{
  "openai_api_key": "$OPENAI_API_KEY",
  "documents": [
    { "base64": "$doc1_b64", "mime_type": "image/png" },
    { "base64": "$doc2_b64", "mime_type": "image/png" }
    { "base64": "$doc3_b64", "mime_type": "application/pdf", "filename": "luz.pdf" }
  ]
}
EOF
)

# Envia a requisição
#curl -X POST "$API_URL" \
#     -H "Content-Type: application/json" \
#     -d "$payload"

curl -sS -w '\nStatus: %{http_code}\n' \
     -H "Content-Type: application/json" \
     -d "$payload" \
     "$API_URL"
