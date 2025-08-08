"""Configurações da aplicação.

Este módulo centraliza todas as configurações da aplicação,
incluindo variáveis de ambiente e configurações específicas.
"""

import os
from typing import Dict, Any
from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import BaseSettings as PydanticBaseSettings
import yaml


class Configuracoes(PydanticBaseSettings):
    """Configurações da aplicação usando Pydantic Settings.
    
    Carrega configurações de variáveis de ambiente e arquivos .env
    """
    
    # Configurações da API
    host: str = Field(default="0.0.0.0", description="Host da aplicação")
    port: int = Field(default=8000, description="Porta da aplicação")
    debug: bool = Field(default=False, description="Modo debug")
    
    # Configurações de logging
    log_level: str = Field(default="INFO", description="Nível de log")
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


def obter_configuracoes() -> Configuracoes:
    """Obtém as configurações da aplicação.
    
    Returns:
        Configuracoes: Instância das configurações
    """
    return Configuracoes()


def obter_prompts() -> Dict[str, Any]:
    """Carrega os prompts do arquivo prompts.yaml.
    
    Returns:
        Dict[str, Any]: Dicionário com os prompts configurados
        
    Raises:
        FileNotFoundError: Se o arquivo prompts.yaml não for encontrado
        yaml.YAMLError: Se houver erro na leitura do YAML
    """
    caminho_prompts = "prompts.yaml"
    
    if not os.path.exists(caminho_prompts):
        raise FileNotFoundError(f"Arquivo de prompts não encontrado: {caminho_prompts}")
    
    try:
        with open(caminho_prompts, "r", encoding="utf-8") as arquivo:
            dados = yaml.safe_load(arquivo)
            # Retorna apenas a seção 'prompts' do YAML
            return dados.get('prompts', {}) if dados else {}
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Erro ao carregar prompts.yaml: {e}")