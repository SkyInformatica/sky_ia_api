"""Testes para o módulo principal da aplicação."""

import pytest
from fastapi.testclient import TestClient
from src.app.main import app

client = TestClient(app)


def test_app_health():
    """Testa se a aplicação está funcionando corretamente."""
    response = client.get("/")
    assert response.status_code == 404  # Não há rota raiz definida


def test_app_frontend_route():
    """Testa se a rota do frontend está acessível."""
    response = client.get("/app")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_app_static_files():
    """Testa se os arquivos estáticos estão sendo servidos."""
    response = client.get("/static/css/style.css")
    assert response.status_code == 200
    assert "text/css" in response.headers["content-type"]