#!/usr/bin/env bash
# Verify local GHCR demo image governance catalog matches repo SSOT.
# Usage: bash scripts/verify_ghcr_catalog.sh
# Exit 0: match or SKIP (no local image / docker unavailable)
# Exit 1: mismatch — republish via workflow or use compose build
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON=python3
if [[ -f "${ROOT}/.venv/bin/python" ]]; then
  PYTHON="${ROOT}/.venv/bin/python"
fi

IMAGE="${ACP_GHCR_IMAGE:-ghcr.io/dataxmind/ai-control-plane:demo}"

if ! command -v docker >/dev/null 2>&1; then
  echo "SKIP: docker not available"
  exit 0
fi

if ! docker image inspect "${IMAGE}" >/dev/null 2>&1; then
  echo "SKIP: local image not present — ${IMAGE}"
  echo "  Pull: docker pull ${IMAGE}"
  echo "  Or:   bash scripts/acp-up.sh --compose"
  exit 0
fi

EXPECTED=$("${PYTHON}" -c "from ai_control_plane.core.governance_catalog import GOVERNANCE_VERSION; print(GOVERNANCE_VERSION)")
ACTUAL=$(docker run --rm "${IMAGE}" python3 -c \
  "from ai_control_plane.core.governance_catalog import GOVERNANCE_VERSION; print(GOVERNANCE_VERSION)" \
  2>/dev/null || echo "RUN_FAIL")

if [[ "${ACTUAL}" == "RUN_FAIL" ]]; then
  echo "FAIL: could not read catalog from ${IMAGE}"
  exit 1
fi

if [[ "${EXPECTED}" != "${ACTUAL}" ]]; then
  echo "FAIL: GHCR catalog drift — image=${ACTUAL} repo=${EXPECTED}"
  echo "  Fix: gh workflow run \"Publish GHCR demo image\""
  echo "  Or:  docker compose -f examples/minimal/docker-compose.yml up --build -d"
  exit 1
fi

echo "OK: GHCR catalog ${ACTUAL} matches repo"
