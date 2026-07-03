#!/usr/bin/env bash
# Fail-closed: ACP unreachable must block run_tool_guarded (uses closed local port).
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
RUNNER="$REPO_ROOT/examples/integrate/python/run_tool_guarded.py"

export ACP_API_URL="http://127.0.0.1:9"
export ACP_PROJECT_ID="rust-gateway"
export ACP_AGENT_ID="${ACP_AGENT_ID:-agent1}"
export ACP_ROLE="${ACP_ROLE:-infra}"
export ACP_TIMEOUT_S="1.0"

if python3 "$RUNNER" --tool git_read -- echo ok 2>/dev/null; then
  echo "FAIL: command ran while ACP unreachable" >&2
  exit 1
fi

echo "PASS: fail-closed — command blocked when ACP unreachable"
