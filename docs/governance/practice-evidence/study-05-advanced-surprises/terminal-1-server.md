# Study 05 — Terminal 1 (server)

**Captured:** 2026-06-25  
**Source:** `TestCase/Study05/terminal01-cs05.md`

## 5b / 5c — uvicorn fixture :8000

- Worker **6937** (reloader 6935)
- `POST /policy/evaluate` 200 @ 14:24:58, 14:25:53
- `POST /policy/evaluate` **503** @ 14:26:29 (invalid body — drill 5c)
- Ctrl+C

## 5d / 5e — Docker

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl localhost:8000/health  # policy_rules_count: 8
```

- `governance_version` → **1.0** (without code change)
- `docker compose up -d --build` again → still **1.0**
- `docker compose down`

## 5f — uvicorn + identity verify

- Worker **7345** (reloader 7343)
- `POST /identity/verify` **503** @ 14:32:31
