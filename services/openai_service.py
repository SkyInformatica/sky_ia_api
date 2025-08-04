# services/openai_service.py
import json
import time
import re
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI, OpenAIError
from fastapi import HTTPException
from config import get_prompts

def log(message: str):
    logger = logging.getLogger("uvicorn")
    logger.info(message)

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