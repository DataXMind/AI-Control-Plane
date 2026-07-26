# Lessons Learned — AI Control Plane (L5)

**Document ID:** ACP-GOV-LESSONS-001  
**Layer:** L5 — Governance & Memory  
**Format:** `[Pattern]` → `[When]` → `[Root cause]` → `[Rule added]` → `[Layer]`  
**Update when:** Sprint close, hygiene PR, or significant drift event  
**L5 → L0 loop:** Every pattern must map to a layer in [`.cursorrules`](../../.cursorrules) and/or [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md)  
**Reconciliation:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md)

**Do not delete patterns** — historical audit trail ([`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) **F9**).

---

## Pattern registry

### P-01 — Monolithic PR risk

| Field | Detail |
|-------|--------|
| **When** | Sprint 1 — PR #48 (MB-S1-1..5 + agent4 scope creep); Milestone C — PR #63 (MC-1..11 single PR) |
| **Root cause** | No LOC limit or task-scope enforcement; Path B accepted as one-off but became pattern |
| **Impact** | CI hard to bisect; issue auto-close ambiguity; reviewer audit complexity |
| **Rule added** | L3 — max **300 LOC** per HIGH PR; no combining risk levels (F4). See [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §3 PR size enforcement |
| **Layer** | L3 (Execution Guardrails) |
| **Prevention** | Before open PR: `git diff master --stat \| tail -1` → verify LOC |
| **Status** | [ACTIVE — monitor next 2 sprints] |

---

### P-02 — Scope creep in doc-only PRs

| Field | Detail |
|-------|--------|
| **When** | PR #46 — P2-1 doc-only PR merged agent4 config alongside documentation |
| **Root cause** | No file allowlist per task type; Cursor added “helpful” config during doc work |
| **Impact** | agent4 PII restrictions on master before ABAC `role_not_in` code → GAP-ABAC-2 ordering risk |
| **Rule added** | L3 allowlist: docs-only → `*.md`, `docs/**` only; **forbidden** `src/**`, `tests/**` (F11). L0 Surgical Changes. See [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §1 LOW + §6 |
| **Layer** | L3 + L0 |
| **Prevention** | After stage: `git diff --name-only master` → no `src/` or `tests/` |
| **Status** | [ACTIVE] |

---

### P-03 — GitHub auto-close failure (issue ranges)

| Field | Detail |
|-------|--------|
| **When** | PR #63 — body had `Closes #52..#62`; only #52 closed |
| **Root cause** | GitHub does not parse issue ranges; issues created after PR open also do not auto-close |
| **Impact** | ~10 issues remained OPEN post-merge → hygiene PR → governance lag |
| **Rule added** | L5 process — list each issue: `Closes #53`, `Closes #54`, … never ranges (**F6**). See PR body template §4 |
| **Layer** | L5 (Governance & Memory) |
| **Prevention** | `grep "Closes #.*\.\."` on PR body → 0 matches |
| **Status** | [RULE ENCODED — verify at next PR] |

---

### P-04 — Silent ABAC assumption (`role_not_in` skip)

| Field | Detail |
|-------|--------|
| **When** | `load_policies()` initially skipped `role_not_in`, `approval_status`, `read_only` silently |
| **Root cause** | No “state assumptions before coding”; partial ABAC without flagging skips |
| **Impact** | GAP-ABAC-2 — operators assumed full PII enforcement; runtime silently over-denied |
| **Rule added** | L0 — before policy/loader changes: list condition keys **handled vs skipped**; if skip → document GAP-* in same PR (**F8**). See [`CLAUDE.md`](../../CLAUDE.md) §Think before coding |
| **Layer** | L0 (Behavioral Constitution) |
| **Prevention** | ABAC task prompt: “State all keys in `policies.yml` and which you will implement.” |
| **Status** | [ACTIVE — highest priority prevention] |

---

### P-05 — Step 7 timing (archive before merge)

| Field | Detail |
|-------|--------|
| **When** | Sprint 1 — `PHASE2_SPRINT1_REPORT.md` on branch before MB-S1 PRs merged to master |
| **Root cause** | No explicit rule: close commit = post-merge SHA only |
| **Impact** | Close commit in report ambiguous; governance record inaccurate |
| **Rule added** | L5 — Step 7 archive **only after** all sprint PRs on master; close commit = merge SHA, never branch SHA (**F7**) |
| **Layer** | L5 |
| **Prevention** | Sprint report: `git log master -1 --format=%H` **after** final merge |
| **Status** | [RULE ENCODED] |

---

### P-06 — SAPAL scope reduction undocumented

| Field | Detail |
|-------|--------|
| **When** | Milestone C — ActAdapter skipped PolicyEngine on `risk_level=high`; `learn.py` `proposals=[]` always |
| **Root cause** | Conscious, correct reduction not documented in PR body or issue |
| **Impact** | Audit had to infer intent; ARCHITECTURE Milestone C description drifted |
| **Rule added** | L2 — PR body: `Scope reduction: [item] → [milestone] because [reason]` (or N/A). See [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §4 |
| **Layer** | L2 (Risk Policy) + L5 (Decision log) |
| **Prevention** | PR template scope section required when deferring |
| **Status** | [ENCODED IN PR TEMPLATE] |

---

### P-07 — Doc drift between sprints

| Field | Detail |
|-------|--------|
| **When** | Post Sprint 2 + post MC — `ARCHITECTURE.md`, README, `PHASE1_REPORT_V2`, `MILESTONE_B_BACKLOG` drifted |
| **Root cause** | No mandatory doc sync at sprint close; docs updated on branch but not always synced to master truth |
| **Impact** | Dedicated hygiene PRs; ~12 drift items across two audit cycles |
| **Rule added** | L5 sprint-close — doc sync mandatory before sprint DONE; `ARCHITECTURE.md` + README reflect master. See `.cursorrules` §L5 sprint-close checklist; [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) §5.6 Evolve |
| **Layer** | L5 |
| **Prevention** | Sprint close: `grep -E 'IN PROGRESS|TODO|stale' ARCHITECTURE.md` → 0 unintended hits |
| **Status** | [ACTIVE — enforce at next sprint close] |

---

### P-08 — Stale `.cursorrules` L1 after milestone close

| Field | Detail |
|-------|--------|
| **When** | `.cursorrules` said “apex stub” while C/C+ CLOSED |
| **Root cause** | L1 not synced when milestones close |
| **Rule added** | Sprint-close: review `.cursorrules` + `ARCHITECTURE.md` milestone status |
| **Layer** | L5 — [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) R4 |
| **Prevention** | Sprint-close checklist item 4 |
| **Status** | [RULE ENCODED @ R1] |

---

### P-09 — Pilot without branch (L3 gap)

| Field | Detail |
|-------|--------|
| **When** | README edit on `master` tree without branch |
| **Root cause** | Demo task skipped branch isolation |
| **Rule added** | Even LOW → `{risk}/{desc}` branch + PR |
| **Layer** | L3 |
| **Prevention** | `git branch --show-current` ≠ `master` before commit |
| **Status** | [RULE ENCODED] |

---

### P-10 — Governance UX static-only

| Field | Detail |
|-------|--------|
| **When** | Operators needed milestone/CS context without HTML artifacts |
| **Root cause** | Governance docs static only |
| **Rule added** | `GET /governance/status` + `agentctl gov status` + [`GOVERNANCE_UX_RUNTIME.md`](GOVERNANCE_UX_RUNTIME.md) |
| **Layer** | L1/L4 — `governance_catalog.py` |
| **Prevention** | `agentctl gov status` shows CS-01..06 |
| **Status** | [RULE ENCODED — PR #86] |

---

### P-11 — HTML artifact context drift

| Field | Detail |
|-------|--------|
| **When** | `karpathy_acp_artifacts_fixed.html` (pytest 156, wrong `docs/CURSOR_RISK` path) vs master post Studies 01–07 |
| **Root cause** | HTML not reconciled after Gov UX + practice evidence |
| **Rule added** | [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md); code + practice-evidence > HTML |
| **Layer** | L5 |
| **Prevention** | Reconcile at each major governance milestone (G0, ML5, PB-12) |
| **Status** | [ACTIVE — reconcile each major governance milestone] |

---

### P-12 — WSL2 multi-host ingress (operator)

| Field | Detail |
|-------|--------|
| **When** | Study 06 — Mac timeout until Admin portproxy + correct Windows LAN IP |
| **Root cause** | WSL2 NAT; ping WSL IP from LAN; non-Admin portproxy |
| **Rule added** | [`practice-evidence/study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md`](practice-evidence/study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md) |
| **Layer** | L3 ops (not code) |
| **Prevention** | Study 06 topology before multi-host drills |
| **Status** | [STABLE — encoded in practice evidence] |

---

### P-13 — Kill switch HTTP contract (counter-intuitive behavior)

| Field | Detail |
|-------|--------|
| **When** | Study 05 drill 5g (G-01 remediation, G2-1) — 2026-06-26 |
| **Root cause** | Kill switch active → HTTP **200** + `allowed: false` (NOT 503). Operators expecting HTTP error codes miss the deny signal. `GET /health` is exempt — returns 200 even when kill switch active. |
| **Impact (potential)** | Operator monitoring for HTTP 5xx would not detect kill switch state. TS `PolicyClient` correctly handles 200+`allowed=false`, but human ops dashboards may not surface this without explicit `kill_switch_active` reason check. |
| **Evidence** | [`practice-evidence/study-05-advanced-surprises/artifacts/terminal-5g-g2-killswitch.md`](practice-evidence/study-05-advanced-surprises/artifacts/terminal-5g-g2-killswitch.md); [`kill-switch-active.json`](practice-evidence/study-05-advanced-surprises/artifacts/kill-switch-active.json); [`health-during-kill-switch.json`](practice-evidence/study-05-advanced-surprises/artifacts/health-during-kill-switch.json) |
| **Rule added** | L2 risk policy — kill switch activation is an operator action requiring explicit monitoring of `allowed=false` + `reason` field, not HTTP status code. See [`CURSOR_RISK_POLICY.md`](CURSOR_RISK_POLICY.md) §10; Study 05 [`RUNBOOK.md`](practice-evidence/study-05-advanced-surprises/RUNBOOK.md) §5g |
| **Layer** | L2 (Risk Policy) + L4 (Evaluation — monitoring contract) |
| **Prevention** | When kill switch may be active: `curl -sf -X POST "$ACP_API_URL/policy/evaluate" … \| python3 -c "import sys,json; d=json.load(sys.stdin); assert not d['allowed'] and d['reason'].startswith('kill_switch_active')"` — do **not** alert on HTTP 5xx alone |
| **Status** | [RULE ENCODED — G2-1 @ 2026-06-26] |

> **Note:** Claude architect prompt (post–Study 05g-r) proposed **P-08** for this pattern. **P-08** was already assigned at G0 reconciliation (stale `.cursorrules` L1). Per F9 do-not-delete, this lesson is **P-13**.

---

### P-14 — Governance Catalog Static Drift

| Field | Detail |
|-------|--------|
| **When** | governance_catalog.py `gates_remaining` audited — static hardcoded list, not computed from practice evidence |
| **Root cause** | Manual maintainer sync required at each flip; no evidence predicates |
| **Impact** | Practice PASS and catalog state diverge silently; operator assumes gates closed when catalog still lists them |
| **Rule added** | [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md) §deeper-perspectives; [`GOVERNANCE_CHANGELOG.md`](GOVERNANCE_CHANGELOG.md) |
| **Layer** | L5 (Governance & Memory) |
| **Prevention** | 1. Always update GOVERNANCE_CHANGELOG.md when bumping governance version. 2. Every gate PASS must reference a specific RESULTS.md path, not just verbal claim. 3. Use `GET /governance/status` → `gate_details` + `gates_blocking_pb12` (P-14 predicates @ v1.5.0). |
| **Status** | [ACTIVE] |

---

### P-15 — Soak Load Realism Gap

| Field | Detail |
|-------|--------|
| **When** | PB-9 soak — ~1 req/hour (heartbeat interval), not realistic concurrent agent load |
| **Root cause** | p99 SLO targets stated as design targets, not verified at production load levels |
| **Impact** | System appears healthy under soak but degrades under real agent fleet concurrency (10+ simultaneous agents) |
| **Rule added** | [`LOAD_CHARACTERISTICS.md`](LOAD_CHARACTERISTICS.md); [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) §SLO |
| **Layer** | L4 (Evaluation) |
| **Prevention** | 1. Always specify RPS context when stating p99 SLO (e.g., "p99 < 500ms at 10 RPS", not absolute). 2. Before any production recommendation, run load test with expected concurrency (locust or k6). 3. Document soak scope explicitly: "stability soak" vs "load test" vs "chaos test". |
| **Status** | [ACTIVE] |

---

### P-16 — Threat Model Absence in Security-Critical Infrastructure

| Field | Detail |
|-------|--------|
| **When** | ACP reached Public Beta with no formal threat model; STRIDE analysis absent despite ACP being a security enforcement control plane with fail-closed behavior |
| **Root cause** | Attack surfaces (DoS on policy engine, Redis cache poisoning, token spoofing, network partition) not enumerated before public surface exposure |
| **Impact** | Attack surfaces unknown to operators deploying in production |
| **Rule added** | [`THREAT_MODEL.md`](THREAT_MODEL.md); [`SECURITY.md`](../../SECURITY.md); [`GOVERNANCE_CHANGELOG.md`](GOVERNANCE_CHANGELOG.md) §MINOR definition |
| **Layer** | L2 (Risk Policy) |
| **Prevention** | 1. Threat model (STRIDE-lite minimum) is required artifact before any public surface exposure. 2. "Fail-closed" is not a complete security posture — availability attacks (DoS) still apply. 3. Update THREAT_MODEL.md at every governance MINOR bump. |
| **Status** | [ACTIVE] |

---

### P-17 — MCP Context Tax / Connector Minimalism

| Field | Detail |
|-------|--------|
| **When** | 48H ECC integration — industry shift to default **zero** MCP connectors; each connector loads tool schemas into every session context window |
| **Root cause** | Treating MCP inventory as free — connectors multiply tokens, attack surface, and session startup latency without policy benefit |
| **Impact** | Agents exhaust context on tool metadata; operators confuse harness transport with ACP policy truth |
| **Rule added** | [`MCP_INTEGRATION_CONTRACT.md`](MCP_INTEGRATION_CONTRACT.md) §Decision matrix; [`THREAT_MODEL.md`](THREAT_MODEL.md) §6; [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md) A8 |
| **Layer** | L2 (Risk Policy) + L1 (context budget) |
| **Prevention** | 1. Target **0–1** default MCP connectors per operator harness. 2. Prefer skill/CLI/`docs/prompts/` over new connector. 3. Policy allow/deny stays `POST /policy/evaluate` — MCP is transport only. 4. Full inventory audit deferred **Study 09** post-flip. |
| **Status** | [ACTIVE] |

---

### P-18 — External agent-protocol prompts must map onto existing SSOT, not spawn new ones

| Field | Detail |
|-------|--------|
| **When** | 2026-07-08 — human supplied an external, generic "Autonomous Project Execution Agent" prompt (context anchoring, decision log, lessons log, human-gate tiers, smoke matrix) to be integrated into `CLAUDE.md` |
| **Root cause** | Generic multi-session agent protocols are written file-name-agnostic (`PROJECT_ANCHOR.md`, `DECISION_LOG.md`, `LESSONS_LOG.md`, `CURRENT_STATUS.md`, `DAILY_LOG.md`) — applied literally, they would create a second SSOT next to `docs/prompts/ANCHOR_CURRENT.md`, `STATE/DECISIONS.md`, `docs/governance/LESSONS_LEARNED.md`, and `STATE/PROGRESS.md` |
| **Impact** | Same failure shape as P-07/P-08 (doc drift, stale layer) but self-inflicted by the agent this time, from following an external prompt too literally instead of reconciling it with what already exists |
| **Rule added** | `CLAUDE.md` §5.1 — explicit generic-role → repo-file mapping table; new sections of any adopted external protocol must be mapped onto existing files before being written into `CLAUDE.md`, never given parallel files |
| **Layer** | L0 (Behavioral Constitution) + L5 (Governance & Memory) |
| **Prevention** | Before adopting any external agent protocol: `grep`/`ls` this repo's `docs/prompts/`, `docs/governance/`, and `STATE/` for an existing file serving the same role; only create new files for roles with no existing analogue (verified none needed here) |
| **Status** | [ACTIVE] |

**`.cursorrules` review (L5 sprint-close checklist item 4, performed for P-18):** checked `.cursorrules` L0 (lines 8-33) and L5 (lines 144-157) — L0 is, by existing design, a condensed mirror of only the 4 core Karpathy principles from `CLAUDE.md`; the "ACP-specific rules" and "Governance memory" blocks of `CLAUDE.md` (invariants, risk classification, forbidden list, memory resources) were **already** un-mirrored before this pattern existed. **Conclusion: no `.cursorrules` rule addition needed** — P-18's rule lives in `CLAUDE.md` §5.1 consistent with that existing split, not a gap.

---

### P-19 — STATE claims about other repos go stale fast in a concurrent multi-session environment

| Field | Detail |
|-------|--------|
| **When** | 2026-07-08 — a Self-Audit re-check (re-running `git fetch` on the Hybrid-AI-Gateway remote) found that this repo's own `STATE/DECISIONS.md`/`STATE/PROGRESS.md` claim "GATE-O1 blocked — SACP hasn't pushed the contract" was already false: SACP had pushed (`origin/main` had moved from `c6ec8e4` to `711c6b4`), and GATE-O1 had actually resolved to PASS-with-conditions, independently confirmed in both the SACP and AEOS repos' own STATE files |
| **Root cause** | A cross-repo claim was written once (Batch ACP-02) and then treated as durable fact by the next review pass (Opus Review Gate) without a re-fetch, even though the claim's whole premise was "another session's future action" — the one thing guaranteed to change without this repo's own commits reflecting it |
| **Impact** | Low this time (caught before being acted on) but the failure mode is real: a future session could skip re-verifying, waste effort re-deriving already-resolved state, or worse, escalate a already-closed blocker to a human as if still open |
| **Rule added** | `CLAUDE.md` §5.2 (re-anchor "whenever an assumption contradicts `STATE/DECISIONS.md`" — extend in practice to: **any STATE claim describing another repo's pending action is provisional and must be re-verified via a live check (`git fetch`/read remote), not re-cited from memory, before being relied on** |
| **Layer** | L0 (re-anchoring) + L5 (cross-repo decision log) |
| **Prevention** | Before treating a cross-repo "blocked on X" claim as current: re-run the actual check that would resolve it (fetch, read remote file) — do not answer from the last time it was checked |
| **Status** | [ACTIVE] |

---

### P-20 — Partial read of a long reference doc, silently treated as full review

| Field | Detail |
|-------|--------|
| **When** | 2026-07-08 — human directly asked "have you reviewed `ACP_Guardrails_report.md`?" and it surfaced that an earlier turn had called `Read` on that file with `offset=100`, skipping lines 1-99 (header, changelog v2→v3, confidence-label legend, table of contents, and all of §1 "Hiện trạng hệ thống": identity table, hosting/deploy, milestones, per-module % complete) — and no later turn ever went back to close that gap until asked |
| **Root cause** | Jumping to a mid-file offset out of habit, with no stated reason, then citing/using content from later sections as if the whole document had been read — the gap was invisible because nothing downstream happened to contradict it |
| **Impact** | Low this time (lines 1-99 turned out consistent with everything already in use — `STATE/DECISIONS.md` #1, `STATE/PROGRESS.md` gap table), but the consistency was luck, not verification — a partial read of a source-of-truth document was silently presented as complete understanding of it |
| **Rule added** | When reading a file cited as an authoritative source (an `#Anchor:` reference in the Kickoff Brief, an audit report, etc.) for the first time, read from the start (or state explicitly which range was read and why, e.g. "read only §5, task doesn't need the rest") — never silently partial-read and let it pass as "reviewed" |
| **Layer** | L0 (Think before coding — "state assumptions", extended to "state what was actually read") |
| **Prevention** | Before claiming to have "reviewed" or "read" a file: `grep -c ''` its line count vs. what was actually passed to `Read` (offset/limit) — a claim of review with a truncated range and no disclosure is the same failure as an unverified assumption |
| **Status** | [ACTIVE] |

---

### P-21 — Conflating "no dedicated registration" with "not operational / bypasses policy"

| Field | Detail |
|-------|--------|
| **When** | 2026-07-09 — deep-audit report labeled the AEOS integration row as "CHƯA ĐĂNG KÝ / hoàn toàn không qua ACP check nào", which the operator corrected: AEOS **is** operational and **does** call ACP by design |
| **Root cause** | Two distinct facts were collapsed into one wrong conclusion: (1) `aeos` has no dedicated project/agent in ACP config — it borrows `agent2/backend/rust-gateway` (TRUE, O-02); (2) `ACP_ENABLED=false` in AEOS **dev** while Q-15 is unfixed (TRUE but TEMPORARY). From these two, the report wrongly generalized to "AEOS isn't integrated / bypasses ACP entirely" — contradicting `OSAgent_audit_report.md` §2.2/§4.2 which verifies the session-create path calls `POST /policy/evaluate` and smoke-passed HTTP 201 on 2026-07-05 |
| **Impact** | Mischaracterized a partner system's real maturity in a report to the operator — the kind of over-claim (in the negative direction) that erodes trust in the audit itself |
| **Rule added** | Separate "registered as its own identity" from "operational / policy-enforced". A borrowed identity or a temporary dev-mode toggle is not the same as "not integrated". State each fact at its own scope; never generalize a config gap into a capability claim without reading the partner repo's own audit |
| **Layer** | L0 (state assumptions at correct scope) + L5 (cross-repo claims) |
| **Prevention** | Before asserting a partner system's integration status: read that repo's own audit/STATE (here `OSAgent_audit_report.md`), and distinguish config-registration ≠ runtime-behavior ≠ temporary-toggle |
| **Status** | [ACTIVE] |

---

## Maintenance

Add a pattern at each **sprint close** (before declaring sprint DONE).  
New failures may be added **immediately** — do not wait for sprint end.

Each pattern must:

1. Reference `.cursorrules` layer / section it maps to  
2. Include a **prevention check** (command or template)  
3. Set `Status: [ACTIVE | RULE ENCODED | STABLE]`

**Quarterly review** (first calendar: **2026-09**, G1-3):

- 0 recurrence for 2 sprints → mark **[STABLE]** (do not delete)  
- Rule prevented recurrence 3+ times → consider promote to `.cursorrules` L0  
- Do not delete patterns — F9 audit trail

**Sprint-close checklist** (sync with `.cursorrules` §L5):

1. GitHub issues — individual `Closes #N` (P-03)  
2. Doc drift fixed — `ARCHITECTURE.md`, README, sprint plans (P-07)  
3. New pattern row here if a failure occurred  
4. `.cursorrules` / `CURSOR_RISK_POLICY.md` updated if rule added  
5. Reconcile HTML artifacts if governance milestone shipped (P-11)  
6. `LESSONS_LEARNED.md` updated — [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md) §5.6 Evolve

---

**Last updated:** 2026-06-30 @ P-17 MCP context tax (48H Phase 5); P-08..P-16 unchanged
