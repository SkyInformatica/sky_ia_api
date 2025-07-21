# sky_ia_api.py
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel
from typing import List, Optional
import base64

from openai import OpenAI, OpenAIError
from config import get_prompts          # ← continua

app = FastAPI(title="Qualificação API", version="0.6")


# ---------------------- MODELOS ---------------------------------------------
class Document(BaseModel):
    base64: str
    mime_type: str
    filename: Optional[str] = None

class QualificacaoRequest(BaseModel):
    openai_api_key: str
    documents: List[Document]


# ------------------ Função que fala com a OpenAI ----------------------------
def enviar_para_openai(
    openai_api_key: str,
    contents: List[dict],
    alias: str                           
):
    prompt_cfg = get_prompts().get(alias)
    if not prompt_cfg:
        raise HTTPException(
            500, f"Alias de prompt não encontrado em prompts.yaml: {alias}"
        )

    client = OpenAI(api_key=openai_api_key)
    try:
        response = client.responses.create(
            prompt={
                "id": prompt_cfg["id"],
                "version": str(prompt_cfg["version"])
            },
            input=[{"role": "user", "content": contents}],
            reasoning={},
            max_output_tokens=2048,
            store=True
        )
    except OpenAIError as err:
        raise HTTPException(
            502,
            detail={"msg": "Erro retornado pela OpenAI SDK", "openai_error": str(err)}
        )

    data = response.model_dump()
    try:
        text = data["output"][0]["content"][0]["text"]
    except (KeyError, IndexError, TypeError):
        raise HTTPException(502, "Estrutura inesperada na resposta da OpenAI")

    return {"resposta": text}
# ---------------------------------------------------------------------------


# ----------------------- Endpoint JSON --------------------------------------
@app.post("/qualificacao")
def qualificacao_json(body: QualificacaoRequest):
    if not body.documents:
        raise HTTPException(400, "A lista de documentos está vazia.")

    contents = []
    for doc in body.documents:
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

    # alias fixo para esta rota
    return enviar_para_openai(
        openai_api_key=body.openai_api_key,
        contents=contents,
        alias="qualificacao"        
    )
# ---------------------------------------------------------------------------


# ------------- Endpoint multipart (reutiliza a mesma lógica) ---------------
@app.post("/qualificacao/upload")
async def qualificacao_upload(
    openai_api_key: str = Form(...),
    files: List[UploadFile] = File(...)
):
    if not files:
        raise HTTPException(400, "Nenhum arquivo enviado.")

    documentos: List[Document] = []
    for file in files:
        raw = await file.read()
        if not raw:
            continue

        mime = (file.content_type or "").lower()
        if mime not in ("image/png", "image/jpeg", "image/jpg", "application/pdf"):
            raise HTTPException(400, f"Tipo de arquivo não suportado: {mime}")

        b64 = base64.b64encode(raw).decode()
        filename = file.filename if mime == "application/pdf" else None
        documentos.append(Document(base64=b64, mime_type=mime, filename=filename))

    req = QualificacaoRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    # reutiliza a lógica da rota JSON, que já define o alias
    return qualificacao_json(req)
# ---------------------------------------------------------------------------
