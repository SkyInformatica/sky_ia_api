# Etapa de build (opcional para otimizar cache de deps)
FROM python:3.13.5-slim AS builder

WORKDIR /tmp

# Copia o requirements primeiro para aproveitar cache
COPY sky_ia_api/requirements.txt ./

RUN pip install --upgrade pip \
 && pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

# Etapa final
FROM python:3.13.5-slim

# Cria um usuário não-root (opcional, mas recomendado)
RUN adduser --disabled-password --gecos '' apiuser

WORKDIR /app

# Instala dependências a partir dos wheels gerados
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir /wheels/*

# Copia todo o código-fonte
COPY sky_ia_api/ .

# Expoe a porta padrão
EXPOSE 8000

USER apiuser

# Comando de inicialização
CMD ["uvicorn", "sky_ia_api:app", "--host", "0.0.0.0", "--port", "8000"]
