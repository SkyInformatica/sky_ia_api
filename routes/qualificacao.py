# routes/qualificacao.py
from fastapi import APIRouter, HTTPException, File, Form, UploadFile
from typing import List
from models.qualificacao import QualificacaoRequest, QualificacaoResponse
from services.document_service import process_documents, process_uploaded_files

router = APIRouter(prefix="/qualificacao", tags=["qualificacao"])

@router.post(
    "",
    response_model=QualificacaoResponse,
    summary="Qualificação de documentos via upload de arquivos",
    description="""
    Endpoint para qualificação de documentos através de upload dos arquivos.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Este endpoint aceita requisições multipart/form-data, facilitando o upload 
    direto de arquivos sem a necessidade de codificação prévia em base64.
    
    Tipos de documentos que podem ser utilizados: RG, CNH, Comprovante de residencia, 
    Conta de luz, Conta de agua, Certidão de casamento, Certidão de nascimento, 
    Certidão de obito, Pacto antenupcial, etc...
    """
)
async def qualificacao_upload(
    openai_api_key: str = Form(..., description="Chave de API válida da OpenAI"),
    files: List[UploadFile] = File(..., description="Arquivos para análise (PNG, JPEG/JPG, PDF)")
) -> QualificacaoResponse:
    """
    Processa arquivos enviados diretamente para análise e qualificação.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        QualificacaoResponse: Objeto contendo a resposta da análise
    """
    # Processa os arquivos enviados
    documentos = await process_uploaded_files(openai_api_key, files)
    
    # Cria o objeto de requisição
    req = QualificacaoRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    
    # Processa os documentos e obtém a resposta
    output_json = process_documents(req, alias="qualificacao")
    
    # Constrói e retorna o objeto QualificacaoResponse com o JSON completo
    return QualificacaoResponse(resposta=output_json)