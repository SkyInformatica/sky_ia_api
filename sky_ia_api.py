# sky_ia_api.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import base64

from openai import OpenAI, OpenAIError

app = FastAPI(title="Qualificação API", version="0.4")

# ------------------------- Configuração fixa --------------------------------
PROMPT_ID = "pmpt_68785396f76c8193a6a40e2933b0f0830787678b3fa557b7"
PROMPT_VERSION = "2"
# ---------------------------------------------------------------------------


# ---------------------- MODELOS (modo JSON) ---------------------------------
class Document(BaseModel):
    base64: str
    mime_type: str                    # image/png, image/jpeg ou application/pdf
    filename: Optional[str] = None    # usado só p/ PDF

class QualificacaoRequest(BaseModel):
    openai_api_key: str
    documents: List[Document]
# ---------------------------------------------------------------------------


# -------------------- Função que fala com a OpenAI --------------------------
def enviar_para_openai(openai_api_key: str, contents: List[dict]):
    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.responses.create(
            prompt={"id": PROMPT_ID, "version": PROMPT_VERSION},
            input=[{
                "role": "user",
                "content": contents
            }],
            reasoning={},
            max_output_tokens=2048,
            store=True
        )
    except OpenAIError as err:
        raise HTTPException(
            502,
            detail={"msg": "Erro retornado pela OpenAI SDK", "openai_error": str(err)}
        )
 
    # Converte para dict apenas uma vez
    resp_dict = response.model_dump()
    print(f"Resposta da OpenAI: {resp_dict}")

    try:
        text = (
            resp_dict["output"][0]          # primeira mensagem
                     ["content"][0]         # primeiro bloco
                     ["text"]               # texto
        )
    except (KeyError, IndexError, TypeError):
        raise HTTPException(
            502,
            detail={"msg": "Estrutura inesperada na resposta da OpenAI."}
        )
        
    return {"resposta": text}
# ---------------------------------------------------------------------------


# ----------------------- Endpoint JSON --------------------------------------
@app.post("/qualificacao", summary="Envia documentos já em base64 (JSON)")
def qualificacao_json(body: QualificacaoRequest):            # <= alterado
    if not body.documents:
        raise HTTPException(400, "A lista de documentos está vazia.")

    contents = []
    for doc in body.documents:                               # <= alterado
        mime = doc.mime_type.lower()
        if mime in ("image/png", "image/jpeg", "image/jpg"):
            contents.append({
                "type": "input_image",
                "image_url": f"data:{mime};base64,{doc.base64}"
            })
        elif mime == "application/pdf":
            contents.append({
                "type": "input_file",
                "filename": doc.filename or "documento.pdf",
                "file_data": f"data:application/pdf;base64,{doc.base64}"
            })
        else:
            raise HTTPException(400, f"MIME não suportado: {mime}")
    
    return enviar_para_openai(body.openai_api_key, contents) 
# ---------------------------------------------------------------------------


# ------------------ Endpoint multipart/form-data ---------------------------
@app.post("/qualificacao/upload", summary="Envia arquivos via multipart/form-data")
async def qualificacao_upload(
    openai_api_key: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(400, "Nenhum arquivo enviado.")

    documentos: List[Document] = []

    for file in files:
        data = await file.read()
        if not data:
            continue

        mime = (file.content_type or "").lower()
        if mime not in ("image/png", "image/jpeg", "image/jpg", "application/pdf"):
            raise HTTPException(400, f"Tipo de arquivo não suportado: {mime}")

        b64 = base64.b64encode(data).decode()
        filename = file.filename if mime == "application/pdf" else None

        documentos.append(Document(base64=b64, mime_type=mime, filename=filename))

    if not documentos:
        raise HTTPException(400, "Arquivos vazios ou não suportados.")

    # ---------- REUTILIZA A LÓGICA EXISTENTE ----------
    request_body = QualificacaoRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    return qualificacao_json(request_body)
# ---------------------------------------------------------------------------
