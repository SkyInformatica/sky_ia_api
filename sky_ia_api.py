# sky_ia_api.py
import base64, time
import re
import logging
import json
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field 
from typing import List, Optional, Dict, Any
from openai import OpenAI, OpenAIError
from config import get_prompts          
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi import Request
from starlette.responses import HTMLResponse
from pathlib import Path
from models.escritura_publica import EscrituraPublicaSchema


app = FastAPI(
    title="sk.ai - IA da Sky Informática",
    version="0.6",
    description="API para extração de dados estruturados de documentos utilizando IA",    
    swagger_ui_parameters={
        # tempo em milissegundos ‑- 5 minutos = 5 * 60 * 1000
        "requestTimeout": 300_000
    }
)

# Após criar o app FastAPI, adicione:
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Adicione esta rota para servir o frontend
@app.get("/app", response_class=HTMLResponse)
async def frontend(request: Request):
    versao = int(time.time())            
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "versao": versao             
        }
    )


# ---------------------- MODELOS ---------------------------------------------
class Document(BaseModel):
    base64: str = Field(..., example="SGVsbG8gV29ybGQ=", description="Conteúdo do documento codificado em base64")
    mime_type: str = Field(..., example="image/jpeg", description="Tipo MIME do documento (image/png, image/jpeg, application/pdf)")
    filename: Optional[str] = Field(None, example="documento.jpg", description="Nome do arquivo (opcional, mais relevante para PDFs)")

class QualificacaoRequest(BaseModel):
    openai_api_key: str = Field(..., example="sk-...", description="Chave de API válida da OpenAI")
    documents: List[Document] = Field(..., description="Lista de documentos para análise")

# Modelo para a resposta da API - Modificado para aceitar um objeto JSON
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
    
# Adicione após o modelo QualificacaoResponse existente

EscrituraPublicaResponse = EscrituraPublicaSchema    
    

def log(message: str):
    logger = logging.getLogger("uvicorn")
    logger.info(message)

# --- Função para extrair JSON de texto que pode estar em formato markdown
def extrair_json_da_resposta(texto: str) -> Dict[str, Any]:
    """
    Extrai um objeto JSON de uma string que pode conter delimitadores de código markdown.
    
    Args:
        texto: String que pode conter JSON com ou sem delimitadores markdown
    Returns:
        Dict: Objeto JSON extraído da string
        
    Raises:
        JSONDecodeError: Se não for possível extrair um JSON válido
    """
    # Tenta primeiro extrair JSON de blocos de código markdown
    json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(json_pattern, texto)
    
    if matches:
        # Usa o primeiro bloco de código encontrado
        try:
            return json.loads(matches[0])
        except json.JSONDecodeError:
            pass  # Se falhar, continua para tentar outras abordagens
    
    # Tenta interpretar a string inteira como JSON
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        # Tenta remover caracteres não-JSON do início e fim
        texto_limpo = texto.strip()
        if texto_limpo.startswith("{") and texto_limpo.endswith("}"):
            try:
                return json.loads(texto_limpo)
            except json.JSONDecodeError:
                pass
    
    # Se todas as tentativas falharem, lança exceção
    raise json.JSONDecodeError("Não foi possível extrair um JSON válido da resposta", texto, 0)

#----------------- Função para extrair texto da resposta OpenAI ----------------
def extract_response_text(resp_dict: dict) -> str | None:
    """
    Percorre resp_dict["output"] e devolve o primeiro
    item de texto encontrado. Retorna None se não achar.
    """
    for item in resp_dict.get("output", []):
        # ignorar chamadas de ferramentas
        if item.get("type") != "message":
            continue
        for block in item.get("content", []):
            if "text" in block:
                return block["text"]
    return None
# ---------------------------------------------------------------------------

# extração específica para respostas que usam text_format = "json_schema"
def extrair_json_da_resposta_schema(resp_dict: dict) -> Dict[str, Any]:
    """
    Extrai o JSON produzido por um prompt com `text_format=json_schema`.

    Estratégia:
    • Procura o primeiro bloco `type=="output_text"` (ou 'text') cujo
      conteúdo comece com '{' ou '['.
    • Faz json.loads e devolve o dicionário resultante.

    Levanta ValueError se nada válido for encontrado.
    """
    for item in resp_dict.get("output", []):
        if item.get("type") != "message":
            continue

        for block in item.get("content", []):
            if block.get("type") in ("output_text", "text") and "text" in block:
                raw = block["text"].lstrip()

                # Garante que estamos olhando para um JSON
                if raw.startswith("{") or raw.startswith("["):
                    try:
                        return json.loads(raw)
                    except json.JSONDecodeError as e:
                        raise ValueError(f"JSON inválido: {e}") from None

    raise ValueError("Nenhum JSON encontrado na resposta (json_schema).")
# ------------------------------------------------------------------------------


