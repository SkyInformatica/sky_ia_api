"""Router para endpoints de escritura pública.

Este módulo contém os endpoints da API relacionados à
extração de dados de escrituras públicas.
"""

# Biblioteca padrão
from typing import List

# Terceiros
from fastapi import APIRouter, File, Form, UploadFile

# Locais
from ..schemas.escritura_publica_schema import EscrituraPublicaRequest, EscrituraPublicaResponse
from ..services.document_service import processar_documentos, processar_arquivos_upload


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
async def extrair_dados_escritura_publica_upload(
    chave_api_openai: str = Form(
        ..., 
        description="Chave de API válida da OpenAI"
    ),
    arquivos: List[UploadFile] = File(
        ..., 
        description="Arquivos para análise (PNG, JPEG/JPG, PDF)"
    )
) -> EscrituraPublicaResponse:
    """Processa arquivos enviados diretamente para análise de escritura pública.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Args:
        chave_api_openai: Chave de API da OpenAI
        arquivos: Lista de arquivos para análise
        
    Returns:
        EscrituraPublicaResponse: Objeto contendo a resposta da análise
    """
    # Processa os arquivos enviados
    documentos = await processar_arquivos_upload(chave_api_openai, arquivos)
    
    # Cria o objeto de requisição
    requisicao = EscrituraPublicaRequest(
        chave_api_openai=chave_api_openai,
        documentos=documentos
    )
    
    # Processa os documentos e obtém a resposta
    json_saida = processar_documentos(requisicao, alias="escritura_publica")
    
    # Constrói e retorna o objeto EscrituraPublicaResponse com o JSON completo
    # Passando diretamente o JSON retornado pela OpenAI
    return EscrituraPublicaResponse(**json_saida)