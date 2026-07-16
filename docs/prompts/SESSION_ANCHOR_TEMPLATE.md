# Session anchor template (L5 — copy into every Cursor chat)

> **Use:** Paste [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) every session (living facts). Use **this file** for full YAML structure, drift reject list, and examples.  
> **Framework:** [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) · [`AGENTS.md`](../../AGENTS.md) · [`GP-01`](../governance/gold-patterns/GP-01-agent-session-memory.md)

---

## Current status, gates, and drift

> **Do not maintain a second copy of live facts here.** SHA, catalog version, test count,
> `gates_remaining`, and dated drift-reject claims live in **only one place:**
> [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) (updated after every major `master` merge) and
> `GET /governance/status`. A dated snapshot pasted into this template drifts the moment
> it's written — see [`LESSONS_LEARNED.md`](../governance/LESSONS_LEARNED.md) P-07 / P-18.

```text
SESSION ANCHOR: paste the block from ANCHOR_CURRENT.md — this template carries no
dated values of its own.
```

---

## PACE verify (operator / pre-task)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke                   # 8/8 — fixed count, not catalog-dependent
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh          # compare output vs ANCHOR_CURRENT.md
bash scripts/verify_openapi_runtime.sh                    # compare output vs ANCHOR_CURRENT.md
bash scripts/run_ecc_deep_audit.sh                        # optional: full post-verify battery
```

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/governance/status" | jq '.public_beta | {gates_remaining, gates_closed}'
```

---

## Structural / naming drift — reject these claims (timeless, not date-bound)

- `examples/docker-compose.yml` → `examples/minimal/docker-compose.yml`
- CI job `examples-smoke` → `examples-minimal-smoke`
- `curl … > docs/openapi.json` → `python scripts/export_openapi.py` → `docs/openapi/openapi.json`
- `export ACP_CONFIG_DIR` on host changes Docker pilot → use `ACP_HOST_CONFIG_DIR` in `.env.production` ([`PRODUCTION_DEPLOY.md`](../../examples/minimal/PRODUCTION_DEPLOY.md))
- `bash scripts/verify_*` from `examples/minimal/` → **repo root** (`cd ../..`)
- Mac `unknown command: docker compose` → install Compose plugin (Docker Desktop or `docker-compose` standalone)
- Pilot `policy_rules_count: 10` = Profile **B** — not drift vs fixture **8** (smoke)
- Pilot PASS on one stack (e.g. Mac) ≠ PASS on another (e.g. a staging/production soak) — separate stacks, don't conflate results

**Dated/calendar drift (test counts, gate counts, PB-N status, "HOÀN TẤT" claims) is tracked in
[`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) only — do not hardcode a number here; it will go stale.**

| Claim | Verdict |
|-------|---------|
| AgentShield / ECC plugin import (skills, agents, npm dependency) | **REJECTED** — xem [`ECC_ACP_INTEGRATION_ANALYSIS.md`](../governance/ECC_ACP_INTEGRATION_ANALYSIS.md) §REJECT; không re-propose trừ khi operator yêu cầu rõ ràng bằng văn bản |
| AEOS Phase 2 bridge "not wired" | **REJECTED** — aeos `main` @ `9be7e2a`; [`aeos-acp-integration/RESULTS.md`](../governance/practice-evidence/aeos-acp-integration/RESULTS.md) |
| AEOS GitHub CI green | **REJECTED** until workflow passes — local gate green only |
| ACP integration PASS = SACP PASS | **REJECTED** — SACP evidence OPEN; see HYBRID_AI_GATEWAY.md §0 |

---

## Claude / Cursor role this phase

- AOS + platform playbooks: [`AGENT_OPERATING_SYSTEM.md`](AGENT_OPERATING_SYSTEM.md) · [`CURSOR_NEW_SESSION_PLAYBOOK.md`](CURSOR_NEW_SESSION_PLAYBOOK.md) · [`CLAUDE_CODEX_PLAYBOOK.md`](CLAUDE_CODEX_PLAYBOOK.md)
- **Claude Projects:** [`CLAUDE_PROJECT_SETUP.md`](CLAUDE_PROJECT_SETUP.md)
- **Manual ops (no Agent):** [`MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md)
- What's open right now (phase-specific work items) → [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) and `STATE/PROGRESS.md`

---

## Anchor block (fill all fields)

```yaml
session_anchor:
  version: "1.0"
  date: "YYYY-MM-DD"
  baseline: "master @ <git-sha>"      # e.g. 20e4fc3
  risk: "LOW | MEDIUM | HIGH | CRITICAL"
  track: "feature | governance | ops | docs-only"
  gates_approved: []
  issue: "#NN or N/A"
  branch: "low/issue-short-desc or N/A"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/governance/PUBLIC_BETA_OPERATOR_ACTION_PLAN.md
    - docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md
    - ARCHITECTURE.md                # if non-trivial code
  durable_context:
    - docs/governance/PUBLIC_BETA_GO_NO_GO.md
    - docs/governance/PB9_STAGING_SOAK_LOG.md

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
  date: "2026-06-28"
  baseline: "master @ 20e4fc3"
  risk: "LOW"
  track: "governance"
  gates_approved: ["docs-only — Karpathy track"]
  issue: "N/A"
  branch: "docs/example"

memory_tier:
  read_first:
    - AGENTS.md
    - docs/governance/PUBLIC_BETA_GO_NO_GO.md
  durable_context:
    - docs/governance/L5_MATURITY_MODEL.md

file_allowlist:
  allowed:
    - docs/governance/**
    - docs/prompts/**
  forbidden:
    - src/**

assumptions:
  - "Docs-only; no API contract changes."

verify:
  - "git diff --name-only master | grep '^src/' → empty"
  - "pytest tests/test_smoke.py -v -m smoke"

task: |
  Update governance evidence or session anchor.

acceptance:
  - "[ ] Tier C artifact path updated"
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

**Last updated:** 2026-07-16 — structure/template only; live SHA and gate status are in `ANCHOR_CURRENT.md`
