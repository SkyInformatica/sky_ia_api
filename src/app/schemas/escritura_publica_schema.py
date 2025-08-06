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
        
        json_schema_extra = {
            "example": {
                "tipo_escritura": "Compra e Venda",
                "partes": {
                    "outorgante_vendedor": {
                        "nome": "Maria Silva",
                        "cpf": "123.456.789-00",
                        "estado_civil": "Casada"
                    },
                    "outorgado_comprador": {
                        "nome": "João Santos",
                        "cpf": "987.654.321-00",
                        "estado_civil": "Solteiro"
                    }
                },
                "imovel": {
                    "descricao": "Apartamento 101",
                    "endereco": "Rua das Palmeiras, 456",
                    "matricula": "12345",
                    "cartorio": "1º Cartório de Registro de Imóveis"
                },
                "valor_transacao": "R$ 350.000,00",
                "data_escritura": "2024-01-15",
                "cartorio_lavrou": "Cartório Silva",
                "tabeliao": "Dr. Carlos Oliveira"
            }
        }