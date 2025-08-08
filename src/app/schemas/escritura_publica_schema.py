"""Schemas para escritura pública.

Este módulo contém os modelos Pydantic específicos
para entrada e saída da API de escritura pública.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any, List, Optional
from ..models.base import RequisicaoDocumento


class EscrituraPublicaRequest(RequisicaoDocumento):
    """Schema para requisição de análise de escritura pública.
    
    Herda de RequisicaoDocumento, mantendo os campos base
    para chave da API e lista de documentos.
    """
    pass


class EscrituraPublicaResponse(BaseModel):
    """Schema para resposta da análise de escritura pública.
    
    Este modelo é completamente dinâmico e aceita qualquer estrutura JSON
    retornada pela OpenAI sem necessidade de campos predefinidos.
    
    A flexibilidade permite que a IA retorne diferentes estruturas
    dependendo do tipo de escritura analisada.
    """
    
    class Config:
        extra = "allow"  # Permite campos adicionais não definidos
        arbitrary_types_allowed = True  # Permite tipos arbitrários
