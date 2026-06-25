# Lessons Learned — Governance Memory (L5)

**Document ID:** ACP-GOV-LESSONS-001  
**Layer:** L5 — Governance & Memory  
**Format:** `[Pattern]` → `[Occurrence]` → `[Rule added]` → `[Layer / file]`  
**Feedback loop:** Each new pattern must map to `.cursorrules`, `CURSOR_RISK_POLICY.md`, or `DEVELOPMENT_PROTOCOL.md`.

**Source extraction:** [`karpathy_acp_rearchitecture_analysis.html`](karpathy_acp_rearchitecture_analysis.html) pane ⑤ + sprint audits.

---

## Pattern 1 — Monolithic PR

| Field | Detail |
|-------|--------|
| **Occurrence** | PR #48 (MB-S1-1..5 + agent4); PR #63 (MC-1..11 single PR) |
| **Cause** | No LOC limit; Path B waiver without split plan |
| **Rule added** | HIGH ≤300 LOC; no mixing risk levels; split by issue |
| **Prevent** | L3 — [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §Risk levels |

---

## Pattern 2 — Scope creep in doc-only PRs

| Field | Detail |
|-------|--------|
| **Occurrence** | agent4 config merged in PR #46 (doc-only scope) |
| **Cause** | No file allowlist for LOW tasks |
| **Rule added** | docs-only PR: `*.md`, `docs/**` only — `src/**` forbidden |
| **Prevent** | L3 — [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §File allowlists |

---

## Pattern 3 — GitHub auto-close failure

| Field | Detail |
|-------|--------|
| **Occurrence** | PR #63 `Closes #52..#62` — only #52 closed |
| **Cause** | GitHub does not parse issue ranges |
| **Rule added** | Individual `Closes #53`, `Closes #54`, … per issue |
| **Prevent** | L5 process — PR template + hygiene script |

---

## Pattern 4 — Silent policy-loader assumption

| Field | Detail |
|-------|--------|
| **Occurrence** | GAP-ABAC-2 — `role_not_in` handling unclear during loader work |
| **Cause** | No "state assumptions before coding" step |
| **Rule added** | Before `config/loader.py` / `core/policies.py` changes: list condition keys handled vs skipped |
| **Prevent** | L0 — Think Before Coding (see rearchitecture plan Phase R1) |

---

## Pattern 5 — Stale `.cursorrules` after milestone close

| Field | Detail |
|-------|--------|
| **Occurrence** | `.cursorrules` still says "apex/ stub only until Milestone C" while C/C+ CLOSED |
| **Cause** | L1 context not synced when milestones close |
| **Rule added** | Sprint-close: review `.cursorrules` + `ARCHITECTURE.md` execution status |
| **Prevent** | L5 sprint-close checklist — [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) §R4 |

---

## Pattern 6 — Pilot without branch (L3 gap)

| Field | Detail |
|-------|--------|
| **Occurrence** | README pilot link edited on `master` working tree without branch |
| **Cause** | Demo task skipped L3 branch isolation |
| **Rule added** | Even LOW tasks use `{risk}/{desc}` branch + PR |
| **Prevent** | L3 — fixed in `low/gov-ux-runtime` with full 6-layer delivery |

---

## Pattern 7 — Governance UX at runtime

| Field | Detail |
|-------|--------|
| **Occurrence** | Operators needed milestone/risk context without reading HTML artifacts |
| **Cause** | Governance docs static only |
| **Rule added** | `GET /governance/status` + `agentctl gov status` + `GOVERNANCE_UX_RUNTIME.md` |
| **Prevent** | L1/L4 — catalog in `core/governance_catalog.py`; tests in `test_governance_status.py` |

---

## Sprint-close checklist (add to DEVELOPMENT_PROTOCOL Evolve)

1. GitHub issues closed with individual `Closes #N`.
2. Doc drift fixed (`ARCHITECTURE.md`, sprint plans).
3. New row added here if a new failure pattern occurred.
4. `.cursorrules` / `CURSOR_RISK_POLICY.md` updated if rule added.
5. Drift tally per layer (optional) in sprint report.

---

**Last updated:** 2026-06-22 @ `c5d52e5`
