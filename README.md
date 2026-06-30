# ai-control-plane

Control plane for multi-agent AI systems:
- Central config for projects, agents, policies (YAML + `ACP_CONFIG_DIR`)
- FastAPI HTTP bridge for TypeScript PolicyClient (fail-closed)
- MCP Git server facade for controlled repo access
- CLI `agentctl` for task assign/status/approve/quota/logs

**Status:** Milestones A/B/C/C+ **CLOSED** · **181** pytest · smoke **8/8** · policy engine primary; SAPAL `apex/` experimental @ 0.x  
**Public Beta:** **IN PROGRESS** — PB-9 staging soak since 2026-06-22 · review target **~2026-07-06** · [`gates_remaining`](docs/governance/practice-evidence/governance-status-v13-verify/artifacts/TASK_AUDIT_REMAINING_2026-06-27.md) via `GET /governance/status` · **Claude handoff:** [`PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md`](docs/governance/PROJECT_STATUS_FULL_TECHNICAL_REPORT_2026-06-28.md)

## What ACP Is

AI Control Plane is an **AI Agent Policy Engine** — the enforcement layer between
your AI agents and the resources they act on.

- **Fail-closed by default**: unknown agents are denied, API-down is denied
- **Config-driven**: policy rules in version-controlled YAML, not hardcoded
- **Audit log**: every policy decision is logged with agent_id, action, and outcome
- **0.x beta**: API may change; not recommended for unmonitored production use

## What ACP Is NOT

- ❌ Not a content moderation layer (does not inspect LLM outputs)
- ❌ Not a prompt injection filter
- ❌ Not an agent orchestrator (use alongside LangGraph/CrewAI)
- ❌ Not an observability platform (use alongside LangSmith/W&B)

## Quick start (local dev)

**New here?** [`docs/QUICKSTART.md`](docs/QUICKSTART.md) — RUN (`bash scripts/acp-up.sh`) or CONNECT (`ACP_API_URL`) in 5 minutes.

```bash
# From repo root (WSL/Linux recommended)
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -e ".[dev]"

# Use fixture config (matches CI / smoke gate)
export ACP_CONFIG_DIR=tests/fixtures/config

# Run API
uvicorn ai_control_plane.api.server:app --reload --port 8000

# Verify config wiring
curl -s http://localhost:8000/health | python3 -m json.tool

# Governance UX (milestones, gates, lessons_patterns)
curl -s http://localhost:8000/governance/status | python3 -m json.tool | head -30
# Or: bash scripts/verify_governance_status_runtime.sh

# Policy allow path
curl -s -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

# Quota (project / agent / model profile)
curl -s http://localhost:8000/quota/rust-gateway | python3 -m json.tool
curl -s http://localhost:8000/quota/agent/agent2 | python3 -m json.tool
curl -s http://localhost:8000/quota/profile/claude-pro-backend | python3 -m json.tool

# CLI (requires API running)
export ACP_API_URL=http://localhost:8000
agentctl assign rust-gateway agent2 git_read --json
agentctl status rust-gateway --json
agentctl quota rust-gateway --json
```

## Governance check (after API is up)

Requires `ACP_CONFIG_DIR` (see quick start above) and a running API:

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/governance/status" | python3 -m json.tool | head -30
bash scripts/verify_governance_status_runtime.sh
# Expected: OK: governance/status runtime verify 1.5.0 17 patterns
agentctl gov status
```

Returns milestones, 6-layer map, `known_gaps`, `lessons_patterns`, `public_beta` gates, and case studies. See [GOVERNANCE_UX_RUNTIME.md](docs/governance/GOVERNANCE_UX_RUNTIME.md).

## API docs (auto-generated)

FastAPI serves OpenAPI 3.x from Pydantic schemas in `api/schemas.py` (docs are **enabled** — no `docs_url=None`).

```bash
export ACP_API_URL=http://localhost:8000
# Swagger UI: http://localhost:8000/docs
# ReDoc:      http://localhost:8000/redoc
curl -sf "$ACP_API_URL/openapi.json" | python3 -m json.tool | head -20
bash scripts/verify_openapi_runtime.sh
```

Static export (PB-6): `python scripts/export_openapi.py` → [`docs/openapi/openapi.json`](docs/openapi/openapi.json). See [docs/openapi/README.md](docs/openapi/README.md).

## Smoke gate (8 tests — SMK-01..06 + 06b + 06c)

Run before merge when touching `core/`, `api/server.py`, or `config/loader.py`:

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke          # < 2 min
# or
bash scripts/smoke_acp.sh                       # CI mode
bash scripts/smoke_acp.sh --live                # optional uvicorn + curl
```

