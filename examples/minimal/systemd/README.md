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

## After reboot

`acp-staging` starts Docker stack; `acp-soak` waits for `/health` then runs hourly soak into `/var/log/acp-soak-staging.log`.

## Stop

```bash
sudo systemctl disable --now acp-soak.service acp-staging.service
```
