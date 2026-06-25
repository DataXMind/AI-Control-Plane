# Study 04 — Terminal 1 (server)

**Captured:** 2026-06-25  
**Source:** `TestCase/Study04/terminal1-cs04.md`

## Pre-clean

```bash
pkill -f "uvicorn ai_control_plane" 2>/dev/null || true
docker compose -f examples/minimal/docker-compose.yml down 2>/dev/null || true
ss -tlnp | grep ':8000'  # → port 8000 free
```

## 4a — fixture :8000

- Reloader **6547**, worker **6549**
- `GET /health` 200 @ 14:05:01 (latency 26.85 ms)
- Ctrl+C shutdown

## 4b — fixture :8002

- Reloader **6608**, worker **6610**
- `GET /health` 200 @ 14:07:08
- `GET /governance/status` 200 @ 14:07:19
- Ctrl+C; `ss -tlnp | grep 8002` empty

## 4c — fixture then shipped :8000

**Fixture phase (worker 6649):**

- health 200 @ 14:08:35, 14:09:00
- governance 200 @ 14:09:05
- Ctrl+C

**Shipped phase (worker 6676):**

```bash
unset ACP_CONFIG_DIR
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

- `GET /health` 200 @ 14:10:11
- Ctrl+C
