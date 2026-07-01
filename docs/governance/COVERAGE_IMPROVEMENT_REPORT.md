# Coverage improvement report — pre–Public Beta

**Document ID:** ACP-GOV-COVERAGE-REPORT-001  
**Status:** **ACTIVE** — publish before PB-12 repo flip  
**Baseline:** `master` @ post-merge of this PR · catalog **v1.5.0**  
**Audience:** Maintainers · operators · clients evaluating ACP quality gates  
**Related:** [`OPEN_SOURCE_READINESS.md`](../OPEN_SOURCE_READINESS.md) · [`codecov.yml`](../../codecov.yml) · Codecov dashboard

---

## Executive summary

| Metric | Before (2026-07-01) | After (this PR) | Gate |
|--------|---------------------|-----------------|------|
| **Total line coverage** | **~82.8%** | **~86.3%** | `fail_under` **85%** |
| **pytest collected** | 181 | **221+** | CI Full suite |
| **`api/server.py`** | 74% | **~88%** | Tier 1 target met |
| **`cli/_http.py`** | 65% | **~78%** | Tier 2 partial |
| **`mcp/git_server.py`** | 64% | **~71%** | Tier 3 partial |
| **Smoke gate** | 8/8 | **8/8** | Unchanged — merge blocker |

100% coverage was **never** a project gate. Historical floor: **70%** (Milestone B Sprint 1). This PR raises the floor to **85%** for pre–public-beta confidence while documenting residual gaps.

---

## Why 100% was not pursued

1. **Governance scope** — PB-9 calendar + PB-12 flip blockers are soak + human GO, not Codecov 100%.
2. **Experimental modules** — MCP git facade (`[mcp-unverified]`), SAPAL `apex/` demoted @ 0.x.
3. **Deferred identity** — OIDC/JWKS full paths (ADR-002 PROPOSED).
4. **ROI** — Core policy path (`policies.py` ~99%) and smoke 8/8 protect client HTTP integration; remaining gaps are operator CLI UX and MCP subprocess edges.

See prior analysis in operator playbook § optional verify and [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md).

---

## Tier execution log

### Tier 1 — API server error + approve ✅ (early — pre–07-07)

**Tests:** `tests/test_api_server_errors.py`

| Area | Cases added |
|------|-------------|
| `/policy/evaluate` | invalid body, unknown agent, wrong project, timeout, engine exception |
| `/policy/approve` | success, unknown id, internal failure |
| `/tasks`, `/status` | unknown project, store failures |
| `/quota/*` | unknown project/agent/profile, store failures |
| `/telemetry/events`, `/apex/*` | store / pipeline failures |
| `/identity/verify` | missing claims, JWT error, 503 |

**Result:** `api/server.py` **74% → ~88%**

### Tier 2 — CLI HTTP + logs ✅ (partial)

**Tests:** `tests/test_cli_http_errors.py`, `tests/test_cli_logs.py`, `tests/test_cli_main_entry.py`

| File | Before | After | Residual |
|------|--------|-------|----------|
| `cli/_http.py` | 65% | ~78% | apex trigger non-200, some timeout branches |
| `cli/logs.py` | 47% | ~59% | `--follow` loop |
| `cli/main.py` | 0% | **100%** | entry re-export |
| `cli/assign.py`, `status.py` | 67–68% | unchanged | Typer error exits — backlog |

### Tier 3 — MCP forwarder + loader backlog 🔄

**Tests:** `tests/test_mcp_forwarder_coverage.py`

- `StubGitForwarder`, `SubprocessGitForwarder` error paths
- `mcp/git_server.py` **64% → ~71%** — HTTP MCP handlers remain until MCP E2E CI (PROPOSED)

### Tier 4 — Governance artifacts ✅

- This report
- `fail_under` / Codecov target → **85%**
- GitHub issue **post-flip reminder** (~2026-07-07): Tier 3 MCP CI + OIDC test matrix

---

## Residual gaps (honest matrix)

| Module | Coverage | Blocker to 95%+ | Track |
|--------|----------|-----------------|-------|
| `config/loader.py` | ~79% | YAML validation matrix @ 1.0.0 schema freeze | GA |
| `mcp/git_server.py` | ~71% | MCP E2E CI contract | Post-flip |
| `cli/logs.py` `--follow` | ~59% | Operator UX — low client impact | Tier 2b |
| `apex/predict.py` | ~75% | SAPAL experimental | PB-10 GA |
| `core/identity.py` | ~85% | ADR-002 OIDC implement | GA |

---

## Verify (maintainer)

```bash
source .venv/bin/activate
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/ -q --cov=ai_control_plane --cov-report=term-missing:skip-covered
# Expect: TOTAL ≥ 85%, smoke 8/8
pytest tests/test_smoke.py -m smoke -q
```

Codecov: https://app.codecov.io/gh/DataXMind/AI-Control-Plane

---

## Post-flip calendar (~2026-07-07)

- [ ] Re-run full coverage — confirm ≥85% on fresh `master` after PB-12 merge activity
- [ ] Open/follow GitHub issue: Tier 3 MCP E2E + OIDC test expansion (see linked issue in PR)
- [ ] Do **not** raise `fail_under` to 95% until GA schema freeze

**Last updated:** 2026-07-01 · pre–PB-12 public repo package
