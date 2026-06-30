# Agent Operating System (AOS) — AI Control Plane

**Document ID:** ACP-AOS-001  
**Version:** 1.0  
**Audience:** Cursor · Claude (Projects / Code / CLI) · OpenAI Codex · any coding agent  
**Baseline:** `master` @ `bbc65cf` · catalog **v1.5.0** · **17** LESSON patterns · pytest **181**  
**Gold pattern:** [`GP-01`](../governance/gold-patterns/GP-01-agent-session-memory.md)  
**Companion:** [`AGENTS.md`](../../AGENTS.md) · [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md)

> **Purpose:** One scientific framework so every agent understands **what ACP is**, **how to work here**, and **where truth lives** — without relying on chat memory.

---

## 1. Project mental model (read before any task)

### 1.1 What ACP is (core business)

**AI Control Plane** is an **AI Agent Policy Engine** — enforcement between agents and resources.

| Does | Does not |
|------|----------|
| Fail-closed `POST /policy/evaluate` | Content moderation / prompt injection filter |
| Config-driven YAML policies (`ACP_CONFIG_DIR`) | Agent orchestration (LangGraph/CrewAI) |
| Audit log per decision (`agent_id`, action, outcome) | Full observability platform |
| HTTP bridge + optional MCP git facade | Replace OSS policy engines |

**Phase:** Milestones A–C+ **CLOSED** · Public Beta **IN_PROGRESS** (PB-9 soak → PB-12 flip ~07-10).

### 1.2 Key components (code map)

```text
src/ai_control_plane/
├── core/           # PolicyEngine, models, quota, identity, task_store, telemetry
│   ├── policies.py # CRITICAL — never replace with OSS engine (Inv #1)
│   ├── models.py   # HIGH — all data contracts (Inv #2)
│   └── governance_catalog.py  # gates_remaining SSOT (flip bump @ PB-12)
├── api/server.py   # FastAPI — ONLY TS bridge (Inv #6)
├── config/loader.py# ACP_CONFIG_DIR resolution (Inv #8)
├── mcp/git_server.py # Facade only (Inv #3) — [mcp-unverified] @ 0.x
├── cli/            # agentctl — calls core/api only (Inv #4)
└── apex/           # SAPAL experimental (Inv #5) — demoted @ 0.x
```

### 1.3 Main artifacts (what ships)

| Artifact | Path | Role |
|----------|------|------|
| Library + API | `src/ai_control_plane/` | Runtime |
| Shipped config | `config/*.yml` | Defaults; override via `ACP_CONFIG_DIR` |
| Fixture config | `tests/fixtures/config/` | CI / smoke / PB-9 soak (8 rules) |
| Examples | `examples/minimal/` | Docker, PB-9, optional production override |
| OpenAPI | `docs/openapi/openapi.json` | Via `scripts/export_openapi.py` only |
| Governance UX | `GET /governance/status` | Catalog, gates, lessons — not HTML snapshots |
| Practice evidence | `docs/governance/practice-evidence/` | Hands-on PASS/FAIL |
| Operator soak | `PB9_STAGING_SOAK_LOG.md` + iteration logs | Human + machine ML5 |

### 1.4 Infra topology (operator)

```text
[Agents] --POST /policy/evaluate--> [ACP API :8000]
                                        |
                    +-------------------+-------------------+
                    |                   |                   |
              ACP_CONFIG_DIR      ACP_DATA_DIR         ACP_REDIS_URL (opt)
              (YAML policies)     (tasks/telemetry)    (quota persistence)
```

| Deploy path | Use |
|-------------|-----|
| `examples/minimal/docker-compose.yml` | PB-9 soak, CI parity (fixture) |
| `docker-compose.production.yml` | Pilot Tier A — **parallel**, not soak SSOT |
| `ghcr.io/dataxmind/ai-control-plane:demo` | CONNECT door (private until PB-12) |
| VPS systemd | 24/7 soak — [`examples/minimal/systemd/`](../../examples/minimal/systemd/) |

### 1.5 Eight invariants (never violate)

See [`ARCHITECTURE.md`](../../ARCHITECTURE.md) §8 Hard Invariants. Agent **stops** if a task would break any invariant — opens issue, does not patch silently.

---

## 2. Karpathy 6-layer governance

| Layer | Authority | Agent loads |
|-------|-----------|-------------|
| **L0** | `.cursorrules`, `CLAUDE.md` | Simplicity, surgical diff, state assumptions |
| **L1** | `ARCHITECTURE.md`, `DATA_CLASSIFICATION.md` | Module ownership before non-trivial code |
| **L2** | `CURSOR_RISK_POLICY.md` | LOW/MED/HIGH/CRITICAL + file allowlist |
| **L3** | `CONTRIBUTING.md`, branch naming | PR-only `master`; 1 risk level per PR |
| **L4** | CI, `DEVELOPMENT_PROTOCOL.md` §5.5 | Smoke 8/8 + full suite before merge |
| **L5** | `LESSONS_LEARNED.md`, plans, evidence | Tier C durable memory |

