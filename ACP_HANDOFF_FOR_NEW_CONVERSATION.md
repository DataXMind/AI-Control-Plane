# AI Control Plane (ACP) — Complete Handoff Document
# For: New Claude conversation — full context transfer
# Audit date: 2026-06-27 | Baseline: master @ 527eb5d | Catalog: v1.3.3
# DataXMind/AI-Control-Plane (private repo → Public Beta ~2026-07-10)

---
> ## ⚠️ DEPRECATION NOTICE — 2026-06-30
>
> **This document is STALE for ops state** as of 2026-06-28+.
> Frozen snapshots may cite `v1.3.3` / `527eb5d` / `20e4fc3`.
>
> **Do NOT use for:** gate status, timeline, test counts, SHA, or open questions.
>
> **Still valid for architectural reference ONLY:**
> - PART 3 — 8 Hard Invariants (architectural, does not change)
> - PART 4 — Module structure, API surface, tool naming
> - PART 7 — Policy engine ABAC + telemetry hash-chain details
> - PART 14 — Key decisions record
> - PART 15 — Environment variables table
>
> **Current SSOT (use these instead):**
> - Ops / gates: `docs/prompts/SESSION_ANCHOR_TEMPLATE.md`
> - Full audit: `docs/governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`
> - ECC closeout: `docs/governance/ECC_48H_RESULTS.md`
> - Value tiers: `docs/governance/VALUE_AUDIT_MATRIX.md`
>
> **Runtime truth @ v1.5.0:**
> - `governance_version`: **1.5.0** · **17** patterns (P-17)
> - `gates_blocking_pb12`: typically **PB-9**, **PB-12** only
> - `gates_remaining`: **7** until maintainer catalog bump @ flip
> - pytest: **177** · smoke **8/8**
---

---

## PART 1 — CANONICAL ONE-LINER (paste first in every session)

> AI Control Plane @ master `527eb5d`: Milestones A–C+ CODE CLOSED. Public Beta
> IN_PROGRESS (PB-9 staging soak). Governance catalog v1.3.3 live. All Cursor technical
> packets MERGED. Seven operator gates remain until ~2026-07-06 review and ~2026-07-10
> flip target. Trust runtime `verify_*` scripts — not stale HTML prompts.

---

## PART 2 — WHAT THIS PROJECT IS

### 2.1 Core concept

**AI Control Plane (ACP)** là governance layer cho multi-agent AI systems. Nó govern
các AI coding agents (Cursor, Claude Code) đang build Rust Gateway project
(DataXMind/Hybrid-AI-Gateway). ACP không build Rust — nó govern agents đang build Rust.

```
AI Control Plane (Python — governs)
    └── Agent 1 (Infra/K8s)  ──┐
    └── Agent 2 (Rust Backend) ─┼──→ Hybrid-AI-Gateway (Rust codebase)
    └── Agent 3 (Reviewer)    ──┘
```

### 2.2 Package identity

- **Python package:** `ai_control_plane` (src/ layout, pyproject.toml)
- **CLI:** `agentctl` (Typer, via console_scripts)
- **API:** FastAPI at `api/server.py` — 13 HTTP endpoints
- **Config:** Pydantic v2 + PyYAML, path via `ACP_CONFIG_DIR` env var
- **Repo:** `DataXMind/AI-Control-Plane` (private → PB flip ~07-10)
- **Language choice:** Python (not Rust) — governance/orchestration layer,
  không có hot path, không cần Rust-level performance

---

## PART 3 — 8 HARD INVARIANTS (KHÔNG BAO GIỜ VI PHẠM)

```
1. core/policies.py   — custom PolicyEngine only. KHÔNG replace bằng OSS (CrewAI, LangChain)
2. core/models.py     — ALL data contracts ở đây và chỉ đây. Không duplicate types.
3. mcp/git_server.py  — facade ONLY. Không có git logic trong Python.
4. cli/               — HTTP calls only. Không import core/policies.py trực tiếp.
5. apex/              — SAPAL loop ở đây. OSS tools được gọi FROM apex/, không ngược.
6. api/               — sole cross-language bridge với TypeScript PolicyClient.
7. core/quota.py      — QuotaStore ABC, swappable backend (in-memory → Redis).
8. config/            — shipped defaults only. Runtime path = ACP_CONFIG_DIR env var.
```

---

