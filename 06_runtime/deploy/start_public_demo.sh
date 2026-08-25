#!/usr/bin/env bash
set -euo pipefail

port="${SUPESTAR_PORT:-4173}"

if ! command -v cloudflared >/dev/null 2>&1; then
  echo "cloudflared is required" >&2
  exit 1
fi

exec cloudflared tunnel --url "http://127.0.0.1:${port}" --no-autoupdate
