#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
export ACP_API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"
pkill -f 'soak_staging.sh --loop' 2>/dev/null || true
sleep 1
nohup bash scripts/soak_staging.sh --loop 3600 --log /tmp/acp-soak-staging.log \
  >/tmp/acp-soak-nohup.out 2>&1 &
sleep 2
pgrep -af soak_staging || { echo "soak loop failed to start" >&2; exit 1; }
echo "OK: soak loop restarted (3600s interval, log /tmp/acp-soak-staging.log)"
