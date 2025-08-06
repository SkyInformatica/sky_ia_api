"""Schemas para qualificação de documentos.

Este módulo contém os modelos Pydantic específicos
para entrada e saída da API de qualificação.
"""

from pydantic import BaseModel, Field
from typing import Dict, Any
from ..models.base import RequisicaoDocumento


class QualificacaoRequest(RequisicaoDocumento):
    """Schema para requisição de qualificação de documentos.
    
    Herda de RequisicaoDocumento, mantendo os campos base
    para chave da API e lista de documentos.
    """
    pass


class QualificacaoResponse(BaseModel):
    """Schema para resposta da análise de qualificação de documentos.
    
    Este modelo é completamente dinâmico e aceita qualquer estrutura JSON
    retornada pela OpenAI sem necessidade de campos predefinidos.
    
    A flexibilidade permite que a IA retorne diferentes estruturas
    dependendo dos documentos analisados.
    """
    
    class Config:
        extra = "allow"  # Permite campos adicionais não definidos
        arbitrary_types_allowed = True  # Permite tipos arbitrários
        
        json_schema_extra = {
            "example": {
                "pessoa": {
                    "nome": "João Silva",
                    "cpf": "123.456.789-00",
                    "rg": "12.345.678-9"
                },
                "endereco": {
                    "logradouro": "Rua das Flores, 123",
                    "cidade": "São Paulo",
                    "cep": "01234-567"
                },
                "documentos_identificados": [
                    "RG",
                    "CPF",
                    "Comprovante de residência"
                ]
            }
        }