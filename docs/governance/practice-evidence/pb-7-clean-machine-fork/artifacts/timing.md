# PB-7 timing — CLEAN Ubuntu @ MSI

**Run date:** 2026-06-27 (UTC)  
**Path:** A — Docker

| Milestone | Elapsed (approx) | Notes |
|-----------|------------------|-------|
| T0 `git clone` | 0 | Prior to compose (operator) |
| T+compose build | **~54s** | First pull + `pip install` in image |
| T+container start | **~1s** | `minimal-acp-api-1` Started |
| T+health | **< 2 min** from compose start | `status: ok` |
| T+policy allow/deny | **< 3 min** | allow + deny fail-closed |
| T+governance verify | **< 5 min** | After CRLF fix on verify script |
| T+agentctl (optional) | **< 6 min** | `docker exec … agentctl assign` |
| T+teardown | — | `docker compose down` |

**Total wall-clock (clone → teardown):** **≤ 15 min** — **PASS**

**Incident:** `verify_governance_status_runtime.sh` failed once with `set: pipefail` (CRLF on `/mnt/d`); fixed via `sed -i 's/\r$//'` then **PASS** `1.3.3` · 13 patterns.
