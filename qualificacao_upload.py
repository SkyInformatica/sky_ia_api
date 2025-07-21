#curl -X POST http://127.0.0.1:8000/qualificacao/upload \
#  -H "accept: application/json" \
#  -H "Content-Type: multipart/form-data" \
#  -F openai_api_key="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" \
#  -F files=@doc1.png \
#  -F files=@doc2.png

import requests, rich
from rich.markdown import Markdown

url = "http://127.0.0.1:8000/qualificacao/upload"

payload = {'openai_api_key': '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'}
files=[
  ('files',('doc1.png',open('doc1.png','rb'),'image/png')),
  ('files',('doc2.png',open('doc2.png','rb'),'image/png')),
  ('files',('luz.pdf',open('luz.pdf','rb'),'application/pdf'))  
]
headers = {
  'Accept': 'application/json'  
}

response = requests.request("POST", url, headers=headers, data=payload, files=files)

rich.print(Markdown(response.json().get("resposta")))
