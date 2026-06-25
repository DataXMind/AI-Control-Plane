# Lessons Learned — AI Control Plane (L5)

**Document ID:** ACP-GOV-LESSONS-001  
**Layer:** L5 — Governance & Memory  
**Format:** `[Pattern]` → `[When]` → `[Root cause]` → `[Rule added]` → `[Layer]`  
**Feedback loop:** Each pattern maps to `.cursorrules`, [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md), or `DEVELOPMENT_PROTOCOL.md`.  
**Reconciliation:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md) (HTML artifact P-01..P-07 merged 2026-06-25)

**Do not delete patterns** — historical audit trail (CURSOR_RISK F9).

---

## Pattern registry

### P-01 — Monolithic PR risk

| Field | Detail |
|-------|--------|
| **When** | PR #48 (MB bulk); PR #63 (MC-1..11 single PR) |
| **Root cause** | No LOC limit; Path B accepted as pattern |
| **Impact** | CI bisect hard; issue auto-close ambiguity |
| **Rule added** | HIGH ≤300 LOC; no mixing risk levels in one PR |
| **Layer** | L3 — [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §Risk levels |
| **Prevention** | `git diff master --stat \| tail -1` before open PR |
| **Status** | [ACTIVE — monitor] |

---

### P-02 — Scope creep in doc-only PRs

| Field | Detail |
|-------|--------|
| **When** | PR #46 — agent4 config in doc-only PR |
| **Root cause** | No file allowlist for LOW tasks |
| **Impact** | GAP-ABAC-2 ordering risk |
| **Rule added** | docs-only: `*.md`, `docs/**` only — `src/**` forbidden |
| **Layer** | L3 + L0 Surgical Changes |
| **Prevention** | `git diff --name-only master` → no `src/` |
| **Status** | [ACTIVE] |

---

### P-03 — GitHub auto-close failure (issue ranges)

| Field | Detail |
|-------|--------|
| **When** | PR #63 — `Closes #52..#62` closed only #52 |
| **Root cause** | GitHub does not parse ranges |
| **Rule added** | Individual `Closes #N` per issue |
| **Layer** | L5 — PR template |
| **Prevention** | `grep "Closes #.*\.\."` on PR body → 0 matches |
| **Status** | [RULE ENCODED] |

---

### P-04 — Silent ABAC / policy-loader assumption

| Field | Detail |
|-------|--------|
| **When** | GAP-ABAC-2 — `role_not_in` handling unclear |
| **Root cause** | No "state assumptions before coding" |
| **Rule added** | List condition keys handled vs skipped before loader/policy edits |
| **Layer** | L0 — Think Before Coding |
| **Prevention** | ABAC prompts include explicit key list |
| **Status** | [ACTIVE — highest priority] |

---

### P-05 — Step 7 timing (archive before merge)

| Field | Detail |
|-------|--------|
| **When** | Sprint 1 — report on branch before MB-S1 merged |
| **Root cause** | No "close commit = post-merge SHA" rule |
| **Rule added** | Sprint archive only after all PRs on master |
| **Layer** | L5 — CURSOR_RISK F7 |
| **Prevention** | Sprint report: `git log master -1 --format=%H` after final merge |
| **Status** | [RULE ENCODED] |

---

### P-06 — SAPAL scope reduction undocumented

| Field | Detail |
|-------|--------|
| **When** | Milestone C — ActAdapter skip on high risk; `learn.py` proposals=[] |
| **Root cause** | Conscious reduction not in PR body |
| **Rule added** | PR body: `Scope reduction: [item] → [milestone] because [reason]` |
| **Layer** | L2 + L5 |
| **Prevention** | PR template scope section not N/A when deferred |
| **Status** | [ENCODED IN PR TEMPLATE] |

---

### P-07 — Doc drift between sprints

| Field | Detail |
|-------|--------|
| **When** | Post Sprint 2 + post MC — ARCHITECTURE, README, backlog drifted |
| **Root cause** | No mandatory doc sync at sprint close |
| **Rule added** | Sprint-close: ARCHITECTURE + README reflect master |
| **Layer** | L5 sprint-close checklist |
| **Prevention** | Hygiene PR or same-sprint doc commit |
| **Status** | [ACTIVE] |

---

### P-08 — Stale `.cursorrules` L1 after milestone close

| Field | Detail |
|-------|--------|
| **When** | `.cursorrules` said "apex stub" while C/C+ CLOSED |
| **Root cause** | L1 not synced when milestones close |
| **Rule added** | Sprint-close: review `.cursorrules` + ARCHITECTURE status |
| **Layer** | L5 — [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) R4 |
| **Status** | [RULE ENCODED @ R1] |

---

### P-09 — Pilot without branch (L3 gap)

| Field | Detail |
|-------|--------|
| **When** | README edit on `master` tree without branch |
| **Root cause** | Demo task skipped branch isolation |
| **Rule added** | Even LOW → `{risk}/{desc}` branch + PR |
| **Layer** | L3 |
| **Status** | [RULE ENCODED] |

---

### P-10 — Governance UX static-only

| Field | Detail |
|-------|--------|
| **When** | Operators needed milestone/CS context without HTML artifacts |
| **Root cause** | Governance docs static only |
| **Rule added** | `GET /governance/status` + `agentctl gov status` + [`GOVERNANCE_UX_RUNTIME.md`](GOVERNANCE_UX_RUNTIME.md) |
| **Layer** | L1/L4 — `governance_catalog.py` |
| **Status** | [RULE ENCODED — PR #86] |

---

### P-11 — HTML artifact context drift

| Field | Detail |
|-------|--------|
| **When** | `karpathy_acp_artifacts_fixed.html` deploy packet (pytest 156, `docs/CURSOR_RISK` path) vs master post Studies 01–07 |
| **Root cause** | HTML not reconciled after Gov UX + practice evidence |
| **Rule added** | [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md); code + practice-evidence > HTML |
| **Layer** | L5 |
| **Status** | [ACTIVE — reconcile each major governance milestone] |

---

### P-12 — WSL2 multi-host ingress (operator)

| Field | Detail |
|-------|--------|
| **When** | Study 06 — Mac timeout until Admin portproxy + correct LAN IP |
| **Root cause** | WSL2 NAT; ping WSL IP from LAN; non-Admin portproxy |
| **Rule added** | [`study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md`](practice-evidence/study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md) |
| **Layer** | L3 ops (not code) |
| **Status** | [STABLE — encoded in practice evidence] |

---

## Maintenance

Add a pattern at each sprint close **before** declaring DONE.

Each pattern must:
1. Reference `.cursorrules` layer / section
2. Include prevention check (command or template)
3. Set `Status: [ACTIVE | RULE ENCODED | STABLE]`

**Quarterly review:** 0 recurrence for 2 sprints → [STABLE]; do not delete.

**Sprint-close checklist:**
1. GitHub issues — individual `Closes #N`
2. Doc drift fixed (`ARCHITECTURE.md`, sprint plans)
3. New pattern row here if failure occurred
4. `.cursorrules` / `CURSOR_RISK_POLICY.md` updated if rule added
5. Reconcile HTML artifacts if governance milestone shipped

---

**Last updated:** 2026-06-25 @ post Studies 01–07 + drift reconciliation
