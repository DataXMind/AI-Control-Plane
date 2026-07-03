#!/usr/bin/env bash
# Policy smoke matrix — requires live ACP at ACP_API_URL.
set -euo pipefail

: "${ACP_API_URL:?set ACP_API_URL}"
BASE="${ACP_API_URL%/}/policy/evaluate"

eval_case() {
  local label="$1" json="$2" expect="$3"
  local allowed
  allowed=$(curl -sf -X POST "$BASE" -H "Content-Type: application/json" -d "$json" \
    | python3 -c "import sys,json; print(json.load(sys.stdin).get('allowed'))")
  if [[ "$allowed" == "$expect" ]]; then
    echo "PASS $label (allowed=$allowed)"
  else
    echo "FAIL $label expected allowed=$expect got $allowed" >&2
    return 1
  fi
}

eval_case "agent1 git_read" \
  '{"agent_id":"agent1","project_id":"rust-gateway","tool_name":"git_read","role":"infra"}' \
  "True"

eval_case "agent2 build.rust" \
  '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"build.rust","role":"backend"}' \
  "True"

eval_case "agent2 k8s_apply deny" \
  '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"k8s_apply","role":"backend"}' \
  "False"

eval_case "agent3 k8s_apply deny" \
  '{"agent_id":"agent3","project_id":"rust-gateway","tool_name":"k8s_apply","role":"reviewer"}' \
  "False"

eval_case "unknown agent deny" \
  '{"agent_id":"unknown","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  "False"

echo "All policy smoke cases passed."
