# Current session anchor — copy-paste block (living snapshot)

**Document ID:** ACP-PROMPT-ANCHOR-CURRENT-001  
**Update rule:** Maintainer or closing agent updates this file after **major merge** to `master` (governance bump, roadmap PR batch, PB-9 milestone).  
**Structure SSOT:** [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md) · **Framework:** [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md)

> Paste the block below as the **first message** in Cursor / Claude / Codex. Fill `task:` for your session.

---

## Canonical one-liner (2026-07-03)

```text
SESSION ANCHOR: master @ 4274825 · catalog v1.5.0 · 17 patterns · pytest 221 · risk LOW
TRACK: [fill: feature | governance | ops | docs-only]
Public Beta IN_PROGRESS (PB-9 soak). gates_blocking_pb12: PB-9, PB-12 · gates_remaining: 7 until flip bump.
Critical path: PB-9 tick 07-04..05 → Day 14 ~2026-07-06 → pre-flip ~07-07 → PB-12 ~07-10.
PB-9 last tick: 2026-07-03 AM (Apex ☑ soak_iter @ 04:13:19Z). PB-10 deferred GA (#78). PB-8 @ c58b4cc — no re-tag.
Tier A pilot: PASS Mac Mini 2026-06-30 — practice-evidence/mac-pilot-deploy-2026-06-30 (#176 merged)
Verify: source .venv/bin/activate · smoke 8/8 · verify_governance_memory.sh · pytest 221
SSOT: AGENT_OPERATING_SYSTEM.md · END_USER_VALUE.md · MANUAL_OPERATOR_PLAYBOOK.md (no Agent for daily ops)
```

---

## Quick YAML (optional — multi-PR / governance)

```yaml
session_anchor:
  version: "1.0"
  date: "2026-07-03"
  baseline: "master @ 4274825"
  risk: "LOW"
  track: "docs-only"
  gates_approved: []
  issue: "N/A"
  branch: "docs/your-branch"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/prompts/AGENT_OPERATING_SYSTEM.md
    - docs/END_USER_VALUE.md
    - docs/governance/MANUAL_OPERATOR_PLAYBOOK.md
  durable_context:
    - docs/governance/PB9_STAGING_SOAK_LOG.md
    - docs/governance/GOVERNANCE_DRIFT_RECONCILIATION.md

file_allowlist:
  allowed:
    - docs/**
    - README.md
    - examples/minimal/CUSTOMER_INSTALL.md
  forbidden:
    - src/**

verify:
  - "bash scripts/verify_governance_memory.sh"
  - "pytest tests/test_smoke.py -v -m smoke"
  - "pytest tests/ -v"

task: |
  [One paragraph — goal, out of scope, done definition]
```

**Last updated:** 2026-07-03 · baseline `4274825` · PB-9 tick 07-03
