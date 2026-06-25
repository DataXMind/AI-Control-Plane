# Study 06 — Direction B — Mac server (native API)

**Captured:** 2026-06-25  
**Role:** API host (round 2)

## Setup

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

Worker **56713** (reloader 56711).

## Remote requests (Laptop `192.168.1.59`)

| Time (local) | Method | Path | Status |
|--------------|--------|------|--------|
| 17:03:54 | GET | /governance/status | 200 |
| 17:34:35 | POST | /policy/evaluate | 200 |
| 17:34:39 | POST | /policy/evaluate | 200 (agent2) |
| 17:34:39 | POST | /tasks | 200 (agent2) |

All from **`192.168.1.59`** — direct LAN (macOS native bind).

## Shutdown

Ctrl+C @ end of round B.
