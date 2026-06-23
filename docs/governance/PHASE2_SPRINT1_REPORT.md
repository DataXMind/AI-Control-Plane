# Phase 2 Sprint 1 Report

**Date:** 2026-06-22  
**Baseline:** `master` @ `83e3ab5` (Phase 1 v2)  
**Sprint 1 close commit:** pending merge to `master` (PR Sprint 1 MB-S1-1..5)

---

## Completed

| Task | Branch | Tests added | Coverage delta |
|------|--------|-------------|----------------|
| P2-0+P2-2 `core/tool_names.py` | `phase2/p2-0-tool-naming-and-p2-2` | 0 (docs) | 0 |
| P2-1 PII gap doc | `phase2/p2-0-tool-naming-and-p2-2` | 0 (docs) | 0 |
| MB-S1-1 Guardrails+kill_switch | `phase2/p2-0-tool-naming-and-p2-2` | 6 | +2% (guardrails path) |
| MB-S1-2 ABAC full | `phase2/p2-0-tool-naming-and-p2-2` | 4+ | +3% (condition adapter) |
| MB-S1-3 Coverage floor | `phase2/p2-0-tool-naming-and-p2-2` | 17 | policies 99% |
| MB-S1-4 CLI tests | `phase2/p2-0-tool-naming-and-p2-2` | 4 | cli assign/status ~67% |
| MB-S1-5 Identity JWT + SMK-06 | `phase2/p2-0-tool-naming-and-p2-2` | 3 | identity 89% |

**Commit range (Sprint 1):** `dc83c2f` … `41ccf65`

---

## Gates

| Gate | Result |
|------|--------|
| pytest | **124** pass, 0 fail |
| SMK-01..06 | **8/8** pass (06 includes 06b invalid JWT, 06c unknown agent) |
| shipped_config parity | **5/5** pass (incl. Restrict-PII + role_not_in) |
| Codecov / local cov | **82%** (≥70 required, `fail_under=70` in `pyproject.toml`) |
| ruff | clean |
| mypy `--strict` | clean (36 source files) |

---

## Open (Sprint 2)

- Redis QuotaStore (#29–31)
- `mcp/server_factory.py`
- `cli/approve` + `cli/quota` live
- cyanheads MCP E2E

---

## Invariants

All 8 invariants intact — verified via mypy strict + full test suite.

---

## Governance archive

Phase 1 / Phase 2 Claude HTML artifacts remain under [`docs/governance/*.html`](.) (archived at Milestone A close; no root-level HTML at Sprint 1 close).

**Related:** [`MILESTONE_B_BACKLOG.md`](MILESTONE_B_BACKLOG.md) · [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) v1.3
