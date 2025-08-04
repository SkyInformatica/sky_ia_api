# models/qualificacao.py
from pydantic import BaseModel, Field
from typing import Dict, Any
from .base import DocumentRequest

class QualificacaoRequest(DocumentRequest):
    """Modelo para requisição de qualificação de documentos"""
    pass

class QualificacaoResponse(BaseModel):
    """Modelo para resposta da análise de qualificação de documentos
    
    Este modelo é completamente dinâmico e aceita qualquer estrutura JSON
    retornada pela OpenAI sem necessidade de campos predefinidos.
    """
    
    class Config:
        extra = "allow"  
        arbitrary_types_allowed = True