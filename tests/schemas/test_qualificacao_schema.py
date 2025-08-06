"""Testes para os schemas de qualificação."""

import pytest
from pydantic import ValidationError
from src.app.schemas.qualificacao_schema import QualificacaoRequest, QualificacaoResponse
from src.app.models.base import Documento


class TestQualificacaoRequest:
    """Testes para o schema QualificacaoRequest."""

    def test_qualificacao_request_valido(self):
        """Testa a criação de um QualificacaoRequest válido."""
        documento = Documento(
            base64="dGVzdGU=",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        
        request = QualificacaoRequest(
            chave_api_openai="sk-test123",
            documentos=[documento]
        )
        
        assert request.chave_api_openai == "sk-test123"
        assert len(request.documentos) == 1
        assert request.documentos[0].nome_arquivo == "teste.pdf"

    def test_qualificacao_request_sem_chave_api(self):
        """Testa a validação quando a chave da API não é fornecida."""
        documento = Documento(
            base64="dGVzdGU=",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            QualificacaoRequest(
                documentos=[documento]
            )
        
        assert "chave_api_openai" in str(exc_info.value)

    def test_qualificacao_request_sem_documentos(self):
        """Testa a validação quando nenhum documento é fornecido."""
        with pytest.raises(ValidationError) as exc_info:
            QualificacaoRequest(
                chave_api_openai="sk-test123",
                documentos=[]
            )
        
        assert "documentos" in str(exc_info.value)

    def test_qualificacao_request_chave_api_vazia(self):
        """Testa a validação com chave da API vazia."""
        documento = Documento(
            base64="dGVzdGU=",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        
        with pytest.raises(ValidationError) as exc_info:
            QualificacaoRequest(
                chave_api_openai="",
                documentos=[documento]
            )
        
        assert "chave_api_openai" in str(exc_info.value)

    def test_qualificacao_request_multiplos_documentos(self):
        """Testa a criação com múltiplos documentos."""
        documento1 = Documento(
            base64="dGVzdGUx",
            tipo_mime="application/pdf",
            nome_arquivo="teste1.pdf"
        )
        documento2 = Documento(
            base64="dGVzdGUy",
            tipo_mime="image/jpeg",
            nome_arquivo="teste2.jpg"
        )
        
        request = QualificacaoRequest(
            chave_api_openai="sk-test123",
            documentos=[documento1, documento2]
        )
        
        assert len(request.documentos) == 2
        assert request.documentos[0].nome_arquivo == "teste1.pdf"
        assert request.documentos[1].nome_arquivo == "teste2.jpg"


class TestQualificacaoResponse:
    """Testes para o schema QualificacaoResponse."""

    def test_qualificacao_response_campos_dinamicos(self):
        """Testa a criação de QualificacaoResponse com campos dinâmicos."""
        response_data = {
            "status": "aprovado",
            "pontuacao": 85,
            "observacoes": "Documentação completa",
            "detalhes": {
                "cpf_valido": True,
                "renda_comprovada": True
            }
        }
        
        response = QualificacaoResponse(**response_data)
        
        assert response.status == "aprovado"
        assert response.pontuacao == 85
        assert response.observacoes == "Documentação completa"
        assert response.detalhes["cpf_valido"] is True

    def test_qualificacao_response_vazio(self):
        """Testa a criação de QualificacaoResponse vazio."""
        response = QualificacaoResponse()
        
        # Deve permitir criação sem campos obrigatórios
        assert isinstance(response, QualificacaoResponse)

    def test_qualificacao_response_tipos_arbitrarios(self):
        """Testa se o response aceita tipos arbitrários."""
        response_data = {
            "lista_documentos": ["doc1", "doc2"],
            "numero_protocolo": 12345,
            "data_analise": "2024-01-15",
            "analista": {
                "nome": "João Silva",
                "id": 123
            }
        }
        
        response = QualificacaoResponse(**response_data)
        
        assert response.lista_documentos == ["doc1", "doc2"]
        assert response.numero_protocolo == 12345
        assert response.data_analise == "2024-01-15"
        assert response.analista["nome"] == "João Silva"

    def test_qualificacao_response_json_schema_extra(self):
        """Testa se o exemplo do schema está definido corretamente."""
        schema = QualificacaoResponse.model_json_schema()
        
        # No Pydantic v2, o exemplo fica em json_schema_extra dentro de example
        assert "example" in schema
        
        exemplo = schema["example"]
        assert "pessoa" in exemplo
        assert "documentos_identificados" in exemplo