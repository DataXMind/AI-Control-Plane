# Post-merge runtime verify — MSI WSL

**Captured:** 2026-06-27 (UTC)  
**Host:** MSI WSL (`/mnt/d/Projects/ai-control-plane`)  
**Label:** **WARM** — operator re-verify after PR #118 merge + PB-9 PM tick  
**Branch @ run:** `master` @ `375ef14` (#118 merged + verdict stamp)  
**Stack:** Docker `minimal-acp-api-1`

## Procedure (PACE)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_api_contract_snapshot.py tests/test_smoke.py -m smoke -v
docker compose -f examples/minimal/docker-compose.yml up --build -d
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log
docker compose -f examples/minimal/docker-compose.yml down   # optional teardown
```

## Operator output

```text
pytest -m smoke: 8 passed, 3 deselected
OK: governance/status runtime verify 1.3.3 13 patterns
OK: openapi runtime verify 3.1.0 13 paths
2026-06-27T11:53:35Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

## Analysis

| Check | Result | Notes |
|-------|--------|-------|
| Smoke gate | **8/8 PASS** | SMK-01..06c |
| `governance_version` | **1.3.3** | Catalog SSOT |
| `lessons_patterns` | **13** | Incl. P-13 kill switch |
| OpenAPI runtime | **3.1.0 · 13 paths** | `verify_openapi_runtime.sh` |
| PB-9 soak iter | **PASS** | PM tick @ 11:53Z |

**Does not close:** PB-7 CLEAN fork · PB-9 Day 14 (~07-06) · security@ · PB-12 gates.

## Verdict

**PASS** — post-merge PACE + PB-9 PM tick @ MSI WARM · `master` @ `375ef14`.
