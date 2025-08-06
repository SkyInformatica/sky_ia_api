"""Funções utilitárias para logging.

Este módulo contém funções auxiliares para
sistema de logging da aplicação.
"""

import logging
from typing import Optional


def obter_logger(nome: Optional[str] = None) -> logging.Logger:
    """Obtém uma instância do logger configurado.
    
    Args:
        nome: Nome do logger. Se None, usa "uvicorn"
        
    Returns:
        logging.Logger: Instância do logger
    """
    nome_logger = nome or "uvicorn"
    return logging.getLogger(nome_logger)


def log(mensagem: str, nivel: str = "info", logger_nome: Optional[str] = None):
    """Função padronizada para logging.
    
    Args:
        mensagem: Mensagem a ser registrada no log
        nivel: Nível do log ("debug", "info", "warning", "error", "critical")
        logger_nome: Nome do logger a ser usado
    """
    logger = obter_logger(logger_nome)
    
    nivel_lower = nivel.lower()
    if nivel_lower == "debug":
        logger.debug(mensagem)
    elif nivel_lower == "info":
        logger.info(mensagem)
    elif nivel_lower == "warning":
        logger.warning(mensagem)
    elif nivel_lower == "error":
        logger.error(mensagem)
    elif nivel_lower == "critical":
        logger.critical(mensagem)
    else:
        logger.info(mensagem)  # Fallback para info


def log_info(mensagem: str, logger_nome: Optional[str] = None):
    """Registra mensagem de informação.
    
    Args:
        mensagem: Mensagem a ser registrada
        logger_nome: Nome do logger a ser usado
    """
    log(mensagem, "info", logger_nome)


def log_error(mensagem: str, logger_nome: Optional[str] = None):
    """Registra mensagem de erro.
    
    Args:
        mensagem: Mensagem a ser registrada
        logger_nome: Nome do logger a ser usado
    """
    log(mensagem, "error", logger_nome)


def log_warning(mensagem: str, logger_nome: Optional[str] = None):
    """Registra mensagem de aviso.
    
    Args:
        mensagem: Mensagem a ser registrada
        logger_nome: Nome do logger a ser usado
    """
    log(mensagem, "warning", logger_nome)