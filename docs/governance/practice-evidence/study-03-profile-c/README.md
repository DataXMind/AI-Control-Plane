# Study 03 — Profile C (Docker / PB-9 soak) — PENDING

**Profile:** C — `docker compose -f examples/minimal/docker-compose.yml`  
**Expected vs Study 02:**

| Field | Study 02 (uvicorn shipped) | Study 03 (Docker) |
|-------|---------------------------|-------------------|
| Runtime | native uvicorn | container |
| `ACP_CONFIG_DIR` in container | N/A | `tests/fixtures/config` |
| `policy_rules_count` | 10 | **8** (fixture in compose) |

**Prerequisite:** Stop uvicorn on `:8000` before `docker compose up`.

Evidence files will be added after operator run.
