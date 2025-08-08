#!/usr/bin/env python3
"""Envia arquivos via multipart para /escritura_publica
   Usa variáveis de ambiente:
     SKY_API_URL     – URL base da API
     SKY_OPENAI_KEY  – chave OpenAI
"""

import os
import sys
import json
import requests
from rich import print as rprint
from rich.markdown import Markdown

API_URL = os.getenv("SKY_API_URL", "http://127.0.0.1:8000").rstrip("/")
API_KEY = os.getenv("SKY_OPENAI_KEY")

if not API_KEY:
    sys.exit("❌  Defina a variável de ambiente SKY_OPENAI_KEY")

url = f"{API_URL}/escritura_publica"
payload = {"chave_api_openai": API_KEY}

files = [
    ("arquivos", ("escritura-aliencacao-fiduciaria.pdf", open("../docs/escritura_publica/escritura-aliencacao-fiduciaria.pdf", "rb"), "application/pdf")),
]

resp = requests.post(url, data=payload, files=files, timeout=300)
print(resp)

#print(json.dumps(resp, indent=2, ensure_ascii=False))
#print("\n\n\nresposta_processamento_markdown:\n")

# Pegando o conteúdo do atributo "resposta_processamento_markdown"
#markdown_content = resp.get("resposta_processamento_markdown", "")

# Formatando e imprimindo o conteúdo em Markdown
#rprint(Markdown(markdown_content))






