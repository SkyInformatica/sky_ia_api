import os
import base64
import json
import sys
import time
from pathlib import Path
from openai import OpenAI
from rich import print as rprint
from rich.markdown import Markdown
from typing import List, Optional, Dict, Any

# Adiciona o diretório raiz do projeto ao path para importar módulos
sys.path.append(str(Path(__file__).parent.parent))
from src.app.services.openai_service import extrair_json_da_resposta_schema

# ------------------------------------------------------------------------------
# 1. Autenticação
# ------------------------------------------------------------------------------
api_key = os.getenv("SKY_OPENAI_KEY")
if not api_key:
    raise ValueError(
        "SKY_OPENAI_KEY não foi definida. Exporte a variável de ambiente:\n"
        "  export SKY_OPENAI_KEY='seu_token'"
    )

client = OpenAI(api_key=api_key)

# ------------------------------------------------------------------------------
# 2. Utilitário para codificar arquivos em Base64
# ------------------------------------------------------------------------------
def b64(path: str) -> str:
    path = Path(path)
    with path.open("rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")
    
# ------------------------------------------------------------------------------
# 3. Arquivos que serão enviados
# ------------------------------------------------------------------------------
pdfs  = ["../docs/escritura_publica/escritura-aliencacao-fiduciaria.pdf"]

pdfs_b64 = [b64(i) for i in pdfs]

# ------------------------------------------------------------------------------
# 4. Montagem do payload usando o SDK
# ------------------------------------------------------------------------------
start_time = time.time()
response = client.responses.create(
    prompt={
        "id": "pmpt_68876a48fe8c819695a7e8705a7aadc9073a6c6d9c2e8e9d",
    },
    input=[
        {
            "role": "user",
            "content": [                
                *(
                    {
                        "type": "input_file",
                        "file_data": f"data:application/pdf;base64,{pdf_b64}",
                        "filename": "doc.pdf",
                    }
                    for pdf_b64 in pdfs_b64
                ),
            ],
        }
    ],    
    max_output_tokens=8196,
    store=False,
)
elapsed_time = time.time() - start_time
print(f"Tempo de execução do client.responses.create(): {elapsed_time:.2f} segundos")

# ------------------------------------------------------------------------------
# 5. Saída
# ------------------------------------------------------------------------------
data = response.model_dump()
print(json.dumps(data, indent=2, ensure_ascii=False))

print("\n\n\nresposta em json:\n")
response_json = extrair_json_da_resposta_schema(data);     
print(json.dumps(response_json, indent=2, ensure_ascii=False))
