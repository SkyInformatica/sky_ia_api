#!/bin/bash

# Script de Deploy Automatizado - Versão Fixa
# Usa sempre a tag 'latest' sobrescrevendo a imagem anterior

set -e  # Para o script se algum comando falhar

echo "=== Iniciando processo de deploy ==="

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para log colorido
log_info() {
  echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
  echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
  echo -e "${RED}[ERROR]${NC} $1"
}

# Configurações - VERSÃO FIXA
CONTAINER_NAME="sky_ia_api_container"
IMAGE_NAME="sky_ia_api:latest"  # Sempre a mesma tag
PORT_MAPPING="5000:8000"
GIT_REPO_DIR="sky_ia_api"
GIT_BRANCH="origin"

# Verificar se estamos no diretório correto
if [ ! -d "${GIT_REPO_DIR}" ]; then
  log_error "Diretório ${GIT_REPO_DIR} não encontrado!"
  log_error "Certifique-se de estar no diretório correto (onde está a pasta ${GIT_REPO_DIR})."
  exit 1
fi

# 1. Parar e remover container existente
log_info "Parando e removendo container existente..."
if docker ps -q --filter "name=${CONTAINER_NAME}" | grep -q .; then
  docker rm -f ${CONTAINER_NAME}
  log_info "Container ${CONTAINER_NAME} removido com sucesso"
else
  log_warn "Container ${CONTAINER_NAME} não estava rodando"
fi

# 2. Atualizar repositório
log_info "Atualizando repositório do Git..."
cd ${GIT_REPO_DIR}
git pull ${GIT_BRANCH}
cd ..
log_info "Repositório atualizado com sucesso"

# 3. Copiar novo Dockerfile
log_info "Copiando novo Dockerfile..."
if [ -f "${GIT_REPO_DIR}/Dockerfile" ]; then
  cp ${GIT_REPO_DIR}/Dockerfile ./Dockerfile
  log_info "Dockerfile copiado com sucesso"
else
  log_error "Dockerfile não encontrado em ${GIT_REPO_DIR}/Dockerfile"
  exit 1
fi

# 4. Construir nova imagem (sobrescreve a anterior)
log_info "Construindo imagem Docker ${IMAGE_NAME}..."
docker build -t ${IMAGE_NAME} .
log_info "Imagem ${IMAGE_NAME} construída com sucesso"

# 5. Executar novo container
log_info "Iniciando novo container..."
docker run -d -p ${PORT_MAPPING} --name ${CONTAINER_NAME} ${IMAGE_NAME}
log_info "Container ${CONTAINER_NAME} iniciado com sucesso"

# 6. Verificar se o container está rodando
sleep 3
if docker ps --filter "name=${CONTAINER_NAME}" --format "{{.Names}}" | grep -q "^${CONTAINER_NAME}$"; then
  log_info "✅ Deploy concluído com sucesso!"
  log_info "🚀 API rodando na porta 5000"
  log_info "📋 Para ver logs: docker logs ${CONTAINER_NAME}"
  log_info "🔄 Para acompanhar logs: docker logs -f ${CONTAINER_NAME}"
  
  echo ""
  log_info "Status do container:"
  docker ps --filter "name=${CONTAINER_NAME}" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}\t{{.Image}}"
  
  # Opcional: Testar se a API responde
  echo ""
  log_info "Testando conectividade..."
  sleep 2
  if curl -s -o /dev/null -w "%{http_code}" http://localhost:5000 | grep -q "200\|404\|422"; then
      log_info "✅ API respondendo na porta 5000"
  else
      log_warn "⚠️  API pode ainda estar inicializando..."
  fi
  
else
  log_error "❌ Falha no deploy - container não está rodando"
  log_error "Verifique os logs: docker logs ${CONTAINER_NAME}"
  exit 1
fi

# 7. Limpeza opcional de imagens órfãs
log_info "Limpando imagens órfãs..."
docker image prune -f >/dev/null 2>&1 || true

echo ""
echo "=== ✅ Processo de deploy finalizado com sucesso! ==="
echo "🌐 Acesse: http://localhost:5000"
echo "📊 Status: docker ps"
echo "📋 Logs: docker logs ${CONTAINER_NAME}"