# Minimal AI Control Plane stack

Run the API with fixture-equivalent config for local exploration (not production).

**Index:** [examples/README.md](../README.md) · **PB-7:** [clean-machine RUNBOOK](../../docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md)

## Prerequisites

- Docker + Docker Compose v2 (recommended), or Python 3.11+
- ~5 minutes first build (image pull)

## Option A — Docker Compose (recommended)

```bash
# From repo root
docker compose -f examples/minimal/docker-compose.yml up --build

# Or from this directory
cd examples/minimal
docker compose up --build
```

API: http://localhost:8000

Uses `tests/fixtures/config` (8 policy rules) and persistent `ACP_DATA_DIR` volume.

## Option B — Native Python (repo root)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000
```

PyPI install (`pip install ai-control-plane`) is **not** available pre–public beta.

## First checks (PACE)

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
curl -sf "$ACP_API_URL/governance/status" | python3 -m json.tool | head -30
bash scripts/verify_governance_status_runtime.sh
```

Expected: `config_loaded: true`, `OK: governance/status runtime verify 1.5.0 17 patterns` (fixture stack: `policy_rules_count: 8`).

## Assign your first task (CLI)

```bash
export ACP_API_URL=http://localhost:8000
agentctl assign rust-gateway agent2 git_read --json
agentctl status --project rust-gateway
```

## Shipped vs configurable

| Item | Default (this example) | Production override |
|------|------------------------|---------------------|
| Config | `tests/fixtures/config` (8 rules) | `ACP_CONFIG_DIR` |
| Task storage | Docker volume `/data/acp` | `ACP_DATA_DIR` |
| Quota / registry | in-memory | `ACP_REDIS_URL` |
| Auth | HS256 dev stub | `ACP_JWKS_URL` |
| MCP Git | disabled | `ACP_MCP_GIT_URL` |

**Production pilot (Redis + host config, Profile B / 10 rules):** [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md) · `docker-compose.production.yml` · PASS evidence [`mac-pilot-deploy-2026-06-30`](../../docs/governance/practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md)

See [ARCHITECTURE.md](../../ARCHITECTURE.md) for invariants and wiring.

## VPS 24/7 (PB-9)

[systemd/README.md](systemd/README.md) — `acp-staging.service` + hourly soak.

## Optional env file

```bash
cp .env.example .env   # edit overrides for native runs
```

## Verify (from repo root)

```bash
docker compose -f examples/minimal/docker-compose.yml up --build -d
sleep 5
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
docker compose -f examples/minimal/docker-compose.yml down
```