**Harness vs policy:** ECC-style skills map to layers ([`ECC_ACP_LAYER_MAP.md`](../governance/ECC_ACP_LAYER_MAP.md)). Runtime allow/deny stays **`POST /policy/evaluate`** — not agent chat rules.

---

## 3. Memory tiers + anti-drift

### 3.1 Three tiers (GP-01)

| Tier | Storage | Lifetime | Who writes |
|------|---------|----------|------------|
| **A — Auto** | `.cursorrules`, `.cursor/rules/*.mdc`, user rules | Every session | Maintainers |
| **B — Session** | Anchor in chat + `@` files + issue/PR | One task | Agent + human |
| **C — Durable** | Soak logs, `practice-evidence/`, `LESSONS_LEARNED.md` | Months | **Human operator** (agent assists draft only) |

**Rule:** If it must survive a **new chat** or **new account** → **Tier C** (or update `ANCHOR_CURRENT.md`).

### 3.2 SSOT hierarchy (conflict resolution)

```text
code + ARCHITECTURE.md
  > practice-evidence/*/RESULTS.md + PRACTICE_STUDIES_AUDIT_01-07.md
  > GET /governance/status (runtime catalog)
  > GOVERNANCE_DRIFT_RECONCILIATION.md
  > HTML governance snapshots (HISTORICAL — reject as current)
```

### 3.3 Context hygiene — keep vs discard

| **Keep** (high value) | **Discard** (low value / harmful) |
|------------------------|-----------------------------------|
| `baseline: master @ <sha>` from `ANCHOR_CURRENT.md` | Old chat summaries without SHA |
| `gates_remaining` / `gates_blocking_pb12` from runtime curl | Claim "only PB-9 blocks" (7 gates in catalog) |
| File allowlist + risk in anchor | Full-file paste when `path:line` citation works |
| Operator calendar dates (Day 14 = ~07-06) | "HOÀN TẤT" without evidence path |
| PROPOSED vs IMPLEMENTED (ADR-002, k6, MCP) | Treating PROPOSED docs as shipped code |
| SEV-3 documented vs SEV-1/2 | Confusing manual restart with fail-open |

**Anti-drift ritual (start of session):**

1. Read [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) (30 seconds).
2. If task touches gates/soak → read [`GOVERNANCE_DRIFT_RECONCILIATION.md`](../governance/GOVERNANCE_DRIFT_RECONCILIATION.md) §1.
3. If claim sounds like PASS → require **Tier C path** or stop.

### 3.4 Practice PASS ≠ catalog closed

Until **PB-12 flip**, maintainer bumps `governance_catalog.py`. Agents **must not** edit gates to "match practice" without explicit H1-06 approval.

---

## 4. PACE — mandatory workflow

### 4.1 Session PACE (every session)

| Step | Action |
|------|--------|
| **P** Plan | Read AOS + anchor; classify L2 risk; read `ARCHITECTURE.md` if code |
| **A** Act | Surgical diff; respect allowlist; ≤3 retrieval rounds then Pause |
| **C** Check | `ruff`, `mypy`, `pytest`; smoke 8/8 for any PR |
| **E** Evolve | PR body; update Tier C if sprint close; **never** sole evidence in chat |

### 4.2 Task PACE (Standard+ / HIGH)

| Step | Action |
|------|--------|
| **P** Pause | Impact analysis — no patch yet |
| **A** Anchor | Done/pending in issue or anchor YAML |
| **C** Confirm | Human/architect for P0, schema, policy |
| **E** Execute | Patch + verify + commit **only when human asks** |

### 4.3 Smoke gate (L4 — non-negotiable for PR)

```bash
source .venv/bin/activate          # WSL — system Python fails (structlog)
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke    # 8/8
```

Post-merge / runtime (Docker fresh build):

```bash
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh   # catalog · patterns
pytest --collect-only -q | tail -3                  # 181 @ bbc65cf
```

Full protocol: [`DEVELOPMENT_PROTOCOL.md`](../DEVELOPMENT_PROTOCOL.md).

---

## 5. Session anchor — placement rules

| When | Where | What |
|------|-------|------|
| **New Cursor chat** | First user message (pin) | Block from [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md) + `task:` |
| **New Claude Project chat** | First message after Instructions | Opener in [`CLAUDE_CODEX_PLAYBOOK.md`](CLAUDE_CODEX_PLAYBOOK.md) |
| **Multi-PR governance track** | YAML block in anchor | `gates_approved`, `file_allowlist`, `forbidden` |
| **Session close** | PR body + optional `LESSONS_LEARNED` | Outcome, SHA, verify output |

**Wrong:** Anchor only in agent's head · anchor at end of long chat · stale SHA from HTML report.

**Right:** Anchor **before** first tool call · SHA from `git log -1` · update `ANCHOR_CURRENT.md` after roadmap merge batch.

---

## 6. Platform routing matrix

