#!/usr/bin/env bash
# P-15 — k6 policy evaluate load smoke (optional; skips if k6 missing)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! command -v k6 >/dev/null 2>&1; then
  echo "SKIP: k6 not installed — see benchmarks/k6/README.md"
  exit 0
fi

export ACP_API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"
echo "k6 policy smoke @ ${ACP_API_URL} (VUS=${K6_VUS:-10} DURATION=${K6_DURATION:-30s})"
k6 run benchmarks/k6/policy_evaluate.js
