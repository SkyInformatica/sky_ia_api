"""Arquivo principal da aplicação FastAPI.

Este módulo configura e inicializa a aplicação FastAPI,
incluindo routers, middleware e configurações gerais.
"""

import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from .routers import qualificacao_router, escritura_publica_router, frontend_router
from .core.config import obter_configuracoes
from .helpers.logging_helper import log_info as log


def configurar_logging():
    """Configura o sistema de logging da aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def criar_aplicacao() -> FastAPI:
    """Cria e configura a instância da aplicação FastAPI.
    
    Returns:
        FastAPI: Instância configurada da aplicação
    """
    configuracoes = obter_configuracoes()
    
    app = FastAPI(
        title="sk.ai - IA da Sky Informática",
        version="0.6",
        description="API para extração de dados estruturados de documentos utilizando IA",
        swagger_ui_parameters={
            # Tempo em milissegundos - 5 minutos = 5 * 60 * 1000
            "requestTimeout": 300_000
        }
    )
    
    # Montagem dos arquivos estáticos
    app.mount("/static", StaticFiles(directory="src/app/static"), name="static")
    
    # Inclusão das rotas
    app.include_router(frontend_router.router)
    app.include_router(qualificacao_router.router)
    app.include_router(escritura_publica_router.router)
    
    return app


# Configuração inicial
configurar_logging()

# Criação da aplicação
app = criar_aplicacao()