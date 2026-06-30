#!/usr/bin/env bash
# ECC 48H post-verify deep audit — operator run (MSI/WSL)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
export ACP_API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"

ART_DIR="docs/governance/practice-evidence/ecc-48h-post-verify/artifacts"
mkdir -p "$ART_DIR"
LOG="$ART_DIR/deep-audit-$(date +%Y-%m-%d).log"
exec > >(tee "$LOG") 2>&1

echo "=== DEEP AUDIT $(date -Iseconds) master $(git rev-parse --short HEAD) ==="

echo "--- docker :8000 ---"
docker ps --filter publish=8000 --format '{{.Names}} {{.Image}} {{.Status}}' 2>/dev/null || true

echo "--- verify scripts ---"
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
bash scripts/verify_governance_memory.sh

echo "--- GHCR catalog version (local image if present) ---"
if docker image inspect ghcr.io/dataxmind/ai-control-plane:demo >/dev/null 2>&1; then
  docker run --rm ghcr.io/dataxmind/ai-control-plane:demo python3 -c \
    "from ai_control_plane.core.governance_catalog import GOVERNANCE_VERSION; print('GHCR_CATALOG', GOVERNANCE_VERSION)" \
    || echo "GHCR_RUN_FAIL"
else
  echo "GHCR image not local"
fi

echo "--- integrate examples (live API) ---"
python3 examples/integrate/python/before_tool_call.py
python3 examples/integrate/python/startup_health_gate.py
python3 examples/integrate/python/quota_check.py

echo "--- openapi static export diff ---"
python3 scripts/export_openapi.py
if git diff --quiet docs/openapi/openapi.json; then
  echo "OK: openapi.json in sync"
else
  echo "DRIFT: docs/openapi/openapi.json differs after export"
  git diff --stat docs/openapi/openapi.json
fi

echo "--- MCP pytest subset ---"
pytest tests/test_mcp_policy_integration.py tests/test_mcp_http_transport.py tests/test_mcp_git_server.py -q

echo "--- full suite ---"
pytest tests/ -q

echo "=== LOG: $LOG ==="
