# services/document_service.py
import base64
from typing import List, Dict, Any
from fastapi import HTTPException, UploadFile
from models.base import Document, DocumentRequest
from services.openai_service import enviar_para_openai, extrair_json_da_resposta, extrair_json_da_resposta_schema, log
import json

def process_documents(request: DocumentRequest, alias: str, expected_format: str = "text") -> Dict[str, Any]:
    """
    Processa documentos enviados e envia para a OpenAI.
    
    Args:
        request: Objeto DocumentRequest contendo os documentos e a chave da API
        alias: Alias do prompt a ser usado
        expected_format: Formato esperado da resposta ("text" ou "json")
        
    Returns:
        Dict: Resposta processada da OpenAI
    """
    if not request.documents:
        raise HTTPException(400, "A lista de documentos está vazia.")

    contents = []
    for doc in request.documents:
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

    # Envia para a OpenAI
    response = enviar_para_openai(
        openai_api_key=request.openai_api_key,
        contents=contents,
        alias=alias,
        expected_format=expected_format
    )
    
    # Processa a resposta de acordo com o formato esperado
    if expected_format == "json":
        try:
            output_json = extrair_json_da_resposta_schema(response)
            log(f"JSON extraído com sucesso: {json.dumps(output_json)[:100]}...")
            return output_json
        except Exception as e:
            log(f"Falha ao extrair JSON (schema): {str(e)}")
            raise HTTPException(502, "Resposta da OpenAI não contém JSON válido no formato esperado.")
    else:
        try:
            output_json = extrair_json_da_resposta(response)
            log(f"JSON extraído com sucesso: {json.dumps(output_json)[:100]}...")
            return output_json
        except json.JSONDecodeError as e:
            log(f"Erro ao decodificar JSON: {str(e)}")
            log(f"Texto da resposta: {response[:200]}...")
            raise HTTPException(500, "Erro ao decodificar a resposta da OpenAI como JSON.")

async def process_uploaded_files(openai_api_key: str, files: List[UploadFile]) -> List[Document]:
    """
    Processa arquivos enviados via upload e converte para o formato Document.
    
    Args:
        openai_api_key: Chave da API da OpenAI
        files: Lista de arquivos enviados
        
    Returns:
        List[Document]: Lista de documentos processados
    """
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

    return documentos