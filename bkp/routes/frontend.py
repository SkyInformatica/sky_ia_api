# routes/frontend.py
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import os

router = APIRouter()

# Configuração dos templates
JS_PATH = "static/js/app.js"
VERSAO = str(int(os.path.getmtime(JS_PATH)))  # timestamp do arquivo
templates = Jinja2Templates(directory="templates")
templates.env.globals["versao"] = VERSAO

@router.get("/app", response_class=HTMLResponse)
async def frontend(request: Request):
    """
    Rota para servir o frontend da aplicação.
    """
    return templates.TemplateResponse("index.html", {"request": request})