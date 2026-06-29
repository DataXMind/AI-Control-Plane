#!/usr/bin/env bash
# One-command ACP demo stack (RUN door). See docs/QUICKSTART.md
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/examples/minimal/docker-compose.yml"
IMAGE="${ACP_IMAGE:-ghcr.io/dataxmind/ai-control-plane:demo}"
PORT="${ACP_PORT:-8000}"
MODE="${ACP_UP_MODE:-auto}"
CONTAINER_NAME="${ACP_CONTAINER_NAME:-acp-demo}"

usage() {
  cat <<'EOF'
Usage: bash scripts/acp-up.sh [--compose | --ghcr | --down]

Start ACP in demo mode (fixture config, port 8000 by default).

  --compose   Build from repo via docker compose (default when repo present)
  --ghcr      Pull pre-built image from GHCR (no git clone required)
  --down      Stop stack started by this script

Environment:
  ACP_PORT=8000          Host port
  ACP_IMAGE=...          GHCR image (with --ghcr)
  ACP_UP_MODE=auto       auto | compose | ghcr

After start:
  export ACP_API_URL=http://127.0.0.1:8000
  curl -sf $ACP_API_URL/health
EOF
}

wait_health() {
  local url="http://127.0.0.1:${PORT}/health"
  echo "Waiting for ${url} ..."
  for _ in $(seq 1 30); do
    if curl -sf "${url}" >/dev/null 2>&1; then
      curl -sf "${url}" | python3 -m json.tool 2>/dev/null || curl -sf "${url}"
      echo ""
      echo "OK: ACP is up. export ACP_API_URL=http://127.0.0.1:${PORT}"
      return 0
    fi
    sleep 2
  done
  echo "ERROR: ACP did not become healthy within 60s" >&2
  return 1
}

up_compose() {
  if [[ ! -f "${COMPOSE_FILE}" ]]; then
    echo "ERROR: ${COMPOSE_FILE} not found — use --ghcr or clone the repo." >&2
    exit 1
  fi
  echo "Starting ACP via docker compose (${COMPOSE_FILE}) ..."
  docker compose -f "${COMPOSE_FILE}" up -d --build
}

down_compose() {
  if [[ -f "${COMPOSE_FILE}" ]]; then
    docker compose -f "${COMPOSE_FILE}" down
  fi
}

up_ghcr() {
  echo "Starting ACP from ${IMAGE} on port ${PORT} ..."
  docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
  docker pull "${IMAGE}"
  docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "${PORT}:8000" \
    -e ACP_CONFIG_DIR=/app/tests/fixtures/config \
    -e ACP_DATA_DIR=/data/acp \
    -v acp-demo-data:/data/acp \
    "${IMAGE}"
}

down_ghcr() {
  docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
}

resolve_mode() {
  case "${MODE}" in
    compose) echo compose ;;
    ghcr) echo ghcr ;;
    auto)
      if [[ -f "${COMPOSE_FILE}" ]]; then
        echo compose
      else
        echo ghcr
      fi
      ;;
    *)
      echo "ERROR: invalid ACP_UP_MODE=${MODE}" >&2
      exit 1
      ;;
  esac
}

ACTION=up
if [[ $# -gt 0 ]]; then
  case "$1" in
    --compose) MODE=compose ;;
    --ghcr) MODE=ghcr ;;
    --down) ACTION=down ;;
    -h|--help) usage; exit 0 ;;
    *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
  esac
fi

if [[ "${ACTION}" == down ]]; then
  down_compose || true
  down_ghcr || true
  echo "ACP stopped."
  exit 0
fi

RESOLVED="$(resolve_mode)"
if [[ "${RESOLVED}" == compose ]]; then
  up_compose
else
  up_ghcr
fi

wait_health
