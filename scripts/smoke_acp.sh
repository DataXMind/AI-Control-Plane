#!/usr/bin/env bash
# ACP smoke gate — SMK-01..SMK-05 (see docs/DEVELOPMENT_PROTOCOL.md §5.5)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

export ACP_CONFIG_DIR="${ACP_CONFIG_DIR:-$ROOT/tests/fixtures/config}"
export ACP_API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"

echo "=== ACP Smoke Gate (ACP_CONFIG_DIR=$ACP_CONFIG_DIR) ==="

echo "[SMK-01] P0 core import"
.venv/bin/python -c "from ai_control_plane.core import registry, telemetry; print('P0 OK')"

echo "[SMK-02..05] pytest smoke markers"
.venv/bin/pytest tests/test_smoke.py -v -m smoke --tb=short

echo "=== Smoke gate PASSED ==="
