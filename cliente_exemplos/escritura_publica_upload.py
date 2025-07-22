#!/usr/bin/env python3
"""Envia arquivos via multipart para /qualificacao/upload
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

url = f"{API_URL}/escritura_publica/upload"
payload = {"openai_api_key": API_KEY}

files = [
    ("files", ("escritura-aliencacao-fiduciaria.pdf", open("escritura-aliencacao-fiduciaria.pdf", "rb"), "application/pdf")),
]

resp = requests.post(url, data=payload, files=files, timeout=120)
resp.raise_for_status()

print(resp.json())

#output_json = resp.json().get("resposta", {})
#print(json.dumps(output_json, indent=2, ensure_ascii=False))
#print("\n\n\nresposta_processamento_markdown:\n")

# Pegando o conteúdo do atributo "resposta_processamento_markdown"
#markdown_content = output_json.get("resposta_processamento_markdown", "")

# Formatando e imprimindo o conteúdo em Markdown
#rprint(Markdown(markdown_content))

# Removendo a chave "resposta_processamento_markdown" do output_json
#output_json.pop("resposta_processamento_markdown", None)

#print("\n\n\noutput_json:\n")
# Imprimindo o conteúdo restante de output_json formatado e colorido
#rprint(output_json)







