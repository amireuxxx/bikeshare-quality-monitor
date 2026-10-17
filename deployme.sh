#!/bin/bash
# deployme.sh: publish to the course Posit Connect server.
# Needs CONNECT_SERVER and CONNECT_API_KEY in a gitignored .env (see .env.example).
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
if [ -f .env ]; then
  set -a; . ./.env; set +a
fi
: "${CONNECT_SERVER:?Set CONNECT_SERVER in .env}"
: "${CONNECT_API_KEY:?Set CONNECT_API_KEY in .env}"
python -m pip install --quiet rsconnect-python
rsconnect deploy fastapi \
  --server "$CONNECT_SERVER" \
  --api-key "$CONNECT_API_KEY" \
  --title "BikeShare Quality Monitor" \
  --entrypoint backend.main:app \
  .
