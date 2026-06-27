# VPS staging 24/7 — systemd (Option B: Docker)

PB-9 parity stack: `examples/minimal/docker-compose.yml`. Use **Docker**, not bare uvicorn, so healthcheck + `ACP_DATA_DIR` volume match local staging.

## Install (on `ubuntu-vps`)

Adjust `ACP_REPO` if the clone path differs.

```bash
export ACP_REPO=/root/AI-Control-Plane
sudo cp "$ACP_REPO/examples/minimal/systemd/"*.service /etc/systemd/system/
sudo sed -i "s|/root/AI-Control-Plane|$ACP_REPO|g" /etc/systemd/system/acp-staging.service /etc/systemd/system/acp-soak.service
sudo systemctl daemon-reload
sudo systemctl enable --now acp-staging.service
sudo systemctl enable --now acp-soak.service
```

## Verify

```bash
sudo systemctl status acp-staging.service acp-soak.service
docker compose -f "$ACP_REPO/examples/minimal/docker-compose.yml" ps
tail -3 /var/log/acp-soak-staging.log
```

### Governance runtime (catalog v1.3+)

After `git pull` touching `src/`:

```bash
cd "$ACP_REPO"
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
```

Expected: `OK: governance/status runtime verify 1.3.3 13 patterns`.  
Troubleshooting: [`../../../docs/governance/practice-evidence/governance-status-v13-verify/RESULTS.md`](../../../docs/governance/practice-evidence/governance-status-v13-verify/RESULTS.md).

## After reboot

`acp-staging` starts Docker stack; `acp-soak` waits for `/health` then runs hourly soak into `/var/log/acp-soak-staging.log`.

## Stop

```bash
sudo systemctl disable --now acp-soak.service acp-staging.service
```
