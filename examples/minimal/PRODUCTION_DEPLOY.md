# Production-style deploy (pilot / internal)

**Document ID:** ACP-EXAMPLES-PROD-DEPLOY-001  
**Status:** Operator-ready draft — **0.x beta** (not GA; see README disclaimer)  
**Baseline:** `master` @ catalog v1.5.0  
**Related:** [`README.md`](README.md) · [`docs/RUNBOOK.md`](../../docs/RUNBOOK.md) · ADR-002 (OIDC PROPOSED)

---

## When to use this stack

| Scenario | Compose files |
|----------|---------------|
| **PB-9 staging soak** (fixture, evidence) | `docker-compose.yml` only |
| **Pilot / internal production** (your YAML + Redis) | `docker-compose.yml` + `docker-compose.production.yml` |
| **GHCR pull + production** | `docker-compose.ghcr.yml` + `docker-compose.production.yml` |

This is **Tier A pilot** from the go-live assessment — not Public Beta (PB-12) or GA (PB-10).

---

## Prerequisites

- Linux VPS or WSL2 with Docker Compose v2
- DNS or Tailscale if remote agents connect ([`RUNBOOK.md`](../../docs/RUNBOOK.md))
- Strong `REDIS_PASSWORD` (generate: `openssl rand -hex 32`)

---

## Step 1 — Config on host

```bash
cd examples/minimal
cp .env.production.example .env.production
# Edit REDIS_PASSWORD, optional ACP_JWKS_URL

mkdir -p production-config
cp ../../config/{policies,agents,projects}.yml production-config/
# Edit production-config/*.yml — agents, roles, quotas
```

On VPS, prefer absolute path:

```bash
export ACP_HOST_CONFIG_DIR=/opt/acp/config
# in .env.production
```

---

## Step 2 — Start stack

**From `examples/minimal/`:**

```bash
docker compose -f docker-compose.yml \
  -f docker-compose.production.yml \
  --env-file .env.production \
  up -d --build
```

**GHCR (no build):**

```bash
docker login ghcr.io   # private repo until PB-12
docker compose -f docker-compose.ghcr.yml \
  -f docker-compose.production.yml \
  --env-file .env.production \
  up -d
```

---

## Step 3 — Verify

```bash
export ACP_API_URL=http://127.0.0.1:8000   # or VPS / Tailscale IP

curl -sf "$ACP_API_URL/health" | python3 -m json.tool
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"YOUR_AGENT","project_id":"YOUR_PROJECT","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

docker compose -f docker-compose.yml -f docker-compose.production.yml ps
docker inspect minimal-acp-api-1 --format 'RestartCount={{.RestartCount}} StartedAt={{.State.StartedAt}}'
```

---

## Step 4 — Integrate agents

Use [`examples/integrate/python/before_tool_call.py`](../integrate/python/before_tool_call.py):

```bash
export ACP_API_URL=http://YOUR_HOST:8000
python examples/integrate/python/before_tool_call.py
```

Every tool call should hit `POST /policy/evaluate` before execution.

---

## Step 5 — Operate

| Task | Command |
|------|---------|
| Logs | `docker compose -f docker-compose.yml -f docker-compose.production.yml logs -f acp-api` |
| Config reload | Edit host `production-config/`, then `docker compose ... restart acp-api` |
| Rollback image | `docker compose ... pull` previous tag or `git checkout` + `--build` |
| Backup data | Volume `acp-data` + Redis volume `redis-data` |
| Stop | `docker compose -f docker-compose.yml -f docker-compose.production.yml down` |

**Soak evidence (if this host is PB-9 MSI):** continue `bash scripts/restart_soak_loop.sh` against the running API — do not mix PB-9 fixture stack and production stack on the same port without documenting the switch.

---

## Security checklist (pilot)

- [ ] `REDIS_PASSWORD` not `changeme`
- [ ] `production-config/` not world-readable (`chmod 750`)
- [ ] `.env.production` mode `600`, not in git
- [ ] `ACP_JWKS_URL` set if agents are network-exposed (THREAT S-1)
- [ ] Reverse proxy + TLS for WAN (not raw `:8000` on public IP)
- [ ] 0.x disclaimer communicated to integrators

---

## What this does NOT provide

- Fleet load SLO (see `K6_FLEET_TEST_PLAN.md` — post-flip)
- MCP CI guarantee (`[mcp-unverified]`)
- 30-day production soak (PB-10 — GA track)
- Automatic OIDC enforcement (ADR-002 PROPOSED)

---

**Last updated:** 2026-06-30 · Operator draft for PB-12 prep
