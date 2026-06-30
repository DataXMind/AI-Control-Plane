# Production-style deploy (pilot / internal)

**Document ID:** ACP-EXAMPLES-PROD-DEPLOY-001  
**Status:** Operator-ready — **PASS** Mac Mini @ 2026-06-30 ([evidence](../../docs/governance/practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md))  
**Baseline (pilot run):** `8a4e7fa` (#175 Dockerfile `[redis]`) · **Docs on master:** `4210ad2` (#176–#177)  
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

- **Docker Compose V2** (`docker compose`, not legacy `docker-compose` only) — see [macOS troubleshooting](#macos-docker-desktop) below
- Linux VPS, WSL2, or **macOS** (Docker Desktop / Colima with compose plugin)
- DNS or Tailscale if remote agents connect ([`RUNBOOK.md`](../../docs/RUNBOOK.md))
- Strong `REDIS_PASSWORD` (generate: `openssl rand -hex 32`)

### macOS (Docker Desktop)

**Symptom:** `docker: unknown command: docker compose` and `docker-compose: command not found`

**Cause:** Only the **Docker CLI** is installed (`brew install docker`) — **Compose plugin** and **daemon** are separate. Docker 29.x CLI alone does not include Compose.

**Fix A — Recommended: Docker Desktop (daemon + Compose V2)**

```bash
brew install --cask docker
open -a Docker          # wait until whale icon is steady
docker compose version  # must print v2.x
```

**Fix B — Homebrew Compose standalone**

```bash
brew install docker-compose   # provides docker-compose (hyphen)
docker-compose version

# Colima (daemon if you don't use Desktop):
brew install colima
colima start
```

**Fix C — No Compose at all (pilot script)**

From repo root, after config exists:

```bash
mkdir -p examples/minimal/production-config
cp config/{policies,agents,projects}.yml examples/minimal/production-config/
export REDIS_PASSWORD="$(openssl rand -hex 16)"
bash examples/minimal/run-pilot-without-compose.sh
```

Uses `docker build` + `docker run` only (see script header).

**Symptom:** `unknown shorthand flag: 'f' in -f` — same root cause; use Fix A/B/C above.

**Wrong directory:** Files live under `examples/minimal/`, not repo root.

```bash
cd /path/to/AI-Control-Plane/examples/minimal   # NOT cd /examples/minimal
cp .env.production.example .env.production
```

**Important:** `export ACP_CONFIG_DIR=/opt/acp/config` in the **host shell** does **not** change the container. For pilot, set `ACP_HOST_CONFIG_DIR` in `.env.production` or use `run-pilot-without-compose.sh` with `ACP_HOST_CONFIG_DIR=/opt/acp/config`.

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

**Option A — config beside repo (simplest on Mac):**

```bash
# .env.production:
# ACP_HOST_CONFIG_DIR=./production-config
```

**Option B — system path (VPS / Mac):**

```bash
sudo mkdir -p /opt/acp/config
sudo cp ../../config/{policies,agents,projects}.yml /opt/acp/config/
# Edit /opt/acp/config/*.yml
# .env.production:
ACP_HOST_CONFIG_DIR=/opt/acp/config
```

Do **not** rely on `export ACP_CONFIG_DIR=...` on the host unless running **native uvicorn** (no Docker).

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

# From examples/minimal — retry health + show logs if fail:
bash verify-pilot.sh

# Or manual (wait up to ~30s after first start):
curl -v http://127.0.0.1:8000/health
```

**`Expecting value: line 1 column 1` from `curl | python3 -m json.tool`:**  
`curl -sf` returned **empty body** — usually API still starting, container restarting, or port not bound. Run `bash verify-pilot.sh` or `docker compose … logs acp-api`.

**Repo scripts** (`verify_governance_status_runtime.sh`, `restart_soak_loop.sh`) live at **`scripts/`** (repo root), not under `examples/minimal`:

```bash
cd ../..   # repo root from examples/minimal
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh
```

PB-9 soak uses **fixture** stack (`docker-compose.yml` only) — pilot stack is separate; do not mix evidence unless documented.

**Operator-confirmed PASS (2026-06-30):** `minimal-acp-api-1` healthy · `minimal-redis-1` healthy · `verify-pilot.sh` OK · `verify_governance_status_runtime.sh` → v1.5.0 · 17 patterns. Full transcript: [`mac-pilot-deploy-2026-06-30/RESULTS.md`](../../docs/governance/practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md).

### Crash loop: `redis package required for RedisQuotaStore`

**Symptom:** `docker compose ps` shows `acp-api` **Restarting (1)**; logs end with:

```text
RuntimeError: redis package required for RedisQuotaStore (pip install ai-control-plane[redis])
```

**Cause:** Production override sets `ACP_REDIS_URL` but the image was built with `pip install -e .` only (no `redis` extra).

**Fix:** Rebuild after `examples/minimal/Dockerfile` includes `pip install -e ".[redis]"`:

```bash
cd examples/minimal
docker compose -f docker-compose.yml -f docker-compose.production.yml \
  --env-file .env.production up -d --build
```

```bash
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

**Last updated:** 2026-07-01 · docs reconcile @ `4210ad2`
