#!/usr/bin/env bash
# ACP smoke gate — SMK-01..SMK-06 (see docs/DEVELOPMENT_PROTOCOL.md §5.5)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export ACP_CONFIG_DIR="${ACP_CONFIG_DIR:-$ROOT/tests/fixtures/config}"

PYTHON="${ROOT}/.venv/bin/python"
PYTEST="${ROOT}/.venv/bin/pytest"
UVICORN="${ROOT}/.venv/bin/uvicorn"

if [ "${1:-}" == "--live" ]; then
  echo "Starting uvicorn for live smoke..."
  ACP_CONFIG_DIR="$ACP_CONFIG_DIR" "$UVICORN" ai_control_plane.api.server:app --host 127.0.0.1 --port 18000 &
  SERVER_PID=$!
  trap 'kill "$SERVER_PID" 2>/dev/null || true' EXIT
  for _ in $(seq 1 15); do
    if curl -sf "http://localhost:18000/health" >/dev/null 2>&1; then
      break
    fi
    sleep 1
  done
  curl -sf "http://localhost:18000/health" | python3 -m json.tool
  curl -sf -X POST "http://localhost:18000/policy/evaluate" \
    -H "Content-Type: application/json" \
    -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","args":{}}' \
    | python3 -m json.tool
  kill "$SERVER_PID"
  trap - EXIT
  echo "Live smoke done."
else
  echo "Running TestClient smoke (CI mode)..."
  ACP_CONFIG_DIR="$ACP_CONFIG_DIR" "$PYTEST" tests/test_smoke.py -v -m smoke --tb=short
fi
