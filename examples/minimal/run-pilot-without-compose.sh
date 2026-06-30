#!/usr/bin/env bash
# Mac pilot without Docker Compose plugin — build + run ACP with host config bind mount.
# Usage (from repo root):
#   bash examples/minimal/run-pilot-without-compose.sh
#   ACP_HOST_CONFIG_DIR=/opt/acp/config bash examples/minimal/run-pilot-without-compose.sh
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
CONFIG_DIR="${ACP_HOST_CONFIG_DIR:-${REPO_ROOT}/examples/minimal/production-config}"
PORT="${ACP_HOST_PORT:-8000}"
IMAGE="${ACP_PILOT_IMAGE:-acp-pilot:local}"
CONTAINER="${ACP_PILOT_CONTAINER:-acp-pilot}"
NETWORK="${ACP_PILOT_NETWORK:-acp-pilot-net}"
REDIS_CONTAINER="${ACP_REDIS_CONTAINER:-acp-pilot-redis}"
REDIS_PASSWORD="${REDIS_PASSWORD:-changeme-generate-strong-secret}"

if ! command -v docker >/dev/null 2>&1; then
  echo "ERROR: docker not found. Install Docker Desktop: brew install --cask docker" >&2
  exit 1
fi

if ! docker info >/dev/null 2>&1; then
  echo "ERROR: Docker daemon not running. Start Docker Desktop or: colima start" >&2
  exit 1
fi

if [[ ! -d "${CONFIG_DIR}" ]] || [[ ! -f "${CONFIG_DIR}/policies.yml" ]]; then
  echo "ERROR: Config missing at ${CONFIG_DIR}" >&2
  echo "  mkdir -p examples/minimal/production-config" >&2
  echo "  cp config/{policies,agents,projects}.yml examples/minimal/production-config/" >&2
  exit 1
fi

echo "Building ${IMAGE} ..."
docker build -f "${REPO_ROOT}/examples/minimal/Dockerfile" -t "${IMAGE}" "${REPO_ROOT}"

docker network inspect "${NETWORK}" >/dev/null 2>&1 || docker network create "${NETWORK}"

docker rm -f "${REDIS_CONTAINER}" "${CONTAINER}" 2>/dev/null || true

echo "Starting Redis ..."
docker run -d \
  --name "${REDIS_CONTAINER}" \
  --network "${NETWORK}" \
  --restart unless-stopped \
  redis:7-alpine \
  redis-server --requirepass "${REDIS_PASSWORD}"

echo "Starting ACP API on port ${PORT} ..."
docker run -d \
  --name "${CONTAINER}" \
  --network "${NETWORK}" \
  --restart unless-stopped \
  -p "${PORT}:8000" \
  -v "${CONFIG_DIR}:/etc/acp/config:ro" \
  -v acp-pilot-data:/data/acp \
  -e ACP_CONFIG_DIR=/etc/acp/config \
  -e ACP_DATA_DIR=/data/acp \
  -e "ACP_REDIS_URL=redis://:${REDIS_PASSWORD}@${REDIS_CONTAINER}:6379/0" \
  "${IMAGE}"

url="http://127.0.0.1:${PORT}/health"
echo "Waiting for ${url} ..."
for _ in $(seq 1 30); do
  if curl -sf "${url}" >/dev/null 2>&1; then
    curl -sf "${url}" | python3 -m json.tool 2>/dev/null || curl -sf "${url}"
    echo ""
    echo "OK: export ACP_API_URL=http://127.0.0.1:${PORT}"
    exit 0
  fi
  sleep 2
done

echo "ERROR: health check failed — docker logs ${CONTAINER}" >&2
exit 1
