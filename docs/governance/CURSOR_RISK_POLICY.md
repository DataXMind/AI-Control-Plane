# Cursor Risk Policy — AI Control Plane

**Document ID:** ACP-GOV-CURSOR-RISK-001  
**Layer:** L2 — Risk Policy (6-layer governance)  
**Governs:** Cursor-as-developer (not runtime agents — see `config/policies.yml`)  
**Authority:** Claude architect for policy changes; subordinate to `ARCHITECTURE.md` invariants  
**Parent:** [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md)  
**Read before:** Any non-trivial Cursor task

---

## 1. Task risk classification

Classify every task **before** coding. When uncertain → escalate to the higher risk level.

**Priority stack:** L0 behavior > L1 context > **L2 risk** > L3 guardrails > L4 evaluation > L5 memory.

### LOW — proceed without approval

**Characteristics:** No `src/` changes, isolated scope, fully reversible.

- docs-only (`*.md`, `docs/**`)
- **test-only** additions (no `src/` in diff)
- comment or docstring fixes
- non-breaking dependency bumps in `pyproject.toml`
- GitHub issue hygiene (comments, labels, individual `Closes #N`)

**Constraints:**

- Max **50** LOC changed (net diff)
- Allowlist: `*.md`, `docs/**`, `tests/**`, `pyproject.toml`, `.github/**` (templates only)
- No `src/` files — if needed, reclassify **MEDIUM**

**Verify:**

```bash
git diff --name-only master | grep '^src/' && exit 1 || true
```

---

### MEDIUM — state plan first, then proceed

**Characteristics:** New functionality in non-critical modules.

- new test files **paired with** `src/` fixes
- CLI subcommand additions or fixes
- new API endpoints (non-schema-breaking)
- `config/loader.py` additions (`load_*`)
- migration scripts or utilities
- sprint report creation

**Constraints:**

- Max **200** LOC changed
- Plan required: *Files I will touch · Assumptions · Verify command*
- One risk level per PR — do not combine with HIGH/CRITICAL
- Forbidden without separate HIGH/CRITICAL task: `core/policies.py`, `core/models.py`

