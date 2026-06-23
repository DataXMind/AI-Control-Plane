# ai-control-plane

Control plane for multi-agent AI systems:
- Central config for projects, agents, policies (YAML + `ACP_CONFIG_DIR`)
- FastAPI HTTP bridge for TypeScript PolicyClient (fail-closed)
- MCP Git server facade for controlled repo access
- CLI `agentctl` for task assign/status

## Quick start (local dev)

```bash
# From repo root (WSL/Linux recommended)
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Optional: override shipped config/
export ACP_CONFIG_DIR=tests/fixtures/config

# Run API
uvicorn ai_control_plane.api.server:app --reload --port 8000

# Verify config wiring
curl -s http://localhost:8000/health | jq .

# CLI (requires API running)
export ACP_API_URL=http://localhost:8000
agentctl assign rust-gateway agent2 git_read --json
agentctl status rust-gateway --json
```

## Environment variables

| Variable | Purpose |
|----------|---------|
| `ACP_CONFIG_DIR` | Runtime path to `projects.yml`, `agents.yml`, `policies.yml` |
| `ACP_API_URL` | Base URL for CLI/MCP HTTP calls (default `http://127.0.0.1:8000`) |

## Documentation

- [ARCHITECTURE.md](ARCHITECTURE.md) — invariants, API contract, config wiring
- [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) — PACE, P0 gate, 9-step process
- [docs/OPEN_SOURCE_READINESS.md](docs/OPEN_SOURCE_READINESS.md) — public-beta gates

## Tests

```bash
pytest tests/ -v
ruff check src/ tests/
```

Current gate: **36 tests**, P0 import check passes.

## GitHub backlog

https://github.com/DataXMind/AI-Control-Plane/issues — Milestone A tracking: [#38](https://github.com/DataXMind/AI-Control-Plane/issues/38)
