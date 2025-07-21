# config.py
from functools import lru_cache
from pathlib import Path
import yaml

@lru_cache
def get_prompts(path: str | Path = "prompts.yaml") -> dict:
    """Carrega e devolve o dict {alias: {id, version}}"""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Arquivo de configuração não encontrado: {path!s}")

    with path.open("r", encoding="utf-8") as fh:
        data = yaml.safe_load(fh) or {}

    return data.get("prompts", {})
