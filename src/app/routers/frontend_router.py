"""Router para endpoints do frontend.

Este módulo contém os endpoints da API relacionados à
interface web da aplicação.
"""

# Biblioteca padrão
import os

# Terceiros
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse


router = APIRouter()

# Configuração dos templates
CAMINHO_JS = "src/app/static/js/app.js"
VERSAO = str(int(os.path.getmtime(CAMINHO_JS)))  # timestamp do arquivo
templates = Jinja2Templates(directory="src/app/templates")
templates.env.globals["versao"] = VERSAO


@router.get("/app", response_class=HTMLResponse)
async def servir_frontend(request: Request):
    """Rota para servir o frontend da aplicação.
    
    Args:
        request: Objeto de requisição do FastAPI
        
    Returns:
        HTMLResponse: Página HTML do frontend
    """
    return templates.TemplateResponse("index.html", {"request": request})