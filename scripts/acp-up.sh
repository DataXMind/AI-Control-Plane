#!/usr/bin/env bash
# One-command ACP demo stack (RUN door). See docs/QUICKSTART.md
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
COMPOSE_FILE="${REPO_ROOT}/examples/minimal/docker-compose.yml"
IMAGE="${ACP_IMAGE:-ghcr.io/dataxmind/ai-control-plane:demo}"
PORT="${ACP_PORT:-8000}"
MODE="${ACP_UP_MODE:-auto}"
CONTAINER_NAME="${ACP_CONTAINER_NAME:-acp-demo}"
GHCR_FALLBACK="${ACP_UP_GHCR_FALLBACK:-auto}"

usage() {
  cat <<'EOF'
Usage: bash scripts/acp-up.sh [--compose | --ghcr | --down] [--no-fallback]

Start ACP in demo mode (fixture config, port 8000 by default).

  --compose      Build from repo via docker compose (default when repo present)
  --ghcr         Pull pre-built image from GHCR (falls back to compose in repo)
  --down         Stop stack started by this script
  --no-fallback  With --ghcr: do not fall back to compose on pull failure

Environment:
  ACP_PORT=8000                 Host port
  ACP_IMAGE=...                 GHCR image (with --ghcr)
  ACP_UP_MODE=auto              auto | compose | ghcr
  ACP_UP_GHCR_FALLBACK=auto     auto | never  (auto = compose fallback when in repo)

After start:
  export ACP_API_URL=http://127.0.0.1:8000
  curl -sf $ACP_API_URL/health

GHCR image not found or "denied"?
  1. GitHub → Actions → "Publish GHCR demo image" → Run workflow
  2. Private repo: docker login ghcr.io  (PAT with read:packages)
  3. Or use: bash scripts/acp-up.sh --compose
EOF
}

print_ghcr_help() {
  cat <<EOF >&2

GHCR pull failed for: ${IMAGE}

Common causes:
  1. Image not published yet
     → GitHub: Actions → "Publish GHCR demo image" → Run workflow
     → Or: gh workflow run "Publish GHCR demo image"

  2. Package is private (repo is private until PB-12)
     → echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USER --password-stdin
     → PAT needs scope: read:packages

  3. Wrong image tag
     → export ACP_IMAGE=ghcr.io/dataxmind/ai-control-plane:demo

Compose path (no GHCR): bash scripts/acp-up.sh --compose
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
    echo "ERROR: ${COMPOSE_FILE} not found — clone the repo or fix GHCR pull." >&2
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

run_ghcr_container() {
  docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true
  docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p "${PORT}:8000" \
    -e ACP_CONFIG_DIR=/app/tests/fixtures/config \
    -e ACP_DATA_DIR=/data/acp \
    -v acp-demo-data:/data/acp \
    "${IMAGE}"
}

up_ghcr() {
  echo "Starting ACP from ${IMAGE} on port ${PORT} ..."
  local pull_log
  pull_log="$(mktemp)"
  if docker pull "${IMAGE}" >"${pull_log}" 2>&1; then
    rm -f "${pull_log}"
    run_ghcr_container
    return 0
  fi

  cat "${pull_log}" >&2
  rm -f "${pull_log}"
  print_ghcr_help

  if [[ "${GHCR_FALLBACK}" == "auto" && -f "${COMPOSE_FILE}" ]]; then
    echo "" >&2
    echo "Falling back to docker compose (repo present) ..." >&2
    up_compose
    return 0
  fi

  echo "ERROR: GHCR start failed and compose fallback disabled." >&2
  echo "Set ACP_UP_GHCR_FALLBACK=auto or run: bash scripts/acp-up.sh --compose" >&2
  exit 1
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
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --compose) MODE=compose ;;
      --ghcr) MODE=ghcr ;;
      --down) ACTION=down ;;
      --no-fallback) GHCR_FALLBACK=never ;;
      -h|--help) usage; exit 0 ;;
      *) echo "Unknown option: $1" >&2; usage; exit 1 ;;
    esac
    shift
  done
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
