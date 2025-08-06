"""Modelos base da aplicação.

Este módulo contém os modelos Pydantic base utilizados
em toda a aplicação para documentos e requisições.
"""

from pydantic import BaseModel, Field, field_validator
from typing import List, Optional


class Documento(BaseModel):
    """Modelo para representação de um documento.
    
    Attributes:
        base64: Conteúdo do documento codificado em base64
        tipo_mime: Tipo MIME do documento
        nome_arquivo: Nome do arquivo (opcional)
    """
    
    base64: str = Field(
        ..., 
        example="SGVsbG8gV29ybGQ=", 
        description="Conteúdo do documento codificado em base64"
    )
    tipo_mime: str = Field(
        ..., 
        example="image/jpeg", 
        description="Tipo MIME do documento (image/png, image/jpeg, application/pdf)"
    )
    nome_arquivo: Optional[str] = Field(
        None, 
        example="documento.jpg", 
        description="Nome do arquivo (opcional, mais relevante para PDFs)"
    )


class RequisicaoDocumento(BaseModel):
    """Modelo base para requisições que envolvem documentos.
    
    Attributes:
        chave_api_openai: Chave de API válida da OpenAI
        documentos: Lista de documentos para análise
    """
    
    chave_api_openai: str = Field(
        ..., 
        example="sk-...", 
        description="Chave de API válida da OpenAI"
    )
    documentos: List[Documento] = Field(
        ..., 
        description="Lista de documentos para análise"
    )
    
    @field_validator('chave_api_openai')
    @classmethod
    def validar_chave_api(cls, v):
        if not v or v.strip() == "":
            raise ValueError('Chave da API OpenAI não pode estar vazia')
        return v
    
    @field_validator('documentos')
    @classmethod
    def validar_documentos(cls, v):
        if not v or len(v) == 0:
            raise ValueError('Pelo menos um documento deve ser fornecido')
        return v