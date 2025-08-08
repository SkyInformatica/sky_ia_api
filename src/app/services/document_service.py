"""Serviço de processamento de documentos.

Este módulo contém as funções para processamento de documentos,
incluindo upload de arquivos e integração com OpenAI.
"""

import base64
from typing import List, Dict, Any
from fastapi import HTTPException, UploadFile

from ..models.base import Documento, RequisicaoDocumento
from .openai_service import (
    enviar_para_openai, 
    extrair_json_da_resposta_schema
)
from ..helpers.logging_helper import log_info as log


def processar_documentos(requisicao: RequisicaoDocumento, alias: str) -> Dict[str, Any]:
    """Processa documentos enviados e envia para a OpenAI.
    
    Args:
        requisicao: Objeto RequisicaoDocumento contendo os documentos e a chave da API
        alias: Alias do prompt a ser usado
        
    Returns:
        Dict[str, Any]: Resposta processada da OpenAI
        
    Raises:
        HTTPException: Se a lista de documentos estiver vazia ou houver erro no processamento
    """
    if not requisicao.documentos:
        raise HTTPException(400, "A lista de documentos está vazia.")

    conteudos = []
    for documento in requisicao.documentos:
        tipo_mime = documento.tipo_mime.lower()
        
        if tipo_mime in ("image/png", "image/jpeg", "image/jpg"):
            conteudos.append({
                "type": "input_image",
                "image_url": f"data:{tipo_mime};base64,{documento.base64}"
            })
        elif tipo_mime == "application/pdf":
            conteudos.append({
                "type": "input_file",
                "filename": documento.nome_arquivo or "documento.pdf",
                "file_data": f"data:application/pdf;base64,{documento.base64}"
            })
        else:
            raise HTTPException(400, f"MIME não suportado: {tipo_mime}")

    # Envia para a OpenAI
    resposta = enviar_para_openai(
        chave_api_openai=requisicao.chave_api_openai,
        conteudos=conteudos,
        alias=alias        
    )
    
    # Processa a resposta usando schema JSON
    try:
        json_saida = extrair_json_da_resposta_schema(resposta)
        log(f"JSON extraído com sucesso: {len(str(json_saida))} caracteres")
        log(f"JSON extraído: {json_saida}")
        return json_saida
        
    except ValueError as erro:
        log(f"Erro ao extrair JSON da resposta: {erro}")
        raise HTTPException(
            500, 
            f"Erro ao processar resposta da OpenAI: {str(erro)}"
        )


async def processar_arquivos_upload(
    chave_api_openai: str, 
    arquivos: List[UploadFile]
) -> List[Documento]:
    """Processa arquivos enviados via upload e converte para objetos Documento.
    
    Args:
        chave_api_openai: Chave de API da OpenAI
        arquivos: Lista de arquivos enviados via upload
        
    Returns:
        List[Documento]: Lista de documentos processados
        
    Raises:
        HTTPException: Se nenhum arquivo for enviado ou houver erro no processamento
    """
    if not arquivos:
        raise HTTPException(400, "Nenhum arquivo foi enviado.")
    
    documentos = []
    
    for arquivo in arquivos:
        if not arquivo.filename:
            raise HTTPException(400, "Nome do arquivo é obrigatório.")
        
        # Lê o conteúdo do arquivo
        try:
            conteudo_arquivo = await arquivo.read()
        except Exception as erro:
            raise HTTPException(
                500, 
                f"Erro ao ler arquivo {arquivo.filename}: {str(erro)}"
            )
        
        # Codifica em base64
        conteudo_base64 = base64.b64encode(conteudo_arquivo).decode('utf-8')
        
        # Determina o tipo MIME
        tipo_mime = arquivo.content_type or "application/octet-stream"
        
        # Valida tipos suportados
        tipos_suportados = [
            "image/png", "image/jpeg", "image/jpg", "application/pdf"
        ]
        
        if tipo_mime not in tipos_suportados:
            raise HTTPException(
                400, 
                f"Tipo de arquivo não suportado: {tipo_mime}. "
                f"Tipos suportados: {', '.join(tipos_suportados)}"
            )
        
        # Cria objeto Documento
        documento = Documento(
            base64=conteudo_base64,
            tipo_mime=tipo_mime,
            nome_arquivo=arquivo.filename
        )
        
        documentos.append(documento)
        log(f"Arquivo processado: {arquivo.filename} ({tipo_mime})")
    
    log(f"Total de {len(documentos)} arquivos processados com sucesso")
    return documentos