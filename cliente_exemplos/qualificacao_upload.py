#!/usr/bin/env python3
"""Envia arquivos via multipart para /qualificacao/upload
   Usa variáveis de ambiente:
     SKY_API_URL     – URL base da API
     SKY_OPENAI_KEY  – chave OpenAI
"""

import os
import sys
import requests
from pathlib import Path

API_URL = os.getenv("SKY_API_URL", "http://127.0.0.1:8000").rstrip("/")
API_KEY = os.getenv("SKY_OPENAI_KEY")

if not API_KEY:
    sys.exit("❌  Defina a variável de ambiente SKY_OPENAI_KEY")

url = f"{API_URL}/qualificacao/upload"
payload = {"openai_api_key": API_KEY}

files = [
    ("files", ("doc1.png", open("doc1.png", "rb"), "image/png")),
    ("files", ("doc2.png", open("doc2.png", "rb"), "image/png")),
    ("files", ("luz.pdf", open("luz.pdf", "rb"), "application/pdf")),
]

resp = requests.post(url, data=payload, files=files, timeout=60)
resp.raise_for_status()

print(resp.json())
