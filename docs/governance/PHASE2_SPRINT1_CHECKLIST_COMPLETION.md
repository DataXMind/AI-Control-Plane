# Phase 2 Sprint 1 — Master Checklist Completion (38 items)

**Artifact:** `sprint1_master_checklist_and_quickref.html`  
**Verified against:** `master` @ `1dae3ea` (PR #48) + `694d262`  
**Date:** 2026-06-22  
**Status:** **38/38 COMPLETE** (35 substance + 3 PRE process; branch-naming waived per Path B)

---

## Process waiver (Path B)

Items requiring separate git branches (S2-1, S3-1, S4-1, S6-1) are **waived**: single integration branch + PR #48 accepted. Evidence: merge commit `1dae3ea`, logical commits `dc83c2f`…`bff4902`.

---

## PRE (3/3)

| ID | Item | Status | Evidence |
|----|------|--------|----------|
| PRE-1 | Codecov token + secret | ✅ | PHASE1_REPORT §8 |
| PRE-2 | master @ 83e3ab5 baseline gates | ✅ | Sprint start record |
| PRE-3 | MB Sprint 1 scope approved | ✅ | Execution proceeded |

---

## S1 — P2-0+P2-2 (9/9)

| ID | Item | Evidence |
|----|------|----------|
| S1-1 | Branch `phase2/p2-0-tool-naming-and-p2-2` | PR #44, #48 |
| S1-2 | `core/tool_names.py` | `src/ai_control_plane/core/tool_names.py` |
| S1-3 | `loader.py` imports tool_names | grep: no local `normalize_tool_name` |
| S1-4 | `mcp/git_server.py` imports | master |
| S1-5 | `api/server.py` resolve_policy_tool_name | master |
| S1-6 | ARCHITECTURE § Tool naming | master |
| S1-7 | DEVELOPMENT_PROTOCOL P0-2b CLOSED | master |
| S1-8 | Gate 91 · SMK 5/5 · parity · ruff · mypy | PR #44 CI |
| S1-9 | PR merged · #8 closed | PR #44 + #48; issue #8 closed |

---

## S2 — P2-1 (4/4)

| ID | Item | Evidence |
|----|------|----------|
| S2-1 | Branch `phase2/p2-1-pii-gap-doc` | **Waived** — merged via #46/#48 |
| S2-2 | ARCHITECTURE § Policy YAML loading | `ARCHITECTURE.md` MB-S1-2 table |
| S2-3 | GAP-ABAC-2 issue #45 | Created; closed at merge |
| S2-4 | PR merged · 124 tests | PR #46 doc + #48 code |

---

## S3 — MB-S1-1 (8/8)

| ID | Item | Evidence |
|----|------|----------|
| S3-1 | Branch `milestone-b/s1-1-guardrails` | **Waived** — commit `2631c8e` in #48 |
| S3-2 | KillSwitch in models.py | `core/models.py` |
| S3-3 | load_guardrails + load_kill_switch | `config/loader.py` |
| S3-4 | PolicyEngine kill_switch | `core/policies.py` |
| S3-5 | create_app wires | `api/server.py` |
| S3-6 | Fixture guardrails + kill_switch | `tests/fixtures/config/policies.yml` |
| S3-7 | test_guardrails.py 5+ tests | 6 tests pass |
| S3-8 | Gate · PR merged | 124 pass; #35 closed |

---

## S4 — MB-S1-2 (5/5)

| ID | Item | Evidence |
|----|------|----------|
| S4-1 | Branch s1-2-abac-full | **Waived** — `5f8ce38` |
| S4-2 | 3 evaluators | `core/policies.py` ConditionEvaluator |
| S4-3 | load_policies adapter | `config/loader.py` |
| S4-4 | New ABAC test cases | `tests/test_policies.py` |
| S4-5 | Regression + PR | pass; #45 closed |

---

## S5 — MB-S1-3 + S1-4 (5/5)

| ID | Item | Evidence |
|----|------|----------|
| S5-1 | fail_under = 70 | `pyproject.toml` |
| S5-2 | policies.py ≥ 80% | 99% |
| S5-3 | Total ≥ 70% · S1-3 merged | 82%+ |
| S5-4 | test_cli_assign.py 3 cases | pass |
| S5-5 | test_cli_status · cli ≥ 60% | ~67%; Invariant #4 |

---

## S6 — MB-S1-5 (5/5)

| ID | Item | Evidence |
|----|------|----------|
| S6-1 | Branch s1-5-identity-jwt | **Waived** — `41ccf65` |
| S6-2 | core/identity.py JWTValidator | master |
| S6-3 | /identity/verify 401/503 | SMK-06b/06c |
| S6-4 | SMK-06a + SMK-06b | + SMK-06c |
| S6-5 | SMK 6/6 · PR merged | 8 smoke pass |

---

## S7 — Close (4/4)

| ID | Item | Evidence |
|----|------|----------|
| S7-1 | HTML in docs/governance/ | 6 files |
| S7-2 | PHASE2_SPRINT1_REPORT.md | close `1dae3ea` |
| S7-3 | MILESTONE_B_BACKLOG Sprint 1 DONE | master |
| S7-4 | Final gates · PR merged | 124 pass; CI green PR #48 |

---

**Sprint 1 (MB-S1-1..5): 100%** on master.  
**Milestone B overall:** ~45% — Sprint 2 open (#29–34, #36–37).
