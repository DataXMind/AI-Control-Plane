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
curl -s http://localhost:8000/health | python3 -m json.tool
```

Expect `config_loaded: true`, non-empty `agents_loaded` and `model_profiles_loaded`.

See [README.md](../../README.md) for policy/quota examples.
