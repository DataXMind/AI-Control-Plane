#!/usr/bin/env bash
# Sync policies.yml from ACP git checkout → VPS runtime mount → restart API.
# VPS prod reads /opt/acp/production-config (NOT the git tree). See aeos-acp-integration/RESULTS.md.
set -euo pipefail

ACP_GIT_DIR="${ACP_GIT_DIR:-/root/AI-Control-Plane}"
ACP_RUNTIME_CONFIG="${ACP_RUNTIME_CONFIG:-/opt/acp/production-config}"
POLICY_SRC="${ACP_GIT_DIR}/config/policies.yml"
POLICY_DST="${ACP_RUNTIME_CONFIG}/policies.yml"

if [[ ! -f "${POLICY_SRC}" ]]; then
  echo "Missing ${POLICY_SRC} — set ACP_GIT_DIR or git pull as root"
  exit 1
fi

grep -q 'admin.budget.freeze' "${POLICY_SRC}" || {
  echo "Source missing admin.budget.freeze — git pull origin master in ${ACP_GIT_DIR}"
  exit 1
}

echo "==> Copy ${POLICY_SRC} → ${POLICY_DST}"
cp "${POLICY_SRC}" "${POLICY_DST}"

echo "==> Restart minimal-acp-api"
docker restart minimal-acp-api-1
sleep 3

docker exec minimal-acp-api-1 grep admin.budget /etc/acp/config/policies.yml

curl -sf http://127.0.0.1:8000/health | jq .

curl -sf -X POST http://127.0.0.1:8000/policy/evaluate \
  -H 'Content-Type: application/json' \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"admin.budget.freeze","role":"backend"}' | jq .