| SMK | Check |
|-----|-------|
| SMK-01 | Core import (`registry`, `telemetry`) |
| SMK-02 | `GET /health` — `config_loaded`, `policy_rules_count > 0` |
| SMK-03 | Policy allow — backend `git_read` |
| SMK-04 | Fail-closed deny — unknown agent + non-empty `reason` |
| SMK-05 | `GET /quota/rust-gateway` — `tokens_remaining >= 100000` |
| SMK-06 | `POST /identity/verify` — valid HS256 JWT |
| SMK-06b | Invalid JWT → 401 |
| SMK-06c | Unknown agent → 401 |

## Minimal Docker example

```bash
docker compose -f examples/minimal/docker-compose.yml up --build
```

See [examples/README.md](examples/README.md) and [examples/minimal/README.md](examples/minimal/README.md).

**PB-7 clean-machine verify (≤15 min):** operator runbook — [docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md](docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md).

**Staging soak (PB-9):** after `docker compose up`, run `bash scripts/restart_soak_loop.sh` (hourly loop + `--repo-log docs/governance/PB9_SOAK_ITERATION_LOG.md`). Tracker: [docs/governance/PB9_STAGING_SOAK_LOG.md](docs/governance/PB9_STAGING_SOAK_LOG.md). VPS systemd: [examples/minimal/systemd/README.md](examples/minimal/systemd/README.md).

