#!/bin/bash
# testme.sh: run the app locally, then open http://localhost:8000/ (API docs at /docs).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
python -m uvicorn backend.main:app --host 0.0.0.0 --port "${PORT:-8000}"
