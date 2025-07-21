#!/usr/bin/env python3

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


"""Envia documentos em JSON para /qualificacao"""

import base64
import json
import os
import sys
import requests
from pathlib import Path

API_URL = os.getenv("SKY_API_URL", "http://127.0.0.1:8000").rstrip("/")
API_KEY = os.getenv("SKY_OPENAI_KEY")

if not API_KEY:
    sys.exit("❌  Defina a variável de ambiente SKY_OPENAI_KEY")

def to_b64(path: str) -> str:
    return base64.b64encode(Path(path).read_bytes()).decode("ascii")

payload = {
    "openai_api_key": API_KEY,
    "documents": [
        {"filename": "doc1.png", "base64": to_b64("doc1.png"), "mime_type": "image/png"},
        {"filename": "doc2.png", "base64": to_b64("doc2.png"), "mime_type": "image/png"},
        {"filename": "luz.pdf",  "base64": to_b64("luz.pdf"),  "mime_type": "application/pdf"},
    ],
}

resp = requests.post(
    f"{API_URL}/qualificacao",
    headers={"Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(payload),
    timeout=60,
)
resp.raise_for_status()
print(resp.json())
