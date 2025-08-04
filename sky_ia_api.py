# sky_ia_api.py
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routes import qualificacao, escritura_publica, frontend

# Configuração do logger
def log(message: str):
    logger = logging.getLogger("uvicorn")
    logger.info(message)

# Criação da aplicação FastAPI
app = FastAPI(
    title="sk.ai - IA da Sky Informática",
    version="0.6",
    description="API para extração de dados estruturados de documentos utilizando IA",    
    swagger_ui_parameters={
        # tempo em milissegundos ‑- 5 minutos = 5 * 60 * 1000
        "requestTimeout": 300_000
    }
)

# Montagem dos arquivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inclusão das rotas
app.include_router(frontend.router)
app.include_router(qualificacao.router)
app.include_router(escritura_publica.router)