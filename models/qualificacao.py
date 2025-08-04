# models/qualificacao.py
from pydantic import BaseModel, Field
from typing import Dict, Any
from .base import DocumentRequest

class QualificacaoRequest(DocumentRequest):
    """Modelo para requisição de qualificação de documentos"""
    pass

class QualificacaoResponse(BaseModel):
    resposta: Dict[str, Any] = Field(..., 
                         example={ 
                            "data": [{                                                              
                                "informacoes_pessoais": {
                                    "cpf": "123.456.789-00",
                                    "nome": "JOÃO DA SILVA",
                                    "sexo": "MASCULINO",
                                    "estado_civil": "CASADO",
                                    "data_nascimento": "10/01/1980",
                                    "nacionalidade": "BRASILEIRO",
                                    "naturalidade": {
                                    "cidade": "RIO DE JANEIRO",
                                    "uf": "RJ"
                                    },
                                    "profissao": "ENGENHEIRO",
                                    "pai": "ANTONIO DA SILVA",
                                    "mae": "MARIA DA SILVA"
                                },
                                "documentos_identificacao": [
                                    {
                                    "tipo": "CNH",
                                    "numero": "123456789",
                                    "orgao": "DETRAN",
                                    "data_expedicao": "10/01/2019",
                                    "data_vencimento": "10/01/2029",
                                    "uf": "RJ"
                                    },
                                    {
                                    "tipo": "RG",
                                    "numero": "305278123",
                                    "orgao": "SSP",
                                    "data_expedicao": "15/05/2010",
                                    "data_vencimento": "",
                                    "uf": "RJ"
                                    }
                                ],
                                "endereco_residencial": {
                                    "cep": "12345-678",
                                    "logradouro": "AVENIDA BRASIL",
                                    "numero": "123",
                                    "complemento": "APTO 567",
                                    "bairro": "JARDIM DAS ROSAS",
                                    "cidade": "RIO DE JANEIRO",
                                    "uf": "RJ",
                                    "pais": "BRASIL"
                                },
                                "informacoes_nascimento": {
                                    "numero_certidao": "12345",
                                    "livro": "12",
                                    "folha": "34",
                                    "cidade_registro": "RIO DE JANEIRO",
                                    "uf_registro": "RJ",
                                    "data_certidao": "10/01/1980"
                                },
                                "informacoes_conjuge": {
                                    "cpf": "987.654.321-00",
                                    "nome": "MARIA DE SOUZA",
                                    "informacoes_casamento": {
                                    "regime_bens": "comunhão parcial",
                                    "data_casamento": "15/06/2005",
                                    "data_atualizacao": "10/02/2020",
                                    "numero_certidao": "67890",
                                    "data_certidao": "10/06/2005",
                                    "livro": "8",
                                    "folha": "22",
                                    "cidade_registro": "RIO DE JANEIRO",
                                    "uf_registro": "RJ"
                                    },
                                    "pacto_antenupcial": {
                                    "dados_tabelionato": {
                                        "livro": "5",
                                        "folha": "10",
                                        "cidade_tabelionato": "RIO DE JANEIRO",
                                        "uf_tabelionato": "RJ",
                                        "data": "15/06/2005"
                                    },
                                    "dados_registro_imoveis": {
                                        "numero_registro": "54321",
                                        "livro": "4",
                                        "cidade_registro": "RIO DE JANEIRO",
                                        "uf_registro": "RJ",
                                        "data": "20/06/2005"
                                    }
                                    }
                                }
                            }],
                            "resposta_processamento_markdown": ""                            
                         }, 
                         description="Objeto JSON com os dados extraídos da análise dos documentos")