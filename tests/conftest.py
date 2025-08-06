"""Configurações e fixtures para os testes."""

import pytest
import os
import sys
from pathlib import Path

# Adicionar o diretório src ao path para importações
project_root = Path(__file__).parent.parent
src_path = project_root / "src"
sys.path.insert(0, str(src_path))


@pytest.fixture
def mock_openai_api_key():
    """Fixture que fornece uma chave de API mock para testes."""
    return "sk-test-1234567890abcdef"


@pytest.fixture
def sample_pdf_content():
    """Fixture que fornece conteúdo mock de PDF em base64."""
    return "JVBERi0xLjQKJcOkw7zDtsOfCjIgMCBvYmoKPDwKL0xlbmd0aCAzIDAgUgo+PgpzdHJlYW0KQNC4"


@pytest.fixture
def sample_image_content():
    """Fixture que fornece conteúdo mock de imagem em base64."""
    return "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg=="


@pytest.fixture
def mock_documento_pdf(sample_pdf_content):
    """Fixture que cria um documento PDF mock."""
    from app.models.base import Documento
    
    return Documento(
        base64=sample_pdf_content,
        tipo_mime="application/pdf",
        nome_arquivo="documento_teste.pdf"
    )


@pytest.fixture
def mock_documento_imagem(sample_image_content):
    """Fixture que cria um documento de imagem mock."""
    from app.models.base import Documento
    
    return Documento(
        base64=sample_image_content,
        tipo_mime="image/jpeg",
        nome_arquivo="imagem_teste.jpg"
    )


@pytest.fixture
def mock_qualificacao_response():
    """Fixture que fornece uma resposta mock de qualificação."""
    return {
        "status": "aprovado",
        "pontuacao": 85,
        "documentos_analisados": [
            {
                "nome": "documento_teste.pdf",
                "tipo": "CPF",
                "valido": True,
                "observacoes": "Documento válido e legível"
            }
        ],
        "observacoes_gerais": "Documentação completa e em conformidade",
        "recomendacoes": [
            "Prosseguir com a análise de crédito"
        ]
    }


@pytest.fixture
def mock_escritura_response():
    """Fixture que fornece uma resposta mock de escritura pública."""
    return {
        "tipo_escritura": "compra_venda",
        "partes": {
            "vendedor": {
                "nome": "João Silva",
                "cpf": "123.456.789-00"
            },
            "comprador": {
                "nome": "Maria Santos",
                "cpf": "987.654.321-00"
            }
        },
        "imovel": {
            "endereco": "Rua das Flores, 123",
            "matricula": "12345",
            "valor": 350000.00
        },
        "data_escritura": "2024-01-15",
        "cartorio": "1º Tabelionato de Notas",
        "observacoes": "Escritura regular sem pendências"
    }


@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configuração automática do ambiente de teste."""
    # Configurar variáveis de ambiente para testes
    os.environ["TESTING"] = "true"
    os.environ["LOG_LEVEL"] = "DEBUG"
    
    yield
    
    # Limpeza após os testes
    if "TESTING" in os.environ:
        del os.environ["TESTING"]
    if "LOG_LEVEL" in os.environ:
        del os.environ["LOG_LEVEL"]


@pytest.fixture
def client():
    """Fixture que fornece um cliente de teste para a aplicação FastAPI."""
    from fastapi.testclient import TestClient
    from app.main import app
    
    return TestClient(app)