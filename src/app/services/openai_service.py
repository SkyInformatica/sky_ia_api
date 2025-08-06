"""Serviço de integração com OpenAI.

Este módulo contém as funções para comunicação com a API da OpenAI,
incluindo envio de prompts e processamento de respostas.
"""

import json
import time
import re
import logging
from typing import List, Dict, Any, Optional
from openai import OpenAI, OpenAIError
from fastapi import HTTPException

from ..core.config import obter_prompts
from ..helpers.logging_helper import log_info as log


def enviar_para_openai(
    chave_api_openai: str,
    conteudos: List[dict],
    alias: str,
    formato_esperado: str = "text"
) -> Any:
    """Envia conteúdo para a OpenAI usando um prompt específico.
    
    Args:
        chave_api_openai: Chave de API válida da OpenAI
        conteudos: Lista de conteúdos a serem enviados
        alias: Alias do prompt configurado em prompts.yaml
        formato_esperado: Formato esperado da resposta ("text" ou "json")
        
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
            reasoning={},
            max_output_tokens=8196,
            store=True
        )
        tempo_decorrido = time.time() - tempo_inicio
        log(f"Tempo de execução do client.responses.create(): {tempo_decorrido:.2f} segundos")
        
        return resposta
        
    except OpenAIError as erro:
        codigo_status = getattr(erro, "status_code", 502)
        raise HTTPException(
            codigo_status,
            detail=f"Um erro ocorreu com a comunicação com OpenAI. Detalhes: {str(erro)}",
            headers={"openai_error": str(erro)}
        )


def extrair_texto_da_resposta(dicionario_resposta: dict) -> Optional[str]:
    """Extrai o texto da resposta da OpenAI.
    
    Args:
        dicionario_resposta: Dicionário com a resposta da OpenAI
        
    Returns:
        Optional[str]: Texto extraído ou None se não encontrado
    """
    try:
        # Navega pela estrutura da resposta para encontrar o texto
        choices = dicionario_resposta.get("choices", [])
        if choices and len(choices) > 0:
            message = choices[0].get("message", {})
            content = message.get("content")
            if content:
                return content.strip()
        
        # Fallback para outras estruturas possíveis
        if "content" in dicionario_resposta:
            return dicionario_resposta["content"].strip()
            
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
    
    # Procura por blocos JSON na resposta
    padrao_json = r'```json\s*({.*?})\s*```'
    matches = re.findall(padrao_json, texto_resposta, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    # Tenta extrair JSON diretamente do texto
    try:
        return json.loads(texto_resposta)
    except json.JSONDecodeError:
        pass
    
    # Procura por JSON sem delimitadores
    padrao_json_simples = r'({.*})'
    matches = re.findall(padrao_json_simples, texto_resposta, re.DOTALL)
    
    for match in matches:
        try:
            return json.loads(match)
        except json.JSONDecodeError:
            continue
    
    raise ValueError("Nenhum JSON encontrado na resposta (json_schema).")