# ------------------ Função que fala com a OpenAI ----------------------------
def enviar_para_openai(
    openai_api_key: str,
    contents: List[dict],
    alias: str,
    expected_format: str = "text"                           
) -> Any:  
    prompt_cfg = get_prompts().get(alias)
    log("Executando enviar_para_openai")
    log(f"Usando alias de prompt: {alias} -> {prompt_cfg}")
    if not prompt_cfg:
        raise HTTPException(
            500, f"Alias de prompt não encontrado em prompts.yaml: {alias}"
)

    client = OpenAI(api_key=openai_api_key)
    try:        
        start_time = time.time()
        response = client.responses.create(
            prompt={
                "id": prompt_cfg["id"],
                "version": prompt_cfg["version"] if "version" in prompt_cfg else None
            },
            input=[{"role": "user", "content": contents}],
            reasoning={},
            max_output_tokens=8196,
            store=True
    )
        elapsed_time = time.time() - start_time
        log(f"Tempo de execução do client.responses.create(): {elapsed_time:.2f} segundos")
    except OpenAIError as err:
        status_code = getattr(err, "status_code", 502)
        raise HTTPException(
            status_code,
            detail=f"Um erro ocorreu com a comunicação com OpenAI. Detalhes: {str(err)}",
            headers={"openai_error": str(err)}
        )

    data = response.model_dump()
    
    # Decide como devolver com base no formato esperado
    if expected_format == "json":
        # Para rota escritura_publica vamos tratar fora
        return data

    text = extract_response_text(data)
    if text is None:
        log("Estrutura inesperada: não foi encontrado bloco de texto.")
        raise HTTPException(502, "Estrutura inesperada na resposta da OpenAI")
    return text


# ----------------------- Endpoint QUALIFICACAO --------------------------------------
@app.post("/qualificacao", 
    response_model=QualificacaoResponse,
    summary="Qualificação de documentos via JSON",
    description="""
    Endpoint para qualificação de documentos enviados em formato JSON.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Os documentos devem ser codificados em base64 e enviados com o MIME type correto.
    Para PDFs, é possível especificar o nome do arquivo.
    
    Tipos de documentos que podem ser utilizados: RG, CNH, Comprovante de residencia, 
    Conta de luz, Conta de agua, Certidão de casamento, Certidão de nascimento, 
    Certidão de obito, Pacto antenupcial, etc...    
    """
)
def qualificacao_json(body: QualificacaoRequest) -> QualificacaoResponse:
    """
    Processa documentos em formato base64 para análise e qualificação.
    
    - Para imagens (PNG, JPEG/JPG): Envie o conteúdo codificado em base64 com o MIME type correspondente
    - Para PDFs: Envie o conteúdo codificado em base64 com MIME type "application/pdf"
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        QualificacaoResponse: Objeto contendo a resposta da análise
    """
    if not body.documents:
        raise HTTPException(400, "A lista de documentos está vazia.")

    contents = []
    for doc in body.documents:
        mime = doc.mime_type.lower()
        if mime in ("image/png", "image/jpeg", "image/jpg"):
            contents.append({
                "type": "input_image",
                "image_url": f"data:{mime};base64,{doc.base64}"
            })
        elif mime == "application/pdf":
            contents.append({
                "type": "input_file",
                "filename": doc.filename or "documento.pdf",
                "file_data": f"data:application/pdf;base64,{doc.base64}"
            })
        else:
            raise HTTPException(400, f"MIME não suportado: {mime}")

    # Recebe apenas o texto da função enviar_para_openai
    texto_resposta = enviar_para_openai(
        openai_api_key=body.openai_api_key,
        contents=contents,
        alias="qualificacao"        
    )
    
    try:
        # Usa a função robusta para extrair o JSON
        output_json = extrair_json_da_resposta(texto_resposta)
        log(f"JSON extraído com sucesso: {json.dumps(output_json)[:100]}...")
    except json.JSONDecodeError as e:
        log(f"Erro ao decodificar JSON: {str(e)}")
        log(f"Texto da resposta: {texto_resposta[:200]}...")
        raise HTTPException(500, "Erro ao decodificar a resposta da OpenAI como JSON.")

    # Constrói e retorna o objeto QualificacaoResponse com o JSON completo
    return QualificacaoResponse(resposta=output_json)
# ---------------------------------------------------------------------------


# ------------- Endpoint QUALIFICACAO/UPLOAD multipart (reutiliza a mesma lógica) ---------------
@app.post("/qualificacao/upload",
    response_model=QualificacaoResponse,
    summary="Qualificação de documentos via upload de arquivos",
    description="""
    Endpoint para qualificação de documentos através de upload direto de arquivos.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Este endpoint aceita requisições multipart/form-data, facilitando o upload 
    direto de arquivos sem a necessidade de codificação prévia em base64.
    
    Tipos de documentos que podem ser utilizados: RG, CNH, Comprovante de residencia, 
    Conta de luz, Conta de agua, Certidão de casamento, Certidão de nascimento, 
    Certidão de obito, Pacto antenupcial, etc...
    """
)
async def qualificacao_upload(
    openai_api_key: str = Form(..., description="Chave de API válida da OpenAI"),
    files: List[UploadFile] = File(..., description="Arquivos para análise (PNG, JPEG/JPG, PDF)")
) -> QualificacaoResponse:
    """
    Processa arquivos enviados diretamente para análise e qualificação.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        QualificacaoResponse: Objeto contendo a resposta da análise
    """
    if not files:
        raise HTTPException(400, "Nenhum arquivo enviado.")

    documentos: List[Document] = []
    for file in files:
        raw = await file.read()
        if not raw:
            continue

        mime = (file.content_type or "").lower()
        if mime not in ("image/png", "image/jpeg", "image/jpg", "application/pdf"):
            raise HTTPException(400, f"Tipo de arquivo não suportado: {mime}")

        b64 = base64.b64encode(raw).decode()
        filename = file.filename if mime == "application/pdf" else None
        documentos.append(Document(base64=b64, mime_type=mime, filename=filename))

    req = QualificacaoRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    # reutiliza a lógica da rota JSON, que já define o alias
    return qualificacao_json(req)
