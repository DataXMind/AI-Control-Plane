# Study 02 — Terminal 1 (API server)

**Role:** Profile B — uvicorn + shipped `config/`  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study02/terminal01-casestudy02.md`

---

## Environment

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
unset ACP_CONFIG_DIR
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

---

## Key events

| Time (local) | Event | Status |
|--------------|-------|--------|
| ~12:26 | uvicorn `:8000` | ✅ `Application startup complete` |
| 12:26:45 | `GET /health` | 200, latency 12.75 ms |
| 12:27:02 | `GET /governance/status` | 200, latency 4.2 ms |
| 12:29:28 | `POST /policy/evaluate` | 200, `agent_id=agent2`, latency 3.46 ms |
| 12:29:28 | `POST /tasks` | 200, `agent_id=agent2`, latency 2.65 ms |

---

## Process

- Reloader PID: **4947**
- Server PID: **5010**
- Config source: shipped `config/` (no `ACP_CONFIG_DIR` override)

**Note:** `POST /tasks` follows `agentctl assign` from T2 — confirms CLI → HTTP bridge (Invariant #4).
