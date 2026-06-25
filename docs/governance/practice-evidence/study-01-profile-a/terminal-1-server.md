# Study 01 — Terminal 1 (API server)

**Role:** Profile A — uvicorn + fixture config  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study01/terminal1.md`

---

## Environment

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

---

## Key events

| Time (local) | Event | Status |
|--------------|-------|--------|
| Pre-run | `pip install -e ".[dev]"` | ✅ Success |
| Attempt 1 | uvicorn `:8000` | ❌ `[Errno 98] Address already in use` |
| Attempt 2 | uvicorn `:8000` | ✅ `Uvicorn running on http://127.0.0.1:8000` |
| 12:13:06 | `GET /health` | 200, latency 18.2 ms |
| 12:13:59 | `GET /governance/status` | 200, latency 5.61 ms |
| 12:14:20 | `GET /governance/status` | 200, latency 0.3 ms |
| 12:15:42 | `POST /policy/evaluate` (allow path) | 200, latency 8.5 ms |
| 12:16:08 | `POST /policy/evaluate` (deny path) | 200, latency 0.54 ms |

---

## Process

- Reloader PID: **4663**
- Server PID: **4668**
- Watch dir: `/mnt/d/Projects/ai-control-plane`