## Full verify gate

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
```

Optional: `pre-commit install` then `pre-commit run --all-files`

## Environment variables

| Variable | Purpose |
|----------|---------|
| `ACP_CONFIG_DIR` | Runtime path to `projects.yml`, `agents.yml`, `policies.yml` |
| `ACP_DATA_DIR` | Persist task status across API restarts (`tasks/*.json`) |
| `ACP_REDIS_URL` | Redis-backed quota store + action registry |
| `ACP_JWKS_URL` | RS256 JWT validation (else HS256 dev stub) |
| `ACP_MCP_GIT_URL` | HTTP forwarder to cyanheads git-mcp-server |
| `ACP_API_URL` | Base URL for CLI/MCP HTTP calls (default `http://127.0.0.1:8000`) |

Without `ACP_DATA_DIR`, task status and in-memory quota/telemetry are lost on API restart.

## Documentation

- [docs/QUICKSTART.md](docs/QUICKSTART.md) — **start here** for end-users (RUN / CONNECT, 5 min)
- [examples/integrate/](examples/integrate/README.md) — copy-paste integration patterns (Python)
- [docs/DEVELOPER_SCENARIOS.md](docs/DEVELOPER_SCENARIOS.md) — advanced fork/clone / operator scenarios
- [docs/governance/ECC_ACP_INTEGRATION_ANALYSIS.md](docs/governance/ECC_ACP_INTEGRATION_ANALYSIS.md) — ECC harness vs ACP policy (48H SSOT)
- [docs/governance/ECC_48H_RESULTS.md](docs/governance/ECC_48H_RESULTS.md) — 48H integration closeout
- [AGENTS.md](AGENTS.md) — **start here** for coding agents (ML5 memory, session anchor)
- [ARCHITECTURE.md](ARCHITECTURE.md) — invariants, API contract, config wiring
- [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) — PACE, P0 gate, smoke gate §5.5
- [docs/governance/L5_MATURITY_MODEL.md](docs/governance/L5_MATURITY_MODEL.md) — ML0–ML5 memory maturity (target ML5)
- [docs/governance/gold-patterns/GP-01-agent-session-memory.md](docs/governance/gold-patterns/GP-01-agent-session-memory.md) — public gold pattern
- [docs/prompts/SESSION_ANCHOR_TEMPLATE.md](docs/prompts/SESSION_ANCHOR_TEMPLATE.md) — open every agent session
- [docs/governance/CURSOR_RISK_POLICY.md](docs/governance/CURSOR_RISK_POLICY.md) — 6-layer L2 risk classification
- [.cursorrules](.cursorrules) · [`.cursor/rules/`](.cursor/rules/) — L0–L5 Cursor governance (Karpathy)
- [docs/governance/GOVERNANCE_UX_RUNTIME.md](docs/governance/GOVERNANCE_UX_RUNTIME.md) — governance UX runtime + case studies (`GET /governance/status`, `agentctl gov status`)
- [docs/RUNBOOK.md](docs/RUNBOOK.md) — operator runbook (Windows/WSL LAN, Docker, Tailscale)
- [docs/governance/GOV_6LAYER_AUDIT_PASS.md](docs/governance/GOV_6LAYER_AUDIT_PASS.md) — 6-layer governance audit record
- [docs/governance/MILESTONE_B_BACKLOG.md](docs/governance/MILESTONE_B_BACKLOG.md) — Milestone B status (CLOSED)
- [docs/governance/MILESTONE_C_SPRINT_PLAN.md](docs/governance/MILESTONE_C_SPRINT_PLAN.md) — Milestone C status (CLOSED)
- [docs/governance/PUBLIC_BETA_SPRINT_PLAN.md](docs/governance/PUBLIC_BETA_SPRINT_PLAN.md) — Public Beta PB-1..12
- [Data Flow & Trust Boundaries](docs/governance/DATA_FLOW.md)
- [Rollback Protocol](docs/governance/ROLLBACK_PROTOCOL.md)
- [Business Model](docs/governance/BUSINESS_MODEL.md)
- [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [LICENSE](LICENSE)
- [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) — public-beta gates

## Tests

```bash
pytest tests/ -v
ruff check src/ tests/
```

Current gate: **181 pytest**, smoke 8/8 + CI on `master`.

## Security

- Threat model: [docs/governance/THREAT_MODEL.md](docs/governance/THREAT_MODEL.md)
- Report vulnerabilities: security@dataxmind.com (see [SECURITY.md](SECURITY.md))
- Known attack surfaces: [SECURITY.md §Known Attack Surfaces](SECURITY.md#known-attack-surfaces-0x-beta)

## Maintainer & security

- **Maintainer:** DataXMind ([GitHub org](https://github.com/DataXMind))
- **Security:** [SECURITY.md](SECURITY.md) — [Threat model](docs/governance/THREAT_MODEL.md) · `security@dataxmind.com` + [GitHub Security Advisories](https://github.com/DataXMind/AI-Control-Plane/security/advisories/new); 48h acknowledgment SLA (do not file public issues for vulnerabilities)
- **Questions:** [GitHub Discussions](https://github.com/DataXMind/AI-Control-Plane/discussions)

## Pre-release notice

This repository is **private** during staging soak (PB-9). Public beta (`0.x`) will ship with an explicit disclaimer that the HTTP API and config schema may change until `1.0.0`. See [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md).

## GitHub backlog

https://github.com/DataXMind/AI-Control-Plane/issues — Public Beta [#77–#80](docs/governance/PUBLIC_BETA_SPRINT_PLAN.md). PB-9 soak **in progress** since 2026-06-22.
