# Cursor Prompt Packet — Post Milestone C (hygiene + doc truth)

> **Status:** Steps 1-4 + Public Beta prep 2026-06-24 — see [`PUBLIC_BETA_SPRINT_PLAN.md`](governance/PUBLIC_BETA_SPRINT_PLAN.md)  
> **Ref:** [`ACP_FULL_AUDIT_RECONCILIATION.md`](ACP_FULL_AUDIT_RECONCILIATION.md)

Execute in order. Docs-only unless noted.

---

## Cursor Prompt 1 — Remaining HIGH doc drift (30 min)

```
@ARCHITECTURE.md
@docs/governance/PHASE1_REPORT_V2.md
@docs/governance/ACP_FULL_AUDIT_RECONCILIATION.md

Task: Fix remaining HIGH doc drift from reconciliation §7.

Fix 1 — ARCHITECTURE.md §API surface
Add rows after GET /quota/{project_id}:
| GET | /quota/agent/{agent_id} | AgentQuotaStatus |
| GET | /quota/profile/{profile_id} | ModelProfileQuotaStatus |
| GET | /telemetry/events | list[TelemetryEvent] |
| GET | /apex/status | apex cycle status |
| POST | /apex/trigger | run one SAPAL cycle |

Fix 2 — PHASE1_REPORT_V2.md
- §4.2: move GAP-Q-1 to §4.1 closed (MB-S2-11); note GAP-S4-1 partial (#9 open)
- §5: update mcp/server_factory, CLI approve/quota, apex live
- §6: invariant #5 apex live MVP; #7 Redis when ACP_REDIS_URL

Fix 3 — OPEN_SOURCE_READINESS.md §Milestone mapping
| Milestone A | CLOSED 2026-06-23 (#38) |
| Milestone B | CLOSED 2026-06-24 (PR #51) |
| Milestone C (boundary) | CLOSED 2026-06-24 (PR #63) |
| Public Beta | not started |

Verify: pytest tests/ -q (docs-only, no regression)
```

---

## Cursor Prompt 2 — Expand Milestone B line in ARCHITECTURE (15 min)

```
@ARCHITECTURE.md
@docs/governance/MILESTONE_B_BACKLOG.md

Update Milestone B one-liner to full Sprint 2 scope (Redis quota, FileTaskStore,
JWKS, ActionRegistry, MCP HTTP, CLI live, quotas by_agent/profile) — CLOSED PR #48-51.

Verify: ruff not required (markdown only)
```

---

## Cursor Prompt 3 — Milestone C+ issue seeding (after Claude ADR)

```
@docs/prompts/CLAUDE_PROMPT_MILESTONE_C_PLUS.md
@docs/governance/MILESTONE_C_PLUS_ADR.md

Prerequisite: Human approves Claude ADR pack.

Create GitHub issues from ADR §7 only — label milestone-c-plus, spec-gap.
Do NOT implement until second human approve on each issue.

Suggested seeds (if ADR not ready, defer):
- C+-1 TelemetryStore.replay() API
- C+-2 OTel collector config + sense adapter
- C+-3 Argos analyze pipeline design impl
- C+-4 Darts predict adapter + [apex] extras
- C+-5 ActAdapter PolicyEngine gate (per ADR option)
- C+-6 cyanheads MCP E2E CI job
```

---

## Cursor Prompt 4 — B+ debt (#9, #39)

```
@src/ai_control_plane/config/loader.py
@src/ai_control_plane/api/server.py
@docs/governance/ACP_FULL_AUDIT_RECONCILIATION.md

Issue #9: Wire load_model_profiles() into AppState (or document why quota-only is sufficient).
Issue #39: Extend HealthResponse if AC requires fields beyond config wire proof.

Standard+ task — full DEVELOPMENT_PROTOCOL 9-step.
```

---

## Verification gate (all prompts)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
ruff check src/ tests/
mypy src/ai_control_plane --strict
pytest tests/ -q
pytest tests/test_smoke.py -m smoke -q
```

Expected: **156 passed**, smoke **8/8**.

---

**Do not** re-open closed MC issues #52–#62 unless regression found.

---

## Public Beta sprint (current)

Execute [`PUBLIC_BETA_SPRINT_PLAN.md`](governance/PUBLIC_BETA_SPRINT_PLAN.md) PB-1..12.

**Human approve before:** PB-12 public repo flip, PB-9 soak start, GitHub Team upgrade (PB-11).

**Go/No-Go:** [`PUBLIC_BETA_GO_NO_GO.md`](governance/PUBLIC_BETA_GO_NO_GO.md)

---

**Status:** Steps 1-4 executed 2026-06-24 — audit prompts 1-3 closed; Public Beta prep started
