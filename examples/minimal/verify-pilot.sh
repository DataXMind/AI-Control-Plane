#!/usr/bin/env bash
# Verify pilot stack from examples/minimal (after docker compose up).
set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${DIR}"

PORT="${ACP_HOST_PORT:-8000}"
URL="http://127.0.0.1:${PORT}/health"
COMPOSE=(docker compose -f docker-compose.yml -f docker-compose.production.yml)
if [[ -f .env.production ]]; then
  COMPOSE+=(--env-file .env.production)
fi

echo "=== docker compose ps ==="
"${COMPOSE[@]}" ps

echo ""
echo "=== acp-api logs (last 30 lines) ==="
"${COMPOSE[@]}" logs acp-api --tail 30

echo ""
echo "=== health ${URL} ==="
for i in $(seq 1 15); do
  if body="$(curl -sf "${URL}" 2>/dev/null)"; then
    echo "${body}" | python3 -m json.tool
    echo ""
    echo "OK: export ACP_API_URL=${URL%/health}"
    exit 0
  fi
  echo "  attempt ${i}/15 — waiting..."
  sleep 2
done

echo "ERROR: health check failed" >&2
echo "Try: curl -v ${URL}" >&2
exit 1
