# AI Control Plane — Operator runbook

**Document ID:** ACP-OPS-RUNBOOK-001  
**Audience:** Fork operators, multi-host drills, Windows/WSL2 devs  
**Risk class:** N/A (documentation)  
**Practice evidence:** [`governance/practice-evidence/study-06-multi-host/`](governance/practice-evidence/study-06-multi-host/)

---

## Quick reference

| Scenario | Section |
|----------|---------|
| Local API (fixture) | [Run API server](#run-api-server) |
| Windows/WSL LAN bind | [Windows / WSL2 — LAN network bind](#windows--wsl2--lan-network-bind) |
| Remote via Tailscale | [Remote via Tailscale](#remote-via-tailscale) |
| Docker compose (PB-9) | [Docker compose](#docker-compose) |
| Multi-host Study 06 | [`study-06-multi-host/RUNBOOK.md`](governance/practice-evidence/study-06-multi-host/RUNBOOK.md) |
| Clean-machine fork (PB-7) | [`pb-7-clean-machine-fork/RUNBOOK.md`](governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md) |

---

## Run API server

### Native uvicorn (fixture profile — matches CI / smoke)

```bash
cd AI-Control-Plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config

# Local only: --host 127.0.0.1
# Multi-host / LAN: --host 0.0.0.0 (required for remote clients)
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

**Smoke:**

```bash
curl -sf http://127.0.0.1:8000/health | python3 -m json.tool
```

**Expected:** `status: ok`, `config_loaded: true`, `policy_rules_count: 8`.

---

## Windows / WSL2 — LAN network bind

By default WSL2 binds to an internal NAT address (`172.x.x.x` / `192.168.x.x` in WSL). Remote devices on your **home LAN** cannot reach `127.0.0.1` inside WSL. Publish port **8000** on the **Windows host** using portproxy.

**Operator evidence:** Study 06 Round A — [`TOPOLOGY_WINDOWS_MAC.md`](governance/practice-evidence/study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md).

### Step 1 — Start API binding to all interfaces (in WSL2)

```bash
cd /mnt/d/Projects/ai-control-plane   # adjust path
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config

pkill -f "uvicorn ai_control_plane" 2>/dev/null || true
uvicorn ai_control_plane.api.server:app \
  --host 0.0.0.0 \
  --port 8000 \
  --reload
```

Wait for `Application startup complete.`, then:

```bash
curl -sf http://127.0.0.1:8000/health | python3 -m json.tool
```

### Step 2 — Add Windows portproxy (Administrator PowerShell)

```powershell
# Resolve current WSL2 IP (changes after reboot — re-run this block)
$wslIp = (wsl hostname -I).Trim().Split(" ")[0]
Write-Host "WSL IP: $wslIp"

netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0 2>$null
netsh interface portproxy add v4tov4 `
  listenport=8000 `
  listenaddress=0.0.0.0 `
  connectport=8000 `
  connectaddress=$wslIp

netsh interface portproxy show all
```

### Step 3 — Add Windows Firewall inbound rule

```powershell
New-NetFirewallRule `
  -DisplayName "ACP API 8000" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 8000 `
  -Action Allow `
  -ErrorAction SilentlyContinue
```

Study 06 also used display name `ACP-Study06-TCP8000` — either rule name is fine; remove duplicates when cleaning up.

### Step 4 — Verify from second machine on same LAN

On Windows (sanity — portproxy):

```powershell
curl http://127.0.0.1:8000/health
```

On **client** machine (replace with your Windows **LAN** IP from `ipconfig`):

```bash
# Example from Study 06: WINDOWS_LAN_IP=192.168.1.59
curl -sf --connect-timeout 5 http://192.168.1.59:8000/health | python3 -m json.tool
```

Set client env:

```bash
export ACP_API_URL=http://192.168.1.59:8000
agentctl gov status
```

### Step 5 — Cleanup when done

```powershell
netsh interface portproxy delete v4tov4 listenport=8000 listenaddress=0.0.0.0
Remove-NetFirewallRule -DisplayName "ACP API 8000" -ErrorAction SilentlyContinue
Remove-NetFirewallRule -DisplayName "ACP-Study06-TCP8000" -ErrorAction SilentlyContinue
```

In WSL: `Ctrl+C` uvicorn.

### Notes

- **WSL2 IP changes on restart** — re-run Step 2 after reboot or WSL sleep.
- **Server logs** may show client as `192.168.16.1` (Windows NAT hop), not the remote LAN IP — expected with portproxy (Study 06 Round A).
- **WSL mirrored networking** (Win11): may work without portproxy — try `curl` from LAN first; if fail, use portproxy.
- **Tailscale overlay:** clients can use `100.x.x.x` Windows Tailscale IP; portproxy still needed for WSL→Windows publish unless using mirrored mode.

---

## Remote via Tailscale

For cross-network / VPS staging (Study 07), use Tailscale IP — **no LAN portproxy required on client path** when API runs on a Linux host with `0.0.0.0:8000`.

```bash
export ACP_API_URL=http://100.94.21.33:8000   # example ubuntu-vps
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
```

**Runbook:** [`study-07-cross-network/RUNBOOK.md`](governance/practice-evidence/study-07-cross-network/RUNBOOK.md).

---

## Docker compose

PB-9 staging / fork quick path:

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -sf http://localhost:8000/health | python3 -m json.tool
```

See [`examples/minimal/README.md`](../examples/minimal/README.md). On Windows, Docker Desktop publishes `localhost:8000` without portproxy.

---

## Troubleshooting

| Symptom | Fix |
|---------|-----|
| LAN client timeout | Re-run portproxy Admin; check firewall rule |
| `127.0.0.1` OK in WSL, LAN fail | `--host 0.0.0.0` + portproxy |
| Wrong rules count (8 vs 10) | `export ACP_CONFIG_DIR=tests/fixtures/config` on API host |
| Port 8000 busy | `ss -tlnp \| grep 8000` / stop Docker compose |

---

**Last updated:** 2026-06-26 — Windows/WSL LAN bind (Study 06 Round A; P-12)