# ---------------------------------------------------------------------------

# ----------------------- Endpoint ESCRITURA_PUBLICA --------------------------------------

@app.post("/escritura_publica", 
    response_model=EscrituraPublicaResponse,
    summary="Extração de dados de escritura pública",
    description="""
    Endpoint para extração de dados de escritura pública.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Os documentos devem ser codificados em base64 e enviados com o MIME type correto.
    Para PDFs, é possível especificar o nome do arquivo.
    
    Tipos de documentos que podem ser utilizados: Escritura Pública lavrada em Tabelionato de Notas
    """
)
def escritura_publica_json(body: QualificacaoRequest) -> EscrituraPublicaResponse:
    """
    Processa documentos em formato base64 para análise de escritura pública.
    
    - Para imagens (PNG, JPEG/JPG): Envie o conteúdo codificado em base64 com o MIME type correspondente
    - Para PDFs: Envie o conteúdo codificado em base64 com MIME type "application/pdf"
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        EscrituraPublicaResponse: Objeto contendo a resposta da análise
    """
    if not body.documents:
        raise HTTPException(400, "A lista de documentos está vazia.")

    contents = []
    for doc in body.documents:
        mime = doc.mime_type.lower()
        if mime in ("image/png", "image/jpeg", "image/jpg"):
            contents.append({
                "type": "input_image",
                "image_url": f"data:{mime};base64,{doc.base64}"
            })
        elif mime == "application/pdf":
            contents.append({
                "type": "input_file",
                "filename": doc.filename or "documento.pdf",
                "file_data": f"data:application/pdf;base64,{doc.base64}"
            })
        else:
            raise HTTPException(400, f"MIME não suportado: {mime}")

    resp_dict = enviar_para_openai(
        openai_api_key=body.openai_api_key,
        contents=contents,
        alias="escritura_publica",
        expected_format="json"        
    )
    
    try:
        output_json = extrair_json_da_resposta_schema(resp_dict)
        log(f"JSON extraído com sucesso: {json.dumps(output_json)[:100]}...")
    except Exception as e:
        log(f"Falha ao extrair JSON (schema): {str(e)}")
        raise HTTPException(502, "Resposta da OpenAI não contém JSON válido no formato esperado.")

    return EscrituraPublicaResponse(**output_json)

# -----------------Endpoint ESCRITURA_PUBLICA/UPLOAD multipart (reutiliza a mesma lógica) ---------------
@app.post("/escritura_publica/upload",
    response_model=EscrituraPublicaResponse,
    summary="Extração de dados de escritura pública via upload de arquivos",
    description="""
    Endpoint paraExtração de dados de escritura pública através de upload direto de arquivos.
    
    **Tipos de arquivos suportados:**
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    Este endpoint aceita requisições multipart/form-data, facilitando o upload 
    direto de arquivos sem a necessidade de codificação prévia em base64.
    
    Tipos de documentos que podem ser utilizados: Escritura Pública lavrada em Tabelionato de Notas
    """
)
async def escritura_publica_upload(
    openai_api_key: str = Form(..., description="Chave de API válida da OpenAI"),
    files: List[UploadFile] = File(..., description="Arquivos para análise (PNG, JPEG/JPG, PDF)")
) -> EscrituraPublicaResponse:
    """
    Processa arquivos enviados diretamente para análise de escritura pública.
    
    Aceita múltiplos arquivos nos formatos:
    - Imagens: PNG, JPEG/JPG
    - Documentos: PDF
    
    É necessário fornecer uma chave de API válida da OpenAI.
    
    Returns:
        EscrituraPublicaResponse: Objeto contendo a resposta da análise
    """
    if not files:
        raise HTTPException(400, "Nenhum arquivo enviado.")

    documentos: List[Document] = []
    for file in files:
        raw = await file.read()
        if not raw:
            continue

        mime = (file.content_type or "").lower()
        if mime not in ("image/png", "image/jpeg", "image/jpg", "application/pdf"):
            raise HTTPException(400, f"Tipo de arquivo não suportado: {mime}")

        b64 = base64.b64encode(raw).decode()
        filename = file.filename if mime == "application/pdf" else None
        documentos.append(Document(base64=b64, mime_type=mime, filename=filename))

    req = QualificacaoRequest(
        openai_api_key=openai_api_key,
        documents=documentos
    )
    return escritura_publica_json(req)