## PART 4 — ARCHITECTURE

### 4.1 Module structure

```
src/ai_control_plane/
├── core/
│   ├── models.py          # SSOT: ProjectConfig, AgentConfig, ModelProfile, PolicyRule,
│   │                      #   Task, TaskStatus, TelemetryEvent, PolicyDecision,
│   │                      #   AgentIdentity, McpError, ApprovalRequest, ApprovalDecision,
│   │                      #   RegisteredAction, RbacConfig, Guardrail, KillSwitch
│   ├── policies.py        # PolicyEngine, ConditionEvaluator, ApprovalGate,
│   │                      #   GuardrailEvaluator — PURE functions, no I/O
│   ├── registry.py        # ProjectRegistry, AgentRegistry
│   ├── quota.py           # QuotaTracker, TokenBudget, RateLimiter, QuotaStore ABC
│   ├── telemetry.py       # TelemetryWriter, InMemoryTelemetryStore, FileTelemetryStore
│   │                      #   hash-chain: SHA-256(prev_hash + canonical_json(event))
│   ├── identity.py        # JWTValidator (HS256 stub; RS256 via ACP_JWKS_URL)
│   ├── tool_names.py      # MCP_TOOL_TO_POLICY_ACTION, normalize_tool_name(),
│   │                      #   resolve_policy_tool_name() — Option A adapter permanent
│   ├── governance_catalog.py  # SSOT for /governance/status — v1.3.3
│   └── exceptions.py      # ControlPlaneError, ConfigError, PolicyError,
│                          #   QuotaError, AgentError, ApprovalError
├── config/
│   └── loader.py          # load_policies(), load_agents(), load_projects(),
│                          #   load_guardrails(), load_kill_switch(),
│                          #   load_project_token_limits(), build_agent_registry()
├── api/
│   ├── server.py          # FastAPI app — 13 endpoints, create_app(), AppState
│   └── schemas.py         # Pydantic v2 request/response schemas
├── mcp/
│   ├── git_server.py      # GitMcpServer facade → cyanheads TS server
│   ├── server_factory.py  # make_project_server() per ProjectConfig
│   └── server_utils.py    # McpErrorBuilder, ToolSchemaValidator, redact_sensitive_data()
├── cli/
│   ├── main.py            # Typer app — routes subcommands
│   ├── assign.py, status.py, logs.py, approve.py, quota.py, apex.py
│   └── _http.py           # HTTP helper (Invariant #4: CLI → HTTP only)
└── apex/
    ├── loop.py            # SapalLoop — SAPAL orchestrator (Sense→Analyze→Predict→Act→Learn)
    ├── sense.py, analyze.py, predict.py, act.py, learn.py
    └── __init__.py        # imports SapalLoop
```

### 4.2 API surface (13 endpoints)

```
POST /policy/evaluate     → PolicyEvalResponse (200 + allowed bool, NOT 503 on deny)
POST /policy/approve      → ApprovalDecision
POST /identity/verify     → AgentIdentity (401 on auth fail, NOT 200+deny)
GET  /health              → HealthResponse (config_loaded, policy_rules_count, agents_loaded)
POST /tasks               → TaskStatus
GET  /status/{project_id} → TaskStatus
GET  /quota/{project_id}  → QuotaStatus
GET  /quota/agent/{id}    → QuotaStatus (by_agent)
GET  /quota/profile/{id}  → QuotaStatus (by_model_profile)
GET  /telemetry/events    → list[TelemetryEvent]
GET  /governance/status   → full governance JSON (catalog v1.3.3)
POST /apex/trigger        → TriggerResponse (SAPAL loop iteration)
GET  /apex/status         → SapalStatus (last run, anomalies, proposals)
```

HTTP contracts:
- Policy path: deny → HTTP 200 + allowed=false (NOT 503)
- Identity path: auth fail → HTTP 401 (NOT 200+deny)
- kill_switch active → HTTP 200 + allowed=false + reason="kill_switch_active:..."
- Service error → HTTP 503 (both paths)
- GET /health → HTTP 200 always (exempt from kill_switch)

### 4.3 Config runtime wiring (api/server.py startup)

