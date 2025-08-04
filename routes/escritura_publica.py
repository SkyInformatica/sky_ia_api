# routes/escritura_publica.py
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import List
from models.escritura_publica import EscrituraPublicaRequest, EscrituraPublicaResponse
from services.document_service import process_documents, process_uploaded_files

router = APIRouter(prefix="/escritura_publica", tags=["escritura_publica"])

@router.post(
    "",
    response_model=EscrituraPublicaResponse,
    summary="Extração de dados de escritura pública via upload de arquivos",
    description="""
    Endpoint para extração de dados de escritura pública através de upload direto de arquivos.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Este endpoint aceita requisições multipart/form-data, facilitando o upload 
    direto de arquivos sem a necessidade de codificação prévia em base64.
    
    Tipos de documentos que podem ser utilizados: Escritura Pública lavrada em Tabelionato de Notas
    """
)
async def escritura_publica_upload(
    openai_api_key: str = Form(..., description="Chave de API válida da OpenAI"),
    files: List[UploadFile] = File(..., description="Arquivos para análise (PNG, JPEG/JPG, PDF)")
) -> EscrituraPublicaResponse:
    """
    Processa arquivos enviados diretamente para análise de escritura pública.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        EscrituraPublicaResponse: Objeto contendo a resposta da análise
    """
    # Processa os arquivos enviados
    documentos = await process_uploaded_files(openai_api_key, files)
    
    # Cria o objeto de requisição
    req = EscrituraPublicaRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    
    # Processa os documentos e obtém a resposta
    output_json = process_documents(req, alias="escritura_publica", expected_format="json")
    
    # Constrói e retorna o objeto EscrituraPublicaResponse com o JSON completo
    # Passando diretamente o JSON retornado pela OpenAI, sem o atributo "resposta"
    return EscrituraPublicaResponse(**output_json)