| Capability | **Cursor** | **Claude Project** | **Claude Code CLI** | **Codex** |
|------------|------------|--------------------|--------------------|-----------|
| Edit repo files | ✅ | ❌ (draft text only) | ✅ | ✅ (sandbox) |
| `git commit/push` | ✅ human-directed | ❌ | ✅ human-directed | ✅ human-directed |
| `pytest` / docker | ✅ | ❌ (cite commands) | ✅ | ✅ |
| PB-9 soak **tick** | ⚠️ only on operator *"đã tick ngày …"* | ❌ draft row only | ⚠️ same as Cursor | ⚠️ same |
| PB-12 public flip | ❌ human only | ❌ advise only | ❌ | ❌ |
| Best for | Implementation, PRs, CI | Audit, Day 14 draft, prompt review | Terminal workflow | Focused patches |
| Onboarding doc | [`CURSOR_NEW_SESSION_PLAYBOOK.md`](CURSOR_NEW_SESSION_PLAYBOOK.md) | [`CLAUDE_PROJECT_SETUP.md`](CLAUDE_PROJECT_SETUP.md) | [`CLAUDE_CODEX_PLAYBOOK.md`](CLAUDE_CODEX_PLAYBOOK.md) §2 | [`CLAUDE_CODEX_PLAYBOOK.md`](CLAUDE_CODEX_PLAYBOOK.md) §3 |

**Split of labor (DEVELOPMENT_PROTOCOL):**

- **Claude** → architecture, plan, task packet, reject naive wiring  
- **Cursor / Codex / Claude Code** → execute, verify, PR diff  
- **Human** → approve scope, merge, operator calendar, signatures  

---

## 7. Task types — standard packets

| Track | Risk | Allowlist | Verify |
|-------|------|-----------|--------|
| `docs-only` | LOW | `docs/**` only | smoke 8/8; no `src/` in diff |
| `governance` | LOW | `docs/governance/**`, catalog if flip | smoke + `verify_governance_memory.sh` |
| `feature` | MED–HIGH | per `CURSOR_RISK_POLICY` | full pytest + smoke |
| `ops` | LOW | scripts, examples | smoke; operator runs soak |
| `PROPOSED ADR` | LOW | ADR + README | smoke; **STATUS: PROPOSED** line |

Template: [`_TEMPLATE.md`](_TEMPLATE.md).

---

## 8. Forbidden (all platforms)

- Push/merge `master` without human instruction  
- Weaken `ARCHITECTURE.md` invariants  
- Invent PB-9 soak results or tick future dates  
- Close `gates_remaining` in chat or code without H1-06  
- `Closes #52..#62` range in PR body  
- Mix risk levels in one PR  
- Implement PROPOSED items (ADR-002 OIDC, k6 fleet CI, MCP E2E) without flip + maintainer branch  
- Import AgentShield / ECC plugin stack — **REJECTED** ([`ECC_ACP_INTEGRATION_ANALYSIS.md`](../governance/ECC_ACP_INTEGRATION_ANALYSIS.md) §4)  

---

## 9. Public Beta critical path (shared truth)

```text
[M1 operator soak + tick 07-01..05]
        → [C1 Day 14 ~07-06] → [C1-02 pre-flip ~07-07]
        → [H1 PB-12 ~07-10] → [D1 PB-10 #78 GA track]
```

**Human-only ops:** [`MANUAL_OPERATOR_PLAYBOOK.md`](../governance/MANUAL_OPERATOR_PLAYBOOK.md) — **no Agent required** for daily ritual.

**Agent may:** draft `DAY14_REVIEW_DRAFT` → `RESULTS.md`, fix doc drift, prepare catalog bump PR **after** H1-02 GO.

---

## 10. New session checklist (any platform)

- [ ] Paste anchor from [`ANCHOR_CURRENT.md`](ANCHOR_CURRENT.md)  
- [ ] Read [`AGENTS.md`](../../AGENTS.md) if multi-file or governance  
- [ ] Classify risk (L2) + file allowlist  
- [ ] Confirm task not blocked by calendar (PB-9 / PB-12) unless docs-only  
- [ ] Run verify before claiming done  
- [ ] Session close: PR link + SHA — not "done" in chat alone  

---

## 11. Related documents

| Doc | Role |
|-----|------|
| [`docs/prompts/README.md`](README.md) | Prompts index |
| [`L5_MATURITY_MODEL.md`](../governance/L5_MATURITY_MODEL.md) | ML5 target |
| [`GOVERNANCE_DRIFT_RECONCILIATION.md`](../governance/GOVERNANCE_DRIFT_RECONCILIATION.md) | Drift SSOT |
| [`PUBLIC_BETA_GO_NO_GO.md`](../governance/PUBLIC_BETA_GO_NO_GO.md) | Flip checklist |
| [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](../governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md) | Deep audit snapshot |

**Last updated:** 2026-06-30 · AOS v1.0 · baseline `bbc65cf`
