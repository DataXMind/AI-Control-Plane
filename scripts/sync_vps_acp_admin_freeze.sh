#!/usr/bin/env bash
# Sync admin.budget.freeze RBAC to VPS minimal-acp-api and verify B2 allow-path.
set -euo pipefail

ACP_DIR="${ACP_DIR:-$HOME/AI-Control-Plane}"
POLICY_SRC="${ACP_DIR}/config/policies.yml"

[[ -f "${POLICY_SRC}" ]] || { echo "Missing ${POLICY_SRC}"; exit 1; }
grep -q 'admin.budget.freeze' "${POLICY_SRC}" || { echo "config/policies.yml missing admin.budget.freeze"; exit 1; }

echo "==> Copy policies to running ACP mount (adjust if your VPS path differs)"
# Example: docker cp or volume bind — operator edits minimal compose config_dir
echo "    git -C ${ACP_DIR} pull && restart minimal-acp-api"

docker restart minimal-acp-api-1 2>/dev/null || true
sleep 3

curl -sf http://127.0.0.1:8000/health | jq .

curl -sf -X POST http://127.0.0.1:8000/policy/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"admin.budget.freeze","role":"backend"}' | jq .
