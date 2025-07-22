# run.sh
# Este script executa o servidor FastAPI para a API de qualificação.
#!/usr/bin/env bash
set -euo pipefail

uvicorn sky_ia_api:app --host 0.0.0.0 --port 8000 --reload --workers 1 --log-level info --use-colors



