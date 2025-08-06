"""Router para endpoints de qualificação de documentos.

Este módulo contém os endpoints da API relacionados à
qualificação e análise de documentos pessoais.
"""

# Biblioteca padrão
from typing import List

# Terceiros
from fastapi import APIRouter, File, Form, UploadFile, HTTPException

# Locais
from ..schemas.qualificacao_schema import QualificacaoRequest, QualificacaoResponse
from ..services.document_service import processar_documentos, processar_arquivos_upload


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
    
    Tipos de documentos que podem ser utilizados: RG, CNH, Comprovante de residência, 
    Conta de luz, Conta de água, Certidão de casamento, Certidão de nascimento, 
    Certidão de óbito, Pacto antenupcial, etc...
    """
)
async def qualificar_documentos_upload(
    chave_api_openai: str = Form(
        ..., 
        description="Chave de API válida da OpenAI"
    ),
    arquivos: List[UploadFile] = File(
        ..., 
        description="Arquivos para análise (PNG, JPEG/JPG, PDF)"
    )
) -> QualificacaoResponse:
    """Processa arquivos enviados diretamente para análise e qualificação.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Args:
        chave_api_openai: Chave de API da OpenAI
        arquivos: Lista de arquivos para análise
        
    Returns:
        QualificacaoResponse: Objeto contendo a resposta da análise
    """
    try:
        # Processa os arquivos enviados
        documentos = await processar_arquivos_upload(chave_api_openai, arquivos)
        
        # Cria o objeto de requisição
        requisicao = QualificacaoRequest(
            chave_api_openai=chave_api_openai,
            documentos=documentos
        )
        
        # Processa os documentos e obtém a resposta usando schema JSON
        json_saida = processar_documentos(requisicao, alias="qualificacao")
        
        # Retorna diretamente o JSON da OpenAI como QualificacaoResponse
        return QualificacaoResponse(**json_saida)
        
    except ValueError as e:
        # Erros de validação ou tipos de arquivo não suportados
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        # Outros erros (OpenAI, etc.)
        raise HTTPException(status_code=500, detail="Erro interno do servidor")