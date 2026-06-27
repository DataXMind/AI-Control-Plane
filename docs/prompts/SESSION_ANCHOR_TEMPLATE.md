# Session anchor template (L5 — copy into every Cursor chat)

> **Use:** Paste this block as the **first message** (or pin) when starting a session.  
> **Policy:** [`AGENTS.md`](../../AGENTS.md) · [`CURSOR_RISK_POLICY.md`](../governance/CURSOR_RISK_POLICY.md) · Gold pattern: [`GP-01`](../governance/gold-patterns/GP-01-agent-session-memory.md)

---

## PB-12 operator gates — pinned checklist

> SSOT: [`TASK_AUDIT_REMAINING_2026-06-27.md`](../governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) · [`PUBLIC_BETA_OPERATOR_ACTION_PLAN.md`](../governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md) · `master` @ v1.3.3

**Chờ bạn / calendar**

- [ ] PB-9 daily tick → *"đã tick ngày YYYY-MM-DD"* only · review ~**2026-07-06**
- [ ] PB-7 CLEAN fork (laptop riêng, không MSI WARM)
- [ ] security@ mailbox + test email

**Sau PB-9 / flip:** PB-10 soak 30d → PB-8 rc tag → PB-6 OpenAPI → **PB-12 go/no-go**

**Không claim:** PB-7 trên WARM; PB-9 trước Day 14; CS-01/03/04 runtime drill

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/governance/status" | jq '.public_beta | {gates_remaining, gates_closed}'
```

---

## Anchor block (fill all fields)

```yaml
session_anchor:
  version: "1.0"
  date: "YYYY-MM-DD"
  baseline: "master @ <git-sha>"      # e.g. c6e8cc1
  risk: "LOW | MEDIUM | HIGH | CRITICAL"
  track: "feature | governance | ops | docs-only"
  gates_approved: []                 # e.g. ["A"] or ["C","A"] — see PRE_APPROVAL_AUDIT §11
  issue: "#NN or N/A"
  branch: "low/issue-short-desc or N/A"

memory_tier:
  read_first:                        # @-mention in Cursor
    - AGENTS.md
    - docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md   # governance / G1+ / PB-12
    - docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md  # PB-12 operator checklist
    - ARCHITECTURE.md                # if non-trivial code
  durable_context:                   # repo paths, not chat
    - docs/governance/GOVERNANCE_NEXT_PHASE_PLAN.md
    - docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md

file_allowlist:
  allowed:
    - path/to/file
  forbidden:
    - src/**                         # if docs-only

assumptions:
  - "Files I will touch: ..."
  - "If wrong, I will stop and ask: ..."

verify:
  - "ruff check src/ tests/"
  - "mypy src/ai_control_plane/ --strict"
  - "pytest tests/ -v"
  - "pytest tests/test_smoke.py -v -m smoke"
  # task-specific below

task: |
  One paragraph — goal, out of scope, done definition.

acceptance:
  - "[ ] ..."
```

---

## Example (governance docs-only)

```yaml
session_anchor:
  version: "1.0"
  date: "2026-06-25"
  baseline: "master @ c6e8cc1"
  risk: "LOW"
  track: "governance"
  gates_approved: ["pre-approval audit reviewed — Gate C pending"]
  issue: "N/A"
  branch: "low/gov-l5-memory-pack"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md
  durable_context:
    - docs/governance/L5_MATURITY_MODEL.md

file_allowlist:
  allowed:
    - docs/governance/**
    - .cursor/rules/**
    - AGENTS.md
  forbidden:
    - src/**

assumptions:
  - "Docs-only; no API contract changes."
  - "If src/ needed, stop and reclassify MEDIUM."

verify:
  - "git diff --name-only master | grep '^src/' → empty"
  - "bash scripts/verify_governance_memory.sh"

task: |
  Refresh L5 maturity docs and wire CI governance-memory gate.

acceptance:
  - "[ ] ML5 checklist items documented"
  - "[ ] verify_governance_memory.sh passes"
```

---

## Runtime optional (operator)

```bash
export ACP_API_URL=http://localhost:8000
agentctl gov status --json | python3 -m json.tool
```

---

## Session close (Evolve)

- [ ] Issue/PR comment with outcome
- [ ] `LESSONS_LEARNED.md` if pitfall repeated (new P-xx row)
- [ ] `practice-evidence/` if operator ran hands-on steps
- [ ] Do **not** store sole copy of evidence in chat

**Last updated:** 2026-06-27 — PB-12 operator checklist pinned
