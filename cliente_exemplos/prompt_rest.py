import base64
import json
import requests
import rich
from rich.markdown import Markdown

# OpenAI API Key
api_key = "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"

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

# Path to your image
image1 = "doc1.png"
image2 = "doc2.png"
image3 = "doc3.png"
image4 = "doc4.png"

# Getting the base64 string
image1_base64 = encode_image(image1)
image2_base64 = encode_image(image2)
image3_base64 = encode_image(image3)
image4_base64 = encode_image(image4)

headers = {
  "Content-Type": "application/json",
  "Authorization": f"Bearer {api_key}"
}

payload = {
    "prompt": {
        "id": "pmpt_68785396f76c8193a6a40e2933b0f0830787678b3fa557b7",               
        "version": "2"
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
print("markdown output:")
rich.print(Markdown(output_text))

