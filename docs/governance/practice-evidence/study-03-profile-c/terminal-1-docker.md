# Study 03 — Terminal 1 (Docker API)

**Role:** Profile C — `docker compose` minimal stack  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study03/terminal01-cs03.md`

---

## Environment

```bash
cd /mnt/d/Projects/ai-control-plane
docker compose -f examples/minimal/docker-compose.yml up --build
# teardown:
docker compose -f examples/minimal/docker-compose.yml down
```

---

## Build & deploy

| Step | Result |
|------|--------|
| Image build | FINISHED 25.7s — `minimal-acp-api:latest` |
| Container | `minimal-acp-api-1` Recreated |
| Uvicorn | `http://0.0.0.0:8000` inside container |

---

## Request log (selected)

| Time (UTC) | Client | Method | Path | Status |
|------------|--------|--------|------|--------|
| 05:38:23–05:41:24 | 127.0.0.1 | GET | /health | 200 (healthcheck ~10s) |
| 05:39:43 | 172.27.0.1 | GET | /health | 200 |
| 05:39:50 | 172.27.0.1 | GET | /health | 200 |
| 05:39:50 | 172.27.0.1 | POST | /policy/evaluate | 200 |
| 05:39:51 | 172.27.0.1 | GET | /quota/rust-gateway | 200 |
| 05:39:51 | 172.27.0.1 | POST | /apex/trigger | 200 |
| 05:40:11 | 172.27.0.1 | GET | /governance/status | 200 |
| 05:40:46–47 | 172.27.0.1 | health + policy + quota + apex | 200 (soak iter 2) |
| 05:41:07 | 172.27.0.1 | GET | /governance/status | 200 |

`172.27.0.1` = WSL host → container bridge (operator + soak script).

---

## Teardown

```
Gracefully Stopping... Ctrl+C
Container minimal-acp-api-1 Stopped (exit 0)
docker compose down — container + network removed
```