| YAML source      | Loader function                 | AppState field             |
|------------------|---------------------------------|----------------------------|
| policies.yml     | load_policies()                 | policy_engine              |
| policies.yml     | load_guardrails()               | policy_engine (combined)   |
| policies.yml     | load_kill_switch()              | policy_engine.kill_switch  |
| agents.yml       | build_agent_registry()          | agent_registry             |
| projects.yml     | load_projects()                 | projects_loaded            |
| policies.yml     | load_project_token_limits()     | project_limits, token_budget|

### 4.4 Runtime stores

| Store                  | Location                  | Persistence                           |
|------------------------|---------------------------|---------------------------------------|
| TaskStore              | AppState.task_store       | FileTaskStore (ACP_DATA_DIR) or memory|
| QuotaStore             | AppState.quota_store      | Redis (ACP_REDIS_URL) or memory       |
| InMemoryTelemetryStore | AppState.telemetry_store  | Lost on restart (MC-9: FileTelemetryStore)|
| ActionRegistry         | AppState.action_registry  | Redis (ACP_REDIS_URL) or memory       |

### 4.5 Tool naming convention (Option A — permanent)

| Layer              | Format      | Example        | Defined in          |
|--------------------|-------------|----------------|---------------------|
| Shipped config/    | dot notation| git.read       | Human operators      |
| PolicyEngine/API   | snake_case  | git_read       | core/tool_names.py  |
| MCP tool catalog   | snake_case  | git_status     | core/tool_names.py  |
| allowed_tasks      | hyphen      | infra-plan     | Task classifier      |

resolve_policy_tool_name() handles: dot→snake AND mcp_tool→policy_action.
Decision P0-2b: Option A (adapter permanent, not migration). #8 CLOSED.

### 4.6 Deployment profiles

| Profile | Config         | rules | Host              | Evidence  |
|---------|----------------|-------|-------------------|-----------|
| A       | fixture        | 8     | MSI WSL, CI       | Studies 01-07 |
| B       | shipped config | 10    | ubuntu-vps        | Study 08  |
| CLEAN   | shipped        | 10    | separate machine  | PB-7 pending |

---

## PART 5 — MILESTONE HISTORY

### Milestone A — CLOSED 2026-06-23 (#38)
PoC scaffold: core/ + api/ + mcp/ + cli/assign+status + apex/ stubs
Phase 1 v2 remediation: ingress normalize, MCP map, parity CI, MCP integration tests

### Milestone B — CLOSED 2026-06-24 (PR #51)
Sprint 1 (MB-S1-1..5): Guardrails+kill_switch, ABAC full, coverage 82%, CLI tests, JWT stub
Sprint 2 (MB-S2-1..11): Redis, CLI live (approve/quota/logs), MCP HTTP transport,
  JWKS RS256, FileTaskStore, ActionRegistry, quotas by_agent/by_model_profile,
  branch protection workflow doc

### Milestone C — CODE CLOSED 2026-06-24 (PR #63 @ 6dfffdf), governance partial
MC-1..6: SAPAL loop live (heuristic MVP — not full OSS orchestration)
MC-7: apex/ API (/apex/trigger, /apex/status) + cli/apex.py
MC-8: MCP HTTP — StubGitForwarder + HttpGitForwarder (DEBT: real cyanheads E2E not in CI)
MC-9: FileTelemetryStore + ACP_TELEMETRY_DIR
MC-10: scripts/run_otel_collector.sh stub (DEBT: otel-collector.yaml absent)
MC-11: 165 tests

Scope reductions (conscious, not failures):
- MC-4: ActAdapter skip PolicyEngine on risk_level=high (circular dep avoided)
- MC-8: stub forwarder (Milestone C+ debt)
- MC-10: OTel script stub only (Milestone C+ debt)
- learn.py: proposals=[] always (human-in-loop shell, no ML engine yet)

### Milestone C+ (not started — next after PB)
- cyanheads MCP E2E in CI (MC-8)
- otel-collector.yaml + OTLP doc (MC-10)
- apex/act.py full PolicyEngine gate
- SAPAL external signal ingestion (sense.py beyond telemetry aggregate)
- SAPAL ML/rules engine for learn.py

---

## PART 6 — GOVERNANCE FRAMEWORK (6-layer Karpathy)

### 6.1 Layer structure (.cursorrules — 6 sections, priority order)

L0 — Behavioral Constitution (Karpathy 4 principles):
  - CLAUDE.md (root) — think before coding, simplicity, surgical, goal-driven
  - "State assumptions before coding" mandatory
  - "Senior engineer test" for complexity

