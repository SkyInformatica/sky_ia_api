"""Testes para o serviço de documentos."""

import pytest
from unittest.mock import Mock, patch, AsyncMock
from fastapi import UploadFile
from src.app.services.document_service import processar_arquivos_upload, processar_documentos
from src.app.models.base import Documento


class TestProcessarArquivosUpload:
    """Testes para a função processar_arquivos_upload."""

    @pytest.mark.asyncio
    async def test_processar_arquivo_pdf_valido(self):
        """Testa o processamento de um arquivo PDF válido."""
        # Mock do arquivo PDF
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "teste.pdf"
        mock_file.content_type = "application/pdf"
        mock_file.read = AsyncMock(return_value=b"conteudo_pdf_mock")
        
        documentos = await processar_arquivos_upload("sk-test", [mock_file])
        
        assert len(documentos) == 1
        assert isinstance(documentos[0], Documento)
        assert documentos[0].nome_arquivo == "teste.pdf"
        assert documentos[0].tipo_mime == "application/pdf"
        assert documentos[0].base64 is not None

    @pytest.mark.asyncio
    async def test_processar_arquivo_imagem_valida(self):
        """Testa o processamento de um arquivo de imagem válido."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "teste.png"
        mock_file.content_type = "image/png"
        mock_file.read = AsyncMock(return_value=b"conteudo_imagem_mock")
        
        documentos = await processar_arquivos_upload("sk-test", [mock_file])
        
        assert len(documentos) == 1
        assert documentos[0].nome_arquivo == "teste.png"
        assert documentos[0].tipo_mime == "image/png"

    @pytest.mark.asyncio
    async def test_processar_arquivo_tipo_nao_suportado(self):
        """Testa o processamento de um arquivo com tipo não suportado."""
        mock_file = Mock(spec=UploadFile)
        mock_file.filename = "teste.txt"
        mock_file.content_type = "text/plain"
        mock_file.read = AsyncMock(return_value=b"conteudo_texto")
        
        with pytest.raises(Exception, match="Tipo de arquivo não suportado"):
            await processar_arquivos_upload("sk-test", [mock_file])

    @pytest.mark.asyncio
    async def test_processar_multiplos_arquivos(self):
        """Testa o processamento de múltiplos arquivos."""
        mock_file1 = Mock(spec=UploadFile)
        mock_file1.filename = "teste1.pdf"
        mock_file1.content_type = "application/pdf"
        mock_file1.read = AsyncMock(return_value=b"conteudo1")
        
        mock_file2 = Mock(spec=UploadFile)
        mock_file2.filename = "teste2.jpg"
        mock_file2.content_type = "image/jpeg"
        mock_file2.read = AsyncMock(return_value=b"conteudo2")
        
        documentos = await processar_arquivos_upload("sk-test", [mock_file1, mock_file2])
        
        assert len(documentos) == 2
        assert documentos[0].nome_arquivo == "teste1.pdf"
        assert documentos[1].nome_arquivo == "teste2.jpg"


class TestProcessarDocumentos:
    """Testes para a função processar_documentos."""

    @patch('src.app.services.document_service.enviar_para_openai')
    @patch('src.app.services.document_service.extrair_json_da_resposta_schema')
    def test_processar_documentos_sucesso(self, mock_extrair_json, mock_enviar_openai):
        """Testa o processamento bem-sucedido de documentos."""
        # Configurar mocks
        mock_enviar_openai.return_value = "resposta_mock_openai"
        mock_extrair_json.return_value = {"resultado": "sucesso"}
        
        # Criar documento mock
        documento = Documento(
            base64="base64_mock",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        
        # Criar requisição mock
        from src.app.models.base import RequisicaoDocumento
        requisicao = RequisicaoDocumento(
            chave_api_openai="sk-test",
            documentos=[documento]
        )
        
        resultado = processar_documentos(requisicao, "teste")
        
        assert resultado == {"resultado": "sucesso"}
        mock_enviar_openai.assert_called_once()
        mock_extrair_json.assert_called_once_with("resposta_mock_openai")

    @patch('src.app.services.document_service.enviar_para_openai')
    def test_processar_documentos_erro_openai(self, mock_enviar_openai):
        """Testa o tratamento de erro na comunicação com OpenAI."""
        mock_enviar_openai.side_effect = Exception("Erro na API")
        
        documento = Documento(
            base64="base64_mock",
            tipo_mime="application/pdf",
            nome_arquivo="teste.pdf"
        )
        
        # Criar requisição mock
        from src.app.models.base import RequisicaoDocumento
        requisicao = RequisicaoDocumento(
            chave_api_openai="sk-test",
            documentos=[documento]
        )
        
        with pytest.raises(Exception, match="Erro na API"):
            processar_documentos(requisicao, "teste")