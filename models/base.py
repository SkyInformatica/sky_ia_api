# models/base.py
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class Document(BaseModel):
    base64: str = Field(..., example="SGVsbG8gV29ybGQ=", description="Conteúdo do documento codificado em base64")
    mime_type: str = Field(..., example="image/jpeg", description="Tipo MIME do documento (image/png, image/jpeg, application/pdf)")
    filename: Optional[str] = Field(None, example="documento.jpg", description="Nome do arquivo (opcional, mais relevante para PDFs)")

class DocumentRequest(BaseModel):
    """Modelo base para requisições que envolvem documentos"""
    openai_api_key: str = Field(..., example="sk-...", description="Chave de API válida da OpenAI")
    documents: List[Document] = Field(..., description="Lista de documentos para análise")