# sky_ia_api.py
import base64, time
import re
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from openai import OpenAI, OpenAIError
from config import get_prompts          
import logging
import json


app = FastAPI(
    title="Qualificação API", 
    version="0.6",
    description="API para qualificação de documentos utilizando OpenAI"
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
                            },
                            "resposta_processamento_markdown": ""
                            
                         }, 
                         description="Objeto JSON com os dados extraídos da análise dos documentos")
    
    # Caso queira adicionar campos futuros (comentados por enquanto)
    # status: str = Field("success", example="success", description="Status da operação")
    # confidence: float = Field(None, example=0.95, description="Nível de confiança da análise (0-1)")
    # metadata: dict = Field(None, example={"processing_time": "1.2s"}, description="Metadados adicionais da análise")

def log(message: str):
    logger = logging.getLogger("uvicorn")
    logger.info(message)

# Função para extrair JSON de texto que pode estar em formato markdown
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

# ------------------ Função que fala com a OpenAI ----------------------------
def enviar_para_openai(
    openai_api_key: str,
    contents: List[dict],
    alias: str                           
) -> str:  
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
            max_output_tokens=2048,
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
    try:
        text = data["output"][0]["content"][0]["text"]
        return text  # Retorna apenas o texto
    except (KeyError, IndexError, TypeError):
        raise HTTPException(502, "Estrutura inesperada na resposta da OpenAI")
# ---------------------------------------------------------------------------


# ----------------------- Endpoint JSON --------------------------------------
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
    
    A resposta será gerada pela OpenAI com base nos documentos fornecidos.
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


# ------------- Endpoint multipart (reutiliza a mesma lógica) ---------------
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
    
    A resposta será gerada pela OpenAI com base nos documentos fornecidos.
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