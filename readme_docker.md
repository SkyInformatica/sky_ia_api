atualiza o json...

> docker build -t sky-metabase-plugin:1.0 .

para o container rodando...

> docker ps
> docker stop sky-plugin-container
> docker rm sky-plugin-container

inicia o novo

> docker run -d -p 3333:3000 --name sky-plugin-container sky-metabase-plugin:1.0

1. Conferir os logs do container
   Copiar
   docker logs -f sky_ia_api_container

2. Atualizando o container após correções
   Ajuste o Dockerfile ou o código.
   Re-crie a imagem:
   Copiar
   docker build -t sky_ia_api:1.1 .
   Pare e remova o antigo container:
   Copiar
   docker rm -f sky_ia_api_container
   Suba o novo:
   Copiar
   docker run -d -p 5000:8000 --name sky_ia_api_container sky_ia_api:1.1

3. (Opcional) docker-compose.yml
   Se quiser simplificar o run ou juntar com outros serviços:

Copiar
services:
api:
build: .
image: minha-api:latest
ports: - "8000:8000"
environment:
OPENAI_API_KEY: ${OPENAI_API_KEY}
Execute:

Copiar
docker compose up --build

Abra um shell:
Copiar
docker exec -it sky_ia_api_container bash
