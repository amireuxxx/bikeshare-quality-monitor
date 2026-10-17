#!/bin/bash
# manifestme.sh: write manifest.json for Posit Connect.
# Run it inside a virtual environment built with the Python version in .python-version (3.12):
#   python3.12 -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"
want="$(cat .python-version)"
have="$(python -c 'import sys; print("%d.%d" % sys.version_info[:2])')"
if [ "$want" != "$have" ]; then
  echo "Python is $have but .python-version says $want. Activate a $want environment first." >&2
  exit 1
fi
python -m pip install --quiet rsconnect-python
rsconnect write-manifest fastapi . --entrypoint backend.main:app
echo "Wrote manifest.json (Python $have). Commit it, then run ./deployme.sh"
