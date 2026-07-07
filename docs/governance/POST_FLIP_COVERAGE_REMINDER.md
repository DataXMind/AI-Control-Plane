# Post-flip coverage reminder — ~2026-07-07

**Document ID:** ACP-GOV-POST-FLIP-COVERAGE-REMINDER-001  
**Calendar target:** **~2026-07-07** (C1-02 pre-flip, after Day 14 ~07-06)  
**SSOT report:** [`COVERAGE_IMPROVEMENT_REPORT.md`](COVERAGE_IMPROVEMENT_REPORT.md)

> **Note:** Tier 1 (`api/server.py` error + approve) was completed **early** (2026-07-01) in PR #178 — this reminder covers **verification + Tier 3 backlog**.

---

## Operator checklist @ ~07-07

**Pre-flip C1-02 (executed early 2026-07-06 on MSI):** smoke **8/8** · gov **1.6.0·17** · OpenAPI export + verify · **221** pytest PASS — see [`pb-12-public-flip/RESULTS.md`](practice-evidence/pb-12-public-flip/RESULTS.md).

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/ -q --cov=ai_control_plane --cov-report=term:skip-covered   # expect ≥85%
pytest tests/test_smoke.py -m smoke -q                                    # 8/8
bash scripts/verify_governance_status_runtime.sh
python scripts/export_openapi.py && git diff --exit-code docs/openapi/openapi.json
```

- [x] Smoke **8/8** @ 2026-07-06 (pre-flip)
- [x] `verify_governance_status_runtime.sh` PASS @ 2026-07-06
- [x] `export_openapi.py` — no drift (merged pre-flip)
- [x] `verify_openapi_runtime.sh` PASS @ 2026-07-06
- [x] Full pytest suite **221** PASS @ 2026-07-06
- [ ] Local `--cov` ≥ **85%** (run on MSI/WSL — not re-run @ 07-07 yet)
- [ ] Codecov project green vs **85%** target
- [ ] Re-read residual gaps in [`COVERAGE_IMPROVEMENT_REPORT.md`](COVERAGE_IMPROVEMENT_REPORT.md) § Residual gaps
- [ ] Open/follow Tier 3 issue: MCP E2E CI + OIDC test matrix (ADR-002)

## Tier 3 backlog (do not block PB-12)

| Item | Trigger |
|------|---------|
| `mcp/git_server.py` ≥85% + E2E CI | MCP contract implementation |
| `core/identity.py` JWKS paths | ADR-002 OIDC |
| `config/loader.py` validation matrix | 1.0.0 schema freeze |
| `cli/logs.py --follow` | Tier 2b |

**Do not** raise `fail_under` to 95% before GA.

**Last updated:** 2026-07-07 · C1-02 pre-flip ticks @ 07-06 · coverage/Codecov/Tier 3 still open
