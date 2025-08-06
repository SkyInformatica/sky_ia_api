# Usar a imagem oficial do uv para melhor performance
FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

# Cria um usuário não-root (recomendado para segurança)
RUN adduser --disabled-password --gecos '' apiuser

# Define o diretório de trabalho
WORKDIR /app

# Copia os arquivos de configuração de dependências primeiro (para cache)
COPY pyproject.toml uv.lock* ./

# Instala as dependências usando uv
RUN uv sync --frozen --no-cache --no-dev

# Copia todo o código-fonte
COPY . .

# Ajusta as permissões do diretório para o usuário apiuser
RUN chown -R apiuser:apiuser /app

# Expoe a porta padrão
EXPOSE 8000

# Muda para o usuário não-root
USER apiuser

# Comando de inicialização usando uv run
CMD ["uv", "run", "uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
