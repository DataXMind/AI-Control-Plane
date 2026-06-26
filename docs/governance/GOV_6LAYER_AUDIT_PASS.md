# 6-Layer Governance — Audit Pass Record

**Document ID:** ACP-GOV-6LAYER-PASS-001  
**Date:** 2026-06-22  
**Target:** `master` via PR consolidation (`low/gov-6layer-audit-complete`)

---

## Checklist (items 1–6)

| # | Item | Status | Evidence |
|---|------|--------|----------|
| 1 | 6-layer `.cursorrules` on master | ✅ PR branch | `## L0` … `## L5` in `.cursorrules` |
| 2 | Post-merge verify | ✅ | This doc + puzzle map links |
| 3 | Pilot session (L0 pre-flight) | ✅ | Chat pilot 2026-06-22; branch `low/gov-ux-runtime` for L3 fix |
| 4 | Audit reconcile artifact | ✅ | `audit_reconcile_final.html` + `ACP_AUDIT_RECONCILE_FINAL_STATUS.md` |
| 5 | Phase R2 | ✅ | `docs/DATA_CLASSIFICATION.md`, ARCHITECTURE §Module ownership, DEVELOPMENT_PROTOCOL L2 |
| 6 | Phase R3 + harden | ✅ | `CONTRACT_TESTS.md`, `test_api_contract_snapshot.py`, PR template |
| 7 | Governance UX runtime | ✅ | `GET /governance/status`, `agentctl gov status`, `GOVERNANCE_UX_RUNTIME.md` |
| 8 | L5 ML5 memory pack | ✅ | `AGENTS.md`, `.cursor/rules/`, `SESSION_ANCHOR_TEMPLATE`, GP-01, CI `governance-memory` |

---

## L3 / L5 audit @ `low/gov-ux-runtime`

| Layer | Check | Result |
|-------|-------|--------|
| L3 | Branch `low/gov-ux-runtime` from master | ✅ |
| L3 | PR template risk + verify checklist | ✅ |
| L5 | Patterns 6–7 in LESSONS_LEARNED | ✅ |
| L5 | GOV_6LAYER item #7 + pilot #3 closed | ✅ |

## Layer live map @ merge

| Layer | Authority file |
|-------|----------------|
| L0 | `.cursorrules` §L0 |
| L1 | `ARCHITECTURE.md`, `docs/DATA_CLASSIFICATION.md` |
| L2 | `docs/governance/CURSOR_RISK_POLICY.md` |
| L3 | `.cursorrules` §L3, `CONTRIBUTING.md` |
| L4 | CI + `docs/CONTRACT_TESTS.md` + `GET /governance/status` |
| L5 | `LESSONS_LEARNED.md`, `AGENTS.md`, `.cursor/rules/`, GP-01 |

---

## Not mechanically enforced (honor system + review)

- LOC limits per risk tier
- File allowlists per task type
- L0 assumption block before code

Track violations in [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md).

**Supersedes:** Informal audit FAIL @ flat `.cursorrules` on `c5d52e5`.

---

## Post-studies + G1 wave addendum @ `master` `638250c` (2026-06-26)

**Merged PRs:** [#91](https://github.com/DataXMind/AI-Control-Plane/pull/91) ML5 · [#93](https://github.com/DataXMind/AI-Control-Plane/pull/93) CLI gov tests · [#94](https://github.com/DataXMind/AI-Control-Plane/pull/94) CURSOR_RISK full L2 · [#95](https://github.com/DataXMind/AI-Control-Plane/pull/95) CLAUDE.md · [#96](https://github.com/DataXMind/AI-Control-Plane/pull/96) LESSONS enrich

| Layer | Evidence @ `638250c` | L4 verify |
|-------|-------------------|-----------|
| **L0** | `CLAUDE.md` + `.cursorrules` Karpathy 4 | Session anchor + AGENTS.md |
| **L2** | `CURSOR_RISK_POLICY.md` F1–F11, per-level verify | PR template enforced |
| **L4** | **176** pytest · **SMK 8/8** · `test_cli_gov.py` (gov.py 100%) | Operator gate run 2026-06-26 — see below |
| **L5** | P-01..P-12 · GP-01 · ML5 CI `governance-memory` | Studies 01–07 [`practice-evidence/`](practice-evidence/) |

**Operator verify gate** (`DEVELOPMENT_PROTOCOL.md` §5.5 — mandatory before declaring merge-ready):

```bash
bash scripts/verify_governance_memory.sh
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -q
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -q -m shipped_config
```

**Protocol note:** Docs-only PRs still pass **CI** smoke/full suite on GitHub; **local** SMK run was skipped on some agent sessions (drift). Remediation: run full gate above on `master` after every merge batch — not only `git diff` checks.

**G1-4:** This addendum closes GOV_6LAYER item linking practice-evidence L4 proof.

## Post-PR #99 governance UX verify @ `8b30ad4` (2026-06-26)

**Merged:** [#99](https://github.com/DataXMind/AI-Control-Plane/pull/99) — `known_gaps[]` + `practice_evidence` on `GET /governance/status` (catalog v1.2).

| Host | Procedure | Result |
|------|-----------|--------|
| MSI WSL | `git pull` + `docker compose up -d --build` | `1.2 7 PASS` |
| ubuntu-vps | `git pull` + `systemctl restart acp-staging` | `1.2 7 PASS` |

**Evidence:** [`practice-evidence/governance-status-v12-verify/`](practice-evidence/governance-status-v12-verify/)

**Lesson:** Stale Docker image without rebuild → missing JSON fields (`KeyError: known_gaps`); aligns with gap **G-02** / Study 05e narrative.

**Last updated:** 2026-06-26
