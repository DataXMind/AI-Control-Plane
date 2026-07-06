# Study 07 — Terminal — Ubuntu VPS (API)

**Captured:** 2026-06-25  
**Host:** `ubuntu-vps` (`<VPS_TAILSCALE_IP>` Tailscale)  
**Path:** `/root/AI-Control-Plane`

## Setup

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

Worker **666511** (reloader 666506).

## Remote client: `<CLIENT_TAILSCALE_IP>` (msi Tailscale)

| Time (UTC/local) | Method | Path | Status |
|------------------|--------|------|--------|
| 11:09:24 | GET | /health | 200 |
| 11:16:14 | GET | /health | 200 |
| 11:17:48 | GET | /health | 200 |
| 11:17:57 | GET | /governance/status | 200 |
| 11:18:09 | POST | /policy/evaluate | 200 (agent2) |
| 11:18:10 | POST | /tasks | 200 (agent2) |
| 11:18:20–21 | soak burst | health, policy, quota, apex | 200 |

**Không** có request từ IP LAN laptop — chỉ Tailscale overlay.
