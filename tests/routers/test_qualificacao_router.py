"""Testes para o router de qualificação."""

import pytest
from unittest.mock import Mock, patch
from fastapi.testclient import TestClient
from fastapi import FastAPI
from src.app.routers.qualificacao_router import router

# Criar app de teste
app = FastAPI()
app.include_router(router)
client = TestClient(app)


class TestQualificacaoRouter:
    """Testes para o router de qualificação."""

    @patch('src.app.routers.qualificacao_router.processar_documentos')
    @patch('src.app.routers.qualificacao_router.processar_arquivos_upload')
    def test_qualificacao_sucesso(self, mock_processar_upload, mock_processar_docs):
        """Testa o endpoint de qualificação com sucesso."""
        from src.app.models.base import Documento
        
        # Configurar mocks
        documento_mock = Documento(
            base64="dGVzdGU=",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        mock_processar_upload.return_value = [documento_mock]
        mock_processar_docs.return_value = {
            "status": "sucesso",
            "qualificacao": "aprovado"
        }
        
        # Simular arquivo de upload
        files = {
            "arquivos": ("teste.pdf", b"conteudo_pdf", "application/pdf")
        }
        data = {
            "chave_api_openai": "sk-test123"
        }
        
        response = client.post("/qualificacao", files=files, data=data)
        
        assert response.status_code == 200
        assert response.json()["status"] == "sucesso"
        mock_processar_upload.assert_called_once()
        mock_processar_docs.assert_called_once()

    def test_qualificacao_sem_chave_api(self):
        """Testa o endpoint sem fornecer chave da API."""
        files = {
            "arquivos": ("teste.pdf", b"conteudo_pdf", "application/pdf")
        }
        
        response = client.post("/qualificacao", files=files)
        
        assert response.status_code == 422  # Validation error

    def test_qualificacao_sem_arquivos(self):
        """Testa o endpoint sem fornecer arquivos."""
        data = {
            "chave_api_openai": "sk-test123"
        }
        
        response = client.post("/qualificacao", data=data)
        
        assert response.status_code == 422  # Validation error

    @patch('src.app.routers.qualificacao_router.processar_arquivos_upload')
    def test_qualificacao_erro_processamento_arquivo(self, mock_processar_upload):
        """Testa o tratamento de erro no processamento de arquivo."""
        mock_processar_upload.side_effect = ValueError("Tipo de arquivo não suportado")
        
        files = {
            "arquivos": ("teste.txt", b"conteudo_texto", "text/plain")
        }
        data = {
            "chave_api_openai": "sk-test123"
        }
        
        response = client.post("/qualificacao", files=files, data=data)
        
        assert response.status_code == 400
        assert "Tipo de arquivo não suportado" in response.json()["detail"]

    @patch('src.app.routers.qualificacao_router.processar_documentos')
    @patch('src.app.routers.qualificacao_router.processar_arquivos_upload')
    def test_qualificacao_erro_openai(self, mock_processar_upload, mock_processar_docs):
        """Testa o tratamento de erro na comunicação com OpenAI."""
        from src.app.models.base import Documento
        
        documento_mock = Documento(
            base64="dGVzdGU=",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        mock_processar_upload.return_value = [documento_mock]
        mock_processar_docs.side_effect = Exception("Erro na API OpenAI")
        
        files = {
            "arquivos": ("teste.pdf", b"conteudo_pdf", "application/pdf")
        }
        data = {
            "chave_api_openai": "sk-test123"
        }
        
        response = client.post("/qualificacao", files=files, data=data)
        
        assert response.status_code == 500
        assert "Erro interno do servidor" in response.json()["detail"]

    def test_qualificacao_multiplos_arquivos(self):
        """Testa o endpoint com múltiplos arquivos."""
        with patch('src.app.routers.qualificacao_router.processar_arquivos_upload') as mock_upload, \
             patch('src.app.routers.qualificacao_router.processar_documentos') as mock_docs:
            
            from src.app.models.base import Documento
            
            documento_mock = Documento(
                base64="dGVzdGU=",
                tipo_mime="application/pdf",
                nome_arquivo="teste.pdf"
            )
            mock_upload.return_value = [documento_mock]
            mock_docs.return_value = {"status": "sucesso"}
            
            files = [
                ("arquivos", ("teste1.pdf", b"conteudo1", "application/pdf")),
                ("arquivos", ("teste2.jpg", b"conteudo2", "image/jpeg"))
            ]
            data = {
                "chave_api_openai": "sk-test123"
            }
            
            response = client.post("/qualificacao", files=files, data=data)
            
            assert response.status_code == 200
            # Verificar se foi chamado com 2 arquivos
            call_args = mock_upload.call_args[0][1]  # segundo parâmetro é a lista de arquivos
            assert len(call_args) == 2