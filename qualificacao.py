
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

import base64, json, requests, rich
from rich.markdown import Markdown


URL = "http://127.0.0.1:8000/qualificacao"
API_KEY = "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"


doc1_b64 = base64.b64encode(open("doc1.png", "rb").read()).decode("ascii")
doc2_b64 = base64.b64encode(open("doc2.png", "rb").read()).decode("ascii")
doc3_b64 = base64.b64encode(open("luz.pdf", "rb").read()).decode("ascii")

payload = {
    "openai_api_key": API_KEY,
    "documents": [
        {"filename": "doc1.png", "base64": doc1_b64, "mime_type": "image/png"},
        {"filename": "doc2.png", "base64": doc2_b64, "mime_type": "image/png"},
        {"filename": "luz.pdf", "base64": doc3_b64, "mime_type": "application/pdf"},
    ],
}

response = requests.request("POST",
    URL,
    headers={"Content-Type": "application/json", "Accept": "application/json"},
    data=json.dumps(payload),
)

rich.print(Markdown(response.json().get("resposta")))
