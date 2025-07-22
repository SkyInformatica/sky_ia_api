1. Conferir os logs do container  
   $ docker logs -f sky_ia_api_container

2. Atualizando o container após correções

   **Pare e remova o antigo container**

   $ docker ps (opcional)
   $ docker stop sky_ia_api_container (opcional)
   $ docker rm -f sky_ia_api_container

   **Removar a imagem**
   $ docker rmi sky_ia_api:1.0

   **Re-crie a imagem**  
   $ docker build -t sky_ia_api:1.1 .

   **Suba o novo**
   $ docker run -d -p 5000:8000 --name sky_ia_api_container sky_ia_api:1.1

3. Abra um shell:
   $ docker exec -it sky_ia_api_container bash

4. (Opcional) docker-compose.yml

services:
api:
build: .
image: sky_ia_api:1.0
ports: - "8000:8000"

$ docker compose up --build