L1 — Project Context:
  - ARCHITECTURE.md (primary SSOT)
  - Module ownership table
  - Coding conventions (structlog, Pydantic v2, async/await)

L2 — Risk Policy (docs/CURSOR_RISK_POLICY.md):
  - LOW (docs/tests, ≤50 LOC) → proceed
  - MEDIUM (CLI/config, ≤200 LOC) → state plan first
  - HIGH (core/ changes, ≤300 LOC) → Claude review before coding
  - CRITICAL (invariants/auth/ABAC) → human explicit approve
  - 10 forbidden operations (F1..F10)
  - Mandatory PR body template

L3 — Execution Guardrails:
  - Branch isolation: 1 task = 1 branch = 1 PR
  - File allowlist per task type
  - Diff size limits enforced

L4 — Evaluation:
  - ruff check src/ tests/
  - mypy src/ai_control_plane/ --strict
  - pytest tests/ -v (165 tests, fail_under=70)
  - pytest -m smoke -v (8/8 SMK)
  - pytest -m shipped_config (parity)

L5 — Governance & Memory:
  - docs/governance/LESSONS_LEARNED.md — P-01..P-13 failure patterns
  - docs/governance/*.html — Claude decision archive
  - Sprint reports, audit docs, reconciliation docs
  - Sprint close: update LESSONS_LEARNED mandatory

### 6.2 LESSONS_LEARNED patterns (P-01..P-13)

P-01: Monolithic PR risk — PRs #48, #63 (max 300 LOC HIGH tasks)
P-02: Scope creep in doc-only PRs — agent4 in PR #46 (file allowlist)
P-03: GitHub auto-close failure on issue ranges (list individually, not ranges)
P-04: Silent ABAC assumption — role_not_in skipped (state assumptions before coding)
P-05: Step 7 timing — archive before merge (close commit = post-merge SHA)
P-06: Scope reduction without documentation (PR body template)
P-07: Doc drift accumulation between sprints (mandatory doc sync at sprint close)
P-08: Kill switch HTTP contract — 200+deny not 503 (counter-intuitive)
P-09..P-13: [Additional patterns added post-audit]

### 6.3 Governance catalog (v1.3.3 — SSOT)

File: src/ai_control_plane/core/governance_catalog.py
Endpoint: GET /governance/status
Fields: milestones, layers (L0-L5), verify_gate, case_studies (CS-01..CS-06),
        known_gaps (G-01..G-07, 1 OPEN=G-05), practice_evidence,
        public_beta (gates_closed: 4, gates_remaining: 7), doc_links

---

## PART 7 — POLICY ENGINE DETAILS

### 7.1 ABAC condition keys

| Condition      | Loaded | Enforced | Status         |
|----------------|--------|----------|----------------|
| environment    | ✅     | ✅       | —              |
| action/actions | ✅     | ✅       | —              |
| role           | ✅     | ✅       | —              |
| data_class/PII | ✅     | ✅       | —              |
| role_not_in    | ✅     | ✅       | GAP-ABAC-2 CLOSED |
| approval_status| ✅     | ✅       | GAP-ABAC-1 CLOSED |
| read_only      | ✅     | ✅       | GAP-ABAC-1 CLOSED |

### 7.2 Telemetry hash-chain

event_hash = SHA-256(previous_hash + canonical_json(event,
             exclude=[event_hash, previous_hash, id]))
TelemetryWriter.emit() is ONLY way to append — no direct _events.append()
Failure = fail-silent (structlog.warning), never alter PolicyDecision
AppState.telemetry_store = shared in-process store

---

## PART 8 — CI PIPELINE (current)

```
governance-memory (L5)
        │
        ▼
     smoke (pytest -m smoke, 8 tests)
        ├────────────────────┐
        ▼                    ▼
   test (full suite,    examples-minimal-smoke
   165 pytest,          (docker compose up --build,
   fail_under=70)       verify scripts, timeout 5m)
```

CI files: .github/workflows/ci.yml
Examples path: examples/minimal/docker-compose.yml (NOT examples/docker-compose.yml)
Job name: examples-minimal-smoke (NOT examples-smoke)

---

## PART 9 — PRACTICE EVIDENCE (Studies 01-08)

| Study | Profile | Network        | Verdict | Key evidence                         |
|-------|---------|----------------|---------|--------------------------------------|
| 01    | A       | localhost      | PASS    | Fixture config, rules=8, smoke       |
| 02    | B       | localhost      | PASS    | Shipped config, rules=10             |
| 03    | C       | Docker         | PASS    | Profile C soak slice                 |
| 04    | ops edge| localhost      | PASS    | ACP_CONFIG_DIR startup-only (04c)    |
| 05    | advanced| localhost      | PASS†   | Kill switch P-13, 5g SKIPPED→05g-r   |
| 06    | A       | LAN bidirect.  | PASS    | WSL portproxy, Mac↔Laptop            |
| 07    | A       | Tailscale VPS  | PASS    | ubuntu-vps, TS IP overlay proven     |
| 08    | B       | VPS remote     | PASS    | Shipped config on ubuntu-vps (NEW-G-06 CLOSED) |

3 hosts: MSI WSL, Mac Mini M2, ubuntu-vps
4 network topologies: localhost, Docker, LAN, Tailscale overlay
28 machine-readable JSON artifacts
G-01..G-07: all CLOSED except G-05 (PB-9 calendar soak ongoing)

---

## PART 10 — PUBLIC BETA STATUS (as of 2026-06-27)

### 10.1 Gates from governance_catalog.py v1.3.3

CLOSED (4):
- PB-11: Legal artifacts (LICENSE, SECURITY.md, CONTRIBUTING.md, CODE_OF_CONDUCT.md)
- RUNBOOK.md: deploy, rollback, config reload, incident response, Windows/WSL
- Governance catalog: 3-stream convergence live
- GitHub Discussions: enabled

REMAINING (7):
- G-05/PB-9: Staging soak ≥14d (ticks 06-26/27; review ~2026-07-06)
  ⚠️ GAP: 06-22→06-25 no evidence — operator must clarify (gap or /tmp log?)
- PB-7: CLEAN machine fork ≤15 min (MSI WARM ≠ PASS — needs clean VM/Codespace)
- PB-8: CHANGELOG + v0.1.0-rc.1 tag (human approve after PB-9)
- PB-10: Production soak ≥30d (DEFER to GA per recommendation — 0.x beta only)
- PB-6: OpenAPI static publish (runtime ✅; commit docs/openapi.json on flip day)
- security@: mailbox live test (send test email to security@dataxmind.com)
- PB-12: Human go/no-go (~2026-07-10 target)

### 10.2 Runtime verified (2026-06-27)

| Check                    | Result                    | Host           |
|--------------------------|---------------------------|----------------|
| Smoke pytest             | 8/8 PASS                  | MSI WSL        |
| Governance runtime       | v1.3.3 · 13 patterns      | MSI + VPS      |
| OpenAPI runtime          | 3.1.0 · 13 paths          | MSI            |
| PB-9 soak iteration      | PASS @ 11:53Z             | MSI Docker     |
| CI full suite            | PASS (165 tests)          | GitHub Actions |
| CI examples-minimal-smoke| PASS ~41s                 | GitHub Actions |

### 10.3 Target timeline

| Date         | Event                                        | Owner    |
|--------------|----------------------------------------------|----------|
| 2026-06-22   | PB-9 soak started (Day 1)                    | Operator |
| 2026-06-27   | PB-9 ticks 06-26/27 · PR #118 merged        | Done     |
| 2026-06-30..07-05 | PB-7 CLEAN fork attempt               | Operator |
| ~2026-07-06  | PB-9 Day 14 review                           | Operator |
| ~2026-07-07  | PB-8: CHANGELOG + v0.1.0-rc.1 tag + static OpenAPI | Human |
| ~2026-07-08  | security@ mailbox test                       | Human    |
| ~2026-07-10  | PB-12 go/no-go → public flip                 | Human    |

### 10.4 Pre-flip checklist (operator, ~30 min)

```bash
# 1. Export static OpenAPI
uvicorn ai_control_plane.api.server:app --port 8000 &
curl http://localhost:8000/openapi.json > docs/openapi.json
git add docs/openapi.json && git commit -m "docs: export OpenAPI 3.1 for v0.1.0-rc.1"

# 2. Tag rc
git tag v0.1.0-rc.1 && git push origin v0.1.0-rc.1

# 3. Test security@ mailbox
# Send email → confirm receipt

# 4. Final smoke
pytest tests/test_smoke.py -v -m smoke   # 8/8
bash scripts/verify_governance_status_runtime.sh  # v1.3.3

# 5. GitHub: Settings → Public, Security Advisories, Dependabot
# 6. Create Release v0.1.0-beta.1 from tag
```

---

## PART 11 — DRIFT CATALOG (REJECT THESE CLAIMS)

| STALE CLAIM                          | CORRECT SSOT                              |
|--------------------------------------|-------------------------------------------|
| examples/docker-compose.yml          | examples/minimal/docker-compose.yml       |
| examples-smoke (CI job name)         | examples-minimal-smoke                    |
| /openapi.json in paths{} assertion   | Bug fixed @ 1d883ec; URL not operation    |
| "PB-9 only remaining gate"           | 7 gates_remaining (catalog v1.3.3)        |
| "8/12 PB gates done"                 | 4 closed / 7 remaining (catalog taxonomy) |
| MSI WARM = PB-7 PASS                 | CLEAN machine required                    |
| "HOÀN TẤT / nothing to deliver"      | True for Cursor packets only; PB open     |
| 156 tests                            | 165 pytest @ master                       |
| PB-10 blocks PB-12                   | PB-10 deferred to GA (recommendation)    |
| HTML artifact % readiness            | Use gates_remaining count, not HTML %     |

---

## PART 12 — SSOT FILES (priority order for Claude)

```
src/ai_control_plane/core/governance_catalog.py        # Catalog SSOT v1.3.3
GET /governance/status                                  # Runtime mirror
scripts/verify_governance_status_runtime.sh            # Expects v1.3.3, 13 patterns
scripts/verify_openapi_runtime.sh                      # ≥10 paths
ARCHITECTURE.md                                        # Module SSOT
docs/CURSOR_RISK_POLICY.md                             # L2 risk policy
docs/governance/LESSONS_LEARNED.md                     # P-01..P-13
docs/governance/PROJECT_STATUS_AUDIT_FOR_CLAUDE.md     # This handoff source
docs/governance/TASK_AUDIT_REMAINING_2026-06-27.md     # Open vs closed tasks
docs/governance/CLAUDE_RESPONSIBILITY_MATRIX_RECONCILIATION.md
docs/prompts/SESSION_ANCHOR_TEMPLATE.md                # L5 session pin
```

---

## PART 13 — CLAUDE ROLE FROM HERE

### DO:
1. Read this document + TASK_AUDIT_REMAINING at session start
2. Audit any prompt against Part 11 Drift catalog before suggesting code
3. Prepare Day 14 PB-9 review (~2026-07-06): soak log analysis, SEV criteria
4. Draft PB-12 go/no-go narrative — human decides
5. Support PB-7 CLEAN fork Q&A
6. Answer PB-9 gap 06-22→25 scenarios (3 questions for operator)
7. Confirm PB-10 scope decision (block PB-12 or defer to GA?)

### DO NOT:
1. Re-open merged Cursor packets (catalog sync, legal, OpenAPI CI, examples)
2. Create duplicate compose files or CI jobs
3. Close gates_remaining in catalog without human approval + evidence
4. Accelerate PB-9 calendar soak
5. Treat "HOÀN TẤT" stamps in HTML artifacts as Public Beta completion
6. Generate new Cursor code without explicit request + risk classification

### Operator procedures (Claude must NOT auto-execute):
- PB-9 daily tick: update PB9_STAGING_SOAK_LOG.md when operator says "đã tick YYYY-MM-DD"
- PB-9 soak loop: bash scripts/restart_soak_loop.sh
- PB-7: CLEAN machine only → pb-7-clean-machine-fork/RUNBOOK.md
- security@: human sends test email
- PB-8 tag: human approve post PB-9
- PB-12 flip: human go/no-go → PUBLIC_BETA_GO_NO_GO.md

---

## PART 14 — KEY DECISIONS RECORD

| Decision        | Choice          | Rationale                                    |
|-----------------|-----------------|----------------------------------------------|
| P0-2b tool name | Option A        | Adapter permanent; dot notation in config/    |
| Sprint 1 PR     | Path B (mono)   | Cost >> benefit of 7 separate PRs             |
| MC scope        | MVP heuristic   | SAPAL live without OSS orchestration          |
| act.py gate     | skip on HIGH    | Avoids circular dep with PolicyEngine         |
| PB-10           | Defer to GA     | 0.x beta does not require 30d prod soak      |
| JWKS delivery   | Milestone B     | Pulled forward from C (identity hardening)    |
| learn.py        | proposals=[]    | Human-in-loop correct; no ML engine yet       |
| InMemory naming | Keep as-is      | Cursor: EventStore → InMemoryTelemetryStore   |
| agent_registry  | Option A        | _resolve_role(AgentConfig) — Invariant #2     |

---

## PART 15 — ENVIRONMENT VARIABLES

| Variable             | Purpose                                  | Default            |
|----------------------|------------------------------------------|--------------------|
| ACP_CONFIG_DIR       | Runtime config path (startup-only!)      | shipped config/    |
| ACP_DATA_DIR         | FileTaskStore persistence path           | in-memory          |
| ACP_REDIS_URL        | Redis for quota/tasks                    | in-memory          |
| ACP_JWKS_URL         | RS256 JWKS endpoint                      | HS256 dev stub     |
| ACP_MCP_GIT_URL      | cyanheads git-mcp-server HTTP URL        | StubGitForwarder   |
| ACP_TELEMETRY_DIR    | FileTelemetryStore path                  | InMemory           |
| ACP_LOG_LEVEL        | structlog level                          | info               |
| ACP_DEV_MODE         | Console renderer (vs JSON)               | false              |
| ACP_API_BASE_URL     | Factory default policy client base URL   | localhost:8000     |
| ACP_MCP_HTTP_HOST    | MCP HTTP transport bind host             | 127.0.0.1          |
| ACP_MCP_HTTP_PORT    | MCP HTTP transport bind port             | 3001               |

⚠️ ACP_CONFIG_DIR: read at startup ONLY (Study 04c). Changing env on running server
has no effect — must restart API.

---

## PART 16 — PACE VERIFY COMMANDS

```bash
# Full verification sequence (operator)
export ACP_CONFIG_DIR=tests/fixtures/config

# L4 gates
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v                              # 165 pass, fail_under=70
pytest tests/test_smoke.py -v -m smoke        # 8/8
pytest tests/test_shipped_config_parity.py -v -m shipped_config

# L5 governance
uvicorn ai_control_plane.api.server:app --port 8000 &
curl -s http://localhost:8000/governance/status | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh   # expects v1.3.3, 13 patterns
bash scripts/verify_openapi_runtime.sh             # expects ≥10 paths, 3.1.0

# Examples CI equivalent
docker compose -f examples/minimal/docker-compose.yml up --build -d
sleep 8
curl -sf http://localhost:8000/health | python3 -c \
  "import sys,json; d=json.load(sys.stdin); assert d['status']=='ok'"
docker compose -f examples/minimal/docker-compose.yml down
```

---

## PART 17 — RECENT COMMIT HISTORY (context)

| Commit   | Summary                                                    |
|----------|------------------------------------------------------------|
| 527eb5d  | PB-9 PM tick + post-merge doc baseline sync (current)      |
| 81357d3  | PR #118 — RUNBOOK ops, reconciliations, PB-12 checklist    |
| 1d883ec  | Fix OpenAPI verify script (paths bug)                      |
| 375ef14  | Verdict stamp pb_openapi_and_examples_ci.html              |
| 6dfffdf  | PR #63 — MC-1..11 SAPAL + apex API + FileTelemetryStore    |
| 1dae3ea  | PR #48 — MB Sprint 1 (guardrails, ABAC, coverage, CLI, JWT)|
| 83e3ab5  | Phase 1 v2 baseline                                        |

---

## PART 18 — OPEN QUESTIONS FOR NEXT SESSION

1. **PB-9 gap 06-22→25**: soak script chạy continuous hay có outage?
   - YES → Day 14 = 07-06 (on track)
   - NO → Day 14 = 07-10 (adjust flip to ~07-12)

2. **PB-10 scope**: confirm PB-10 deferred to GA (v1.0.0), không block PB-12 (0.x beta)?

3. **PB-7 machine**: dùng VM mới, colleague machine, hay Docker-in-Docker?

4. **CHANGELOG**: draft v0.1.0-rc.1 sẵn — operator confirm dates trước khi tag.

5. **security@dataxmind.com**: mailbox đã live chưa? Send test email.

---

**Document end. Paste PART 1 + PART 11 + PART 13 as session context minimum.**
**Full document for complete context transfer to new conversation.**
