import base64
import json
import requests
import rich
from rich.markdown import Markdown
import os

# OpenAI API Key
api_key = os.getenv("SKY_OPENAI_KEY", "")
if not api_key:
    raise ValueError("SKY_OPENAI_KEY nao foi definda. Defina a variável de ambiente com export SKY_OPENAI_KEY=...")

# Function to encode the image
def encode_b64(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image1 = "doc1.png"
image2 = "doc2.png"
image3 = "doc3.png"
image4 = "doc4.png"
doc1 = "luz.pdf"


# Getting the base64 string
image1_base64 = encode_b64(image1)
image2_base64 = encode_b64(image2)
image3_base64 = encode_b64(image3)
image4_base64 = encode_b64(image4)
doc1_base64 = encode_b64(doc1)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
    "prompt": {
        "id": "pmpt_687d830e2d28819697ff506d530cfd0103574d5ce096ea5e",              
    },
    "input": [
        {
            "role": "user",
            "content": [
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image1_base64}"
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image2_base64}"
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image3_base64}"
                },
                {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{image4_base64}"
                },
                {
                    "type": "input_file",
                    "file_data": f"data:application/pdf;base64,{doc1_base64}",
                    "filename": "doc1.pdf"
                }
            ]
        },    
    ],
    "reasoning": {},
    "max_output_tokens": 2048,
    "store": True  
}

response = requests.post("https://api.openai.com/v1/responses", headers=headers, json=payload)

print(json.dumps(response.json(), indent=2, ensure_ascii=False))

output_text = response.json()["output"][0]["content"][0]["text"]

#output_json = json.loads(output_text)
#print(json.dumps(output_json, indent=2, ensure_ascii=False))


rich.print(Markdown(output_text))

