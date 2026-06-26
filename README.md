# ai-control-plane

Control plane for multi-agent AI systems:
- Central config for projects, agents, policies (YAML + `ACP_CONFIG_DIR`)
- FastAPI HTTP bridge for TypeScript PolicyClient (fail-closed)
- MCP Git server facade for controlled repo access
- CLI `agentctl` for task assign/status/approve/quota/logs

## Quick start (local dev)

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

See [examples/minimal/README.md](examples/minimal/README.md).

**PB-7 clean-machine verify (≤15 min):** operator runbook — [docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md](docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md).

**Staging soak (PB-9):** after `docker compose up`, run `bash scripts/soak_staging.sh --loop 3600 --log /tmp/acp-soak-staging.log`. Tracker: [docs/governance/PB9_STAGING_SOAK_LOG.md](docs/governance/PB9_STAGING_SOAK_LOG.md).

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
- [CONTRIBUTING.md](CONTRIBUTING.md) · [SECURITY.md](SECURITY.md) · [LICENSE](LICENSE)
- [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) — public-beta gates

## Tests

```bash
pytest tests/ -v
ruff check src/ tests/
```

Current gate: **165 pytest**, smoke 8/8 + CI on `master`.

## Maintainer & security

- **Maintainer:** DataXMind ([GitHub org](https://github.com/DataXMind))
- **Security:** See [SECURITY.md](SECURITY.md) — use private report path before public beta flip

## Pre-release notice

This repository is **private** during staging soak (PB-9). Public beta (`0.x`) will ship with an explicit disclaimer that the HTTP API and config schema may change until `1.0.0`. See [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md).

## GitHub backlog

https://github.com/DataXMind/AI-Control-Plane/issues — Public Beta [#77–#80](docs/governance/PUBLIC_BETA_SPRINT_PLAN.md). PB-9 soak **in progress** since 2026-06-22.
