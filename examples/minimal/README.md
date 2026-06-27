# Minimal AI Control Plane stack

Run the API with fixture-equivalent config for local exploration (not production).

## Prerequisites

- Docker and Docker Compose
- Or: Python 3.11+ with `pip install -e ".[dev]"` from repo root

## Docker Compose

```bash
# From repo root
docker compose -f examples/minimal/docker-compose.yml up --build
```

API: http://localhost:8000  
Health: http://localhost:8000/health

Uses `tests/fixtures/config` mounted as `ACP_CONFIG_DIR`.

## Native (no Docker)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000
```

## Smoke check

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
curl -sf "$ACP_API_URL/governance/status" | python3 -m json.tool | head -25
bash scripts/verify_governance_status_runtime.sh
```

Expect `config_loaded: true`, `OK: governance/status runtime verify 1.3.3 13 patterns`.

See [README.md](../../README.md) for policy/quota examples.
