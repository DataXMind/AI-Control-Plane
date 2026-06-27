# Claude PB OpenAPI + examples CI packet — reconciliation

**Document ID:** ACP-GOV-PB-OPENAPI-CI-RECON-001  
**Audit date:** 2026-06-27  
**Source:** [`pb_openapi_and_examples_ci.html`](pb_openapi_and_examples_ci.html)  
**Baseline:** `master` / PR #118 branch · catalog v1.3.3

---

## Verdict

| Tab | Claude intent | Status |
|-----|---------------|--------|
| OpenAPI verify + document | Runtime `/docs` `/redoc` `/openapi.json` | ✅ **DONE** (recon PR) |
| examples CI job | Docker compose smoke in GitHub Actions | ✅ **DONE** (`examples/minimal/`) |
| "KHÔNG CÒN GÌ ĐỂ DELIVER" | **FALSE** | Operator gates PB-9/7/security@/12 remain |

---

## OpenAPI prompt — harsh audit

| Step | Claude | Reality | Action |
|------|--------|---------|--------|
| 1 | `FastAPI` without `docs_url=None` | ✅ `create_app()` enables docs | No `src/` change |
| 2 | Runtime `openapi.json` ≥10 paths | ✅ **13** paths | `verify_openapi_runtime.sh` (no `/openapi.json` in `paths{}`) |
| 3 | README API docs section | Missing | ✅ Added |
| 4 | OPEN_SOURCE_READINESS ✅ published | **Partial** | Runtime + static export ✅; **catalog PB-6 publish on flip** ⏳ |
| Title `AI Control Plane` | Expectation | Actual `ai-control-plane` | **No rename** — contract stability |

**Already existed before this packet:**

- `scripts/export_openapi.py` · `docs/openapi/openapi.json`
- `docs/openapi/README.md` · `CONTRACT_TESTS.md`
- `PUBLIC_BETA_SPRINT_PLAN.md` PB-6 ✅ export

**Do not:** Mark catalog `gates_remaining` PB-6 closed — flip-time publish remains.

---

## examples CI prompt — harsh audit

**Re-prompt audit (2026-06-22):** Claude packet references `@examples/docker-compose.yml` and `working-directory: examples` — **reject**. SSOT is `examples/minimal/`; job **`examples-minimal-smoke`** already on PR #118. **No second job.**

| Element | Claude | Action |
|---------|--------|--------|
| `working-directory: examples` | **WRONG** | `examples/minimal/docker-compose.yml` from repo root |
| `cp .env.example .env` | Optional | Not required — compose uses inline env |
| `needs: smoke` | ✅ | `examples-minimal-smoke` after smoke |
| Policy body without `role` | Weak | Use `role: backend` (SMK-03 parity) |
| `paths >= 5` OpenAPI | Low bar | Script requires **≥10** + key paths |

---

## Wired into project

| Artifact | Purpose |
|----------|---------|
| `scripts/verify_openapi_runtime.sh` | PB-spec-check operator gate |
| `tests/test_api_contract_snapshot.py` | L4 `test_openapi_json_minimum_paths` |
| `.github/workflows/ci.yml` | `examples-minimal-smoke` job |
| `README.md` | API docs section |
| `OPEN_SOURCE_READINESS.md` | Split runtime / static / publish |

---

## Verify (PACE Check)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_api_contract_snapshot.py -v
export ACP_API_URL=http://localhost:8000
bash scripts/verify_openapi_runtime.sh
docker compose -f examples/minimal/docker-compose.yml up --build -d
bash scripts/verify_governance_status_runtime.sh
bash scripts/verify_openapi_runtime.sh
```

**Drift:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) §10
