#!/usr/bin/env bash
set -euo pipefail

script_dir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
project_root="$(CDPATH= cd -- "$script_dir/../.." && pwd)"

exec python3 "$project_root/06_runtime/src/supestar_web/server.py" \
  --host "${SUPESTAR_HOST:-127.0.0.1}" \
  --port "${SUPESTAR_PORT:-4173}"
