#!/usr/bin/env bash
# P-15 — k6 policy evaluate load smoke (optional; skips if k6 missing)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

K6_BIN=""
if command -v k6 >/dev/null 2>&1; then
  K6_BIN="k6"
elif [[ -x "${ROOT}/.tools/k6" ]]; then
  K6_BIN="${ROOT}/.tools/k6"
fi

if [[ -z "${K6_BIN}" ]]; then
  echo "SKIP: k6 not installed — see benchmarks/k6/README.md"
  echo "  Tip: download to .tools/k6 or install from https://k6.io/docs/get-started/installation/"
  exit 0
fi

export ACP_API_URL="${ACP_API_URL:-http://127.0.0.1:8000}"
ARTIFACT_DIR="${K6_ARTIFACT_DIR:-}"
SUMMARY_ARGS=()
if [[ -n "${ARTIFACT_DIR}" ]]; then
  mkdir -p "${ARTIFACT_DIR}"
  SUMMARY_ARGS=(--summary-export "${ARTIFACT_DIR}/k6-summary.json")
fi

echo "k6 policy smoke @ ${ACP_API_URL} (VUS=${K6_VUS:-10} DURATION=${K6_DURATION:-30s})"
"${K6_BIN}" run "${SUMMARY_ARGS[@]}" benchmarks/k6/policy_evaluate.js
