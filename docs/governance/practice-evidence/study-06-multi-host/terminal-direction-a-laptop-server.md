# Study 06 — Direction A — Laptop server (WSL)

**Captured:** 2026-06-25  
**Role:** API host (round 1)  
**Path:** `/mnt/d/Projects/ai-control-plane`

## Setup

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

## Windows portproxy (Admin PowerShell)

```text
0.0.0.0:8000 → <WSL_LAN_IP_REDACTED>:8000
Firewall: ACP-Study06-TCP8000
curl.exe http://<LAN_IP_REDACTED>:8000/health → rules 8
```

## Local smoke

- `GET /health` 200 @ 15:14:44, 15:15:59 (`127.0.0.1`)
- `policy_rules_count`: **8**

## Remote burst (Mac client @ 16:59:55)

| Time (local) | Remote IP | Method | Path | Status |
|--------------|-----------|--------|------|--------|
| 16:59:55 | 192.168.16.1 | GET | /health | 200 |
| 16:59:55 | 192.168.16.1 | GET | /governance/status | 200 |
| 16:59:55 | 192.168.16.1 | POST | /policy/evaluate | 200 |
| 16:59:55 | 192.168.16.1 | POST | /policy/evaluate | 200 (agent2) |
| 16:59:55 | 192.168.16.1 | POST | /tasks | 200 (agent2) |

**Note:** `192.168.16.1` = Windows host NAT forwarding qua portproxy; Mac LAN = `192.168.1.99`.

## Shutdown

- Ctrl+C sau round A; portproxy :8000 deleted trên Windows
