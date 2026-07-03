#!/usr/bin/env bash
# Fail-closed policy check — exit 0 allow, 1 deny.
set -euo pipefail

: "${ACP_API_URL:?set ACP_API_URL}"
: "${ACP_PROJECT_ID:=rust-gateway}"
: "${ACP_AGENT_ID:?set ACP_AGENT_ID}"
: "${ACP_ROLE:?set ACP_ROLE}"
TOOL_NAME="${1:?usage: acp_evaluate.sh <tool_name>}"

payload=$(ACP_TOOL="$TOOL_NAME" python3 -c "
import json, os
print(json.dumps({
    'agent_id': os.environ['ACP_AGENT_ID'],
    'project_id': os.environ.get('ACP_PROJECT_ID', 'rust-gateway'),
    'tool_name': os.environ['ACP_TOOL'],
    'role': os.environ['ACP_ROLE'],
}))
")

curl -sf -X POST "${ACP_API_URL%/}/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d "$payload" \
  | python3 -c "import sys,json; b=json.load(sys.stdin); print(b.get('reason','')); sys.exit(0 if b.get('allowed') else 1)"