**Verify:**

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
```

---

### HIGH — Claude architecture review before implement

**Characteristics:** Core domain logic, schema changes, security-adjacent.

- `core/models.py` (new types, field changes)
- `core/identity.py` authentication logic
- `config/loader.py` schema-breaking loader changes
- `api/server.py` schema-breaking changes
- `mcp/git_server.py` policy gate changes
- `core/quota.py` rate-limit logic
- new Pydantic models in `api/schemas.py`
- `apex/**` design and wiring (non–SAPAL-act execution)
- changes touching **3+ modules** simultaneously

**Constraints:**

- Max **300** LOC changed
- Claude reviews spec **before** Cursor implements
- PR body: `Architecture decision: [why this approach]`
- Document scope reductions: `Scope reduction: [item] → [milestone] because [reason]`
- Forbidden: combine HIGH + MEDIUM/LOW in one PR

**Verify:** full gate + shipped parity:

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config
```

---

### CRITICAL — human explicit approve before starting

**Characteristics:** Invariant-touching, security-critical, irreversible at scale.

- any change to **8 invariants** in `ARCHITECTURE.md`
- `core/policies.py` (PolicyEngine, ConditionEvaluator, ApprovalGate)
- ABAC evaluator additions (affects all policy decisions)
- identity contract changes (HTTP 401 vs 200+deny semantics)
- persistence format changes (`FileTaskStore`, Redis keys)
- `apex/` **SAPAL loop execution** (act path, not proposal-only)
- removing or deprecating public API endpoints
- any change to documented **fail-closed** behavior

**Process:**

1. Human reads spec and types **approved** in chat
2. Claude writes architecture spec (not code)
3. Cursor implements per spec
4. Human reviews diff before merge
5. Separate invariant compliance pass

**Constraints:**

- LOC: no hard cap if human approves full scope upfront; default split target ≤300 unless waived
- Forbidden: start without step 1

**Verify:** same as HIGH + explicit invariant checklist in PR body.

---

## 2. Forbidden operations — absolute (no exceptions)

| ID | Operation | Why |
|----|-----------|-----|
| **F1** | Direct push or force-push to `master` | Branch protection convention |
| **F2** | Remove, rename, or weaken any **8 invariant** | Architectural foundation |
| **F3** | Import OSS policy runtimes into `core/` (CrewAI, LangChain, …) | Invariant #1 |
| **F4** | Combine different risk levels in one PR | Bisectability; audit clarity |
| **F5** | Commit without running verify gate | Local-only misses (`DEVELOPMENT_PROTOCOL.md` §5.5) |
| **F6** | Issue ranges in PR body (`Closes #52..#62`) | GitHub parses only first (P-03) |
| **F7** | Mark sprint DONE before all sprint PRs on `master` | Step 7 timing (P-05) |
| **F8** | Skip “state assumptions” for ABAC/policy/loader work | Silent skip (P-04) |
| **F9** | Delete or archive `LESSONS_LEARNED.md` entries | Audit trail (P-11) |
| **F10** | `core/` imports from `mcp/` or `cli/` | Dependency direction |
| **F11** | Doc-only PR touching `src/**` | Scope creep (P-02) — reclassify MEDIUM |

**Historical waivers:** Path B (#48, #63) — one-time; see `PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md`. No new waivers without §5.

---

## 3. PR size enforcement

| Risk | Max LOC (net diff) | Waiver |
|------|-------------------|--------|
| LOW | 50 | None — reclassify or split |
| MEDIUM | 200 | Claude architect + documented reason |
| HIGH | 300 | Claude architect + why split not possible |
| CRITICAL | Human-approved scope | Human approves entire scope before start |

**Check:**

```bash
git diff master --stat | tail -1
```

If MEDIUM/HIGH exceeded:

1. Stop — do not commit
2. Split at natural boundary
3. New branch per sub-task
4. Ask Claude for split plan if unclear

---

## 4. Mandatory PR body template

Every PR to `master` must include:

```markdown
Risk level: [LOW / MEDIUM / HIGH / CRITICAL]

Files touched:
- [path] — [why]

Assumptions made:
- [assumption]
(or: No assumptions — task was fully specified)

Scope reductions (if any):
- [item] → [milestone] because [reason]
(or: N/A)

Closes #N
Closes #M
(individual lines — no ranges)

Verify gate passed:
- [ ] ruff check src/ tests/
- [ ] mypy src/ai_control_plane/ --strict
- [ ] pytest tests/ -v
- [ ] pytest tests/test_smoke.py -v -m smoke
- [ ] pytest tests/test_shipped_config_parity.py -v -m shipped_config (HIGH+)
```

GitHub template: [`.github/pull_request_template.md`](../../.github/pull_request_template.md)

---

## 5. Waiver process

Waivers require **Claude architect** written approval in chat **and** human acknowledgment for HIGH+.

- Document in [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md)
- PR body: `Waiver: [rule] waived because [reason], approved by Claude [date]`
- Same waiver type **not twice** per milestone without new lesson row

---

## 6. File allowlists (L3 — enforce with risk level)

| Task type | Allowed | Forbidden |
|-----------|---------|-----------|
| **docs-only** | `*.md`, `docs/**`, `CHANGELOG.md` | `src/**`, `tests/**` |
| **test-only** | `tests/**`, `tests/fixtures/**` | `src/**` (→ MEDIUM if needed) |
| **core/** | `src/ai_control_plane/core/**`, matching tests | `api/**`, `mcp/**`, `cli/**` unless in scope |
| **api/** | `src/ai_control_plane/api/**`, related tests | `core/policies.py` without CRITICAL path |

---

## 7. Module ownership (review triggers)

| Module | Default risk | Reviewer |
|--------|--------------|----------|
| `core/policies.py` | CRITICAL | Claude arch + human |
| `core/models.py` | HIGH | Claude arch |
| `config/loader.py` | HIGH | Claude arch |
| `core/identity.py` | HIGH | Claude arch |
| `api/server.py` | MEDIUM–HIGH | Invariant checklist |
| `apex/**` (SAPAL act) | CRITICAL | Claude design + human |
| `apex/**` (other) | HIGH | Claude design spec first |
| `mcp/**` | MEDIUM | Invariant #3 |
| `tests/**`, `docs/**` | LOW | Self |

---

## 8. PR hygiene

- Branch: `{risk}/{issue-id}-{short-desc}` (e.g. `low/test-cli-gov-coverage`)
- HIGH/CRITICAL: diff summary per invariant touched
- Link patterns: [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md) P-01..P-13

---

## 9. Verify gate (mandatory — L4)

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config
```

Baseline: **165+** pytest, smoke **8/8** (HTML deploy artifact “156” is stale).

---

## 10. Operator monitoring contracts (runtime — L4)

### Kill switch (P-13)

When `kill_switch.active: true` in `config/policies.yml`:

| Endpoint | HTTP | Body signal |
|----------|------|-------------|
| `POST /policy/evaluate` | **200** (not 503) | `allowed: false`, `reason: "kill_switch_active: …"` |
| `GET /health` | **200** | Exempt — process up; does **not** prove kill switch off |

**Rule:** Kill switch activation is an operator action. Alerts must watch `allowed=false` + `reason`, or `policies.yml` `kill_switch.active` — **not** HTTP 5xx alone.

**Evidence:** Study 05 drill 5g G2-1 @ 2026-06-26 — [`practice-evidence/study-05-advanced-surprises/artifacts/terminal-5g-g2-killswitch.md`](practice-evidence/study-05-advanced-surprises/artifacts/terminal-5g-g2-killswitch.md).

**Prevention check:**

```bash
# When kill switch is intentionally active:
curl -sf -X POST "${ACP_API_URL}/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -c "import sys,json; d=json.load(sys.stdin); assert not d['allowed'] and d['reason'].startswith('kill_switch_active')"
```

---

**Reconciliation:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md)  
**Last updated:** 2026-06-26 @ §10 kill switch monitoring (P-13, G2-1)
