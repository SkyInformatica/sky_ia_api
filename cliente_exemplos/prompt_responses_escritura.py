import os
import base64
import json
from pathlib import Path
from openai import OpenAI
from rich import print as rprint
from rich.markdown import Markdown

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
pdfs  = ["escritura-aliencacao-fiduciaria.pdf"]

pdfs_b64 = [b64(i) for i in pdfs]

# ------------------------------------------------------------------------------
# 4. Montagem do payload usando o SDK
# ------------------------------------------------------------------------------
response = client.responses.create(
    prompt={
        "id": "pmpt_687f9ebb50388193b1f7f0b667076dc00fbc998c46e42ab6",
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
    reasoning={},
    max_output_tokens=8196,
    store=True,
)

# ------------------------------------------------------------------------------
# 5. Saída
# ------------------------------------------------------------------------------
print(json.dumps(response.model_dump(), indent=2, ensure_ascii=False))
#print("\n\n\nmarkdown output:\n")
      

output_text = response.output[0].content[0].text
rprint(Markdown(output_text))

# Extraindo o conteúdo do atributo "resposta_processamento_markdown"
output_text = response.output[0].content[0].text

# Removendo a tag ```json e convertendo a string JSON em um dicionário
output_json = json.loads(output_text.strip("```json ").strip("```"))

# Pegando o conteúdo do atributo "resposta_processamento_markdown"
markdown_content = output_json.get("resposta_processamento_markdown", "")

# Formatando e imprimindo o conteúdo em Markdown
rprint(Markdown(markdown_content))

# Removendo a chave "resposta_processamento_markdown" do output_json
output_json.pop("resposta_processamento_markdown", None)

# Imprimindo o conteúdo restante de output_json formatado e colorido
rprint(output_json)


