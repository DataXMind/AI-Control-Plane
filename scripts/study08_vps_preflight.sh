#!/usr/bin/env bash
# Study 08 VPS preflight — run ON ubuntu-vps as operator (Gate B approved)
set -euo pipefail
REPO="${REPO:-$HOME/AI-Control-Plane}"
cd "$REPO"
git pull origin master
docker compose -f examples/minimal/docker-compose.yml down || true
# Stop systemd staging if active
if systemctl is-active --quiet acp-staging.service 2>/dev/null; then
  sudo systemctl stop acp-staging.service
fi
source .venv/bin/activate
unset ACP_CONFIG_DIR
pkill -f "uvicorn ai_control_plane.api.server" || true
sleep 1
nohup uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000 \
  > /tmp/acp-study08-uvicorn.log 2>&1 &
sleep 2
curl -sf http://127.0.0.1:8000/health | python3 -m json.tool
curl -sf http://127.0.0.1:8000/governance/status | python3 -m json.tool | head -40
echo "Study 08 Phase 2–3 complete. Run laptop Phase 4: ACP_API_URL=http://100.94.21.33:8000 bash scripts/soak_staging.sh"
