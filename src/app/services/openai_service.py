"""Serviço de integração com OpenAI.

Este módulo contém as funções para comunicação com a API da OpenAI,
incluindo envio de prompts e processamento de respostas.
"""

# Biblioteca padrão
import json
import re
import time
from typing import Any, Dict, List, Optional

# Terceiros
from fastapi import HTTPException
from openai import OpenAI, OpenAIError

# Locais
from ..core.config import obter_prompts
from ..helpers.logging_helper import log_info as log


def enviar_para_openai(
    chave_api_openai: str,
    conteudos: List[dict],
    alias: str
) -> Any:
    """Envia conteúdo para a OpenAI usando um prompt específico.
    
    Args:
        chave_api_openai: Chave de API válida da OpenAI
        conteudos: Lista de conteúdos a serem enviados
        alias: Alias do prompt configurado em prompts.yaml
        
    Returns:
        Any: Resposta da OpenAI
        
    Raises:
        HTTPException: Se houver erro na comunicação com a OpenAI
    """
    configuracao_prompt = obter_prompts().get(alias)
    log("Executando enviar_para_openai")
    log(f"Usando alias de prompt: {alias} -> {configuracao_prompt}")
    
    if not configuracao_prompt:
        raise HTTPException(
            500, f"Alias de prompt não encontrado em prompts.yaml: {alias}"
        )

    cliente = OpenAI(api_key=chave_api_openai)
    
    try:
        tempo_inicio = time.time()
        resposta = cliente.responses.create(
            prompt={
                "id": configuracao_prompt["id"],
                "version": configuracao_prompt.get("version")
            },
            input=[{"role": "user", "content": conteudos}],           
            max_output_tokens=8196,
            store=False
        )
        tempo_decorrido = time.time() - tempo_inicio
        log(f"Tempo de execução do client.responses.create(): {tempo_decorrido:.2f} segundos")
        
        return resposta.model_dump()
        
    except OpenAIError as erro:
        codigo_status = getattr(erro, "status_code", 502)
        raise HTTPException(
            codigo_status,
            detail=f"Um erro ocorreu com a comunicação com OpenAI. Detalhes: {str(erro)}",
            headers={"openai_error": str(erro)}
        )


def extrair_json_da_resposta_schema_old(resp_dict: dict) -> Dict[str, Any]:
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

def extrair_texto_da_resposta(dicionario_resposta: dict) -> Optional[str]:
    """Extrai o texto da resposta da OpenAI.
    
    Args:
        dicionario_resposta: Dicionário com a resposta da OpenAI
        
    Returns:
        Optional[str]: Texto extraído ou None se não encontrado
    """
    try:
        log(f"Extraindo texto da resposta: {dicionario_resposta}")
        for item in dicionario_resposta.get("output", []):
            # ignorar chamadas de ferramentas
            if item.get("type") != "message":
                continue
            for block in item.get("content", []):
                if "text" in block:
                    return block["text"]
        return None        
    except (KeyError, IndexError, AttributeError) as erro:
        log(f"Erro ao extrair texto da resposta: {erro}")
        return None


def extrair_json_da_resposta_schema(dicionario_resposta: dict) -> Dict[str, Any]:
    """Extrai JSON da resposta da OpenAI usando schema.
    
    Args:
        dicionario_resposta: Dicionário com a resposta da OpenAI
        
    Returns:
        Dict[str, Any]: JSON extraído da resposta
        
    Raises:
        ValueError: Se nenhum JSON válido for encontrado
    """
    texto_resposta = extrair_texto_da_resposta(dicionario_resposta)
    
    if not texto_resposta:
        raise ValueError("Nenhum texto encontrado na resposta da OpenAI.")
    
    # Tenta extrair JSON diretamente do texto
    try:
        return json.loads(texto_resposta)
    except json.JSONDecodeError:
        pass
    
    # Procura por blocos JSON na resposta
    padrao_json = r'```json\s*({.*?})\s*```'
    matches = re.findall(padrao_json, texto_resposta, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # Procura por JSON sem delimitadores
    padrao_json_simples = r'({.*})'
    matches = re.findall(padrao_json_simples, texto_resposta, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    raise ValueError("Nenhum JSON encontrado na resposta (json_schema).")