# Production config directory (host bind mount)

This folder is mounted read-only into the container at `/etc/acp/config`.

**Do not commit secrets or production-specific agent credentials to git.**

## Bootstrap (first time)

From repo root:

```bash
mkdir -p examples/minimal/production-config
cp config/policies.yml config/agents.yml config/projects.yml \
   examples/minimal/production-config/
```

Edit `agents.yml`, `policies.yml`, and `projects.yml` for your agents and projects.

## Verify YAML loads

```bash
cd examples/minimal
docker compose -f docker-compose.yml -f docker-compose.production.yml \
  --env-file .env.production up -d --build

export ACP_API_URL=http://127.0.0.1:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
```

Expected: `"config_loaded": true`, `policy_rules_count` matches your `policies.yml`.

## Fixture vs production

| | Staging / PB-9 soak | This folder |
|--|---------------------|-------------|
| Config | `tests/fixtures/config` (8 rules) | Your YAML |
| Quota | in-memory (base compose) | Redis (production override) |
| Use | CI parity, soak evidence | Pilot / internal production |

See [`../PRODUCTION_DEPLOY.md`](../PRODUCTION_DEPLOY.md).
