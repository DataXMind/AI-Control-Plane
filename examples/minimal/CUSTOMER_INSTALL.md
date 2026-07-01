# Customer Install — Host ACP Without Forking (Task 1)

**Document ID:** ACP-CUSTOMER-INSTALL-001  
**Audience:** Operators, platform teams, vendors deploying ACP for end-users  
**Integrators (Task 2):** [`docs/CLIENT_INTEGRATION.md`](../../docs/CLIENT_INTEGRATION.md) — they only need `ACP_API_URL`  
**Maintainer path (full repo):** [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md)

You **do not** need to fork or develop on the ACP codebase. You run a **packaged service** (Docker) + **YAML config** on the host.

---

## 0. End-user doc tiers

| Tier | Doc | Task |
|------|-----|------|
| **T0** | [`docs/QUICKSTART.md`](../../docs/QUICKSTART.md) | 5 min RUN or CONNECT |
| **T1** | **This file** | **Task 1** — install & operate ACP |
| **T2** | [`docs/CLIENT_INTEGRATION.md`](../../docs/CLIENT_INTEGRATION.md) | **Task 2** — app integration (zero-git) |
| **T3** | [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md) | Maintainer clone + PB-9 / evidence |

---

## 1. Choose install path

| Path | Git clone? | Stack | Rules | Use when |
|------|------------|-------|-------|----------|
| **A — Maintainer** | Yes (full repo) | compose build | 10 (Profile B) | You develop on ACP or need repo scripts |
| **B — Demo only** | Optional | GHCR `demo` | 8 (fixture) | POC / evaluator — **not** customer production |
| **C — Customer bundle** | **No** | GHCR + compose files | 10 (your YAML) | **Packaged deploy for clients** |

This document is the **complete runbook for Path C**. Path A: [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md). Path B: [`docs/QUICKSTART.md`](../../docs/QUICKSTART.md) § RUN.

---

## 2. Path C — Prerequisites

- [ ] **Docker Compose V2** (`docker compose version` prints v2.x)
- [ ] **Host:** Linux VPS, WSL2, or macOS with Docker Desktop
- [ ] **Port** `8000` free (or set `ACP_HOST_PORT` in env)
- [ ] **Strong Redis password:** `openssl rand -hex 32`
- [ ] **GHCR access** to pull image (login if package is private pre–PB-12):
  ```bash
  echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USER --password-stdin
  ```
  PAT scope: `read:packages`.

---

## 3. Path C — Step 1: Install directory (no git clone)

Create a fixed install root on the customer machine:

```bash
sudo mkdir -p /opt/acp
sudo chown "$USER:$USER" /opt/acp
cd /opt/acp
```

You need the following files in `/opt/acp` (vendor delivers as zip/tar or copies from a release bundle):

| File | Purpose |
|------|---------|
| `docker-compose.ghcr.yml` | Pull pre-built API image |
| `docker-compose.production.yml` | Redis + host config bind mount |
| `.env.production.example` | Template → copy to `.env.production` |
| `verify-pilot.sh` | Post-install smoke |
| `production-config/policies.yml` | Policy rules (from template) |
| `production-config/agents.yml` | Registered agents |
| `production-config/projects.yml` | Projects + quotas |

**How to obtain files without cloning the full repo:**

1. **Vendor bundle** — zip provided by DataXMind / your platform team (recommended for clients).
2. **Sparse copy from release** — download only `examples/minimal/` tree from a tagged release archive.
3. **One-time clone on a build machine** — copy `/opt/acp` directory to customer host via scp/rsync (customer server never needs git).

```bash
# Example: maintainer builds bundle on a machine WITH git (once)
git clone --depth 1 https://github.com/DataXMind/AI-Control-Plane.git /tmp/acp-build
mkdir -p /opt/acp/production-config
cp /tmp/acp-build/examples/minimal/{docker-compose.ghcr.yml,docker-compose.production.yml,.env.production.example,verify-pilot.sh} /opt/acp/
cp /tmp/acp-build/config/{policies,agents,projects}.yml /opt/acp/production-config/
chmod +x /opt/acp/verify-pilot.sh
# tar -czf acp-customer-bundle.tgz -C /opt acp  → ship to customer
```

---

## 4. Path C — Step 2: Environment file

```bash
cd /opt/acp
cp .env.production.example .env.production
chmod 600 .env.production
```

Edit `.env.production`:

```bash
# Required
ACP_HOST_CONFIG_DIR=/opt/acp/production-config
ACP_HOST_PORT=8000
REDIS_PASSWORD=PASTE_OUTPUT_OF_openssl_rand_hex_32

# Optional (when agents are network-exposed)
# ACP_JWKS_URL=https://your-idp.example.com/.well-known/jwks.json
```

**Verify:**

```bash
grep -q 'changeme' .env.production && echo 'FAIL: change REDIS_PASSWORD' || echo 'OK: password customized'
test -d production-config && ls production-config/*.yml
```

---

## 5. Path C — Step 3: Customize policy YAML

Edit `/opt/acp/production-config/` (never commit secrets to git):

| File | Customize |
|------|-----------|
| `agents.yml` | Each bot/worker/service → `agent_id`, roles |
| `projects.yml` | Each product/repo → `project_id`, quotas |
| `policies.yml` | ALLOW/DENY rules per tool + role |

**Verify syntax** (optional, if Python available on operator laptop):

```bash
python3 -c "import yaml; yaml.safe_load(open('production-config/agents.yml'))"
```

---

## 6. Path C — Step 4: Start stack

```bash
cd /opt/acp
docker compose -f docker-compose.ghcr.yml \
  -f docker-compose.production.yml \
  --env-file .env.production \
  up -d
```

Wait ~30s first start, then:

```bash
export ACP_COMPOSE_BASE=docker-compose.ghcr.yml
bash verify-pilot.sh
```

(`verify-pilot.sh` defaults to `docker-compose.yml` for maintainer build path.)

**Pass criteria from `verify-pilot.sh`:**

- `docker compose ps` — `acp-api` and `redis` **healthy** / **running**
- `GET /health` → `"status": "ok"`, `"config_loaded": true`
- Production stack: `"policy_rules_count": 10` (Profile B shipped template)

**Manual allow smoke** (replace IDs with yours):

```bash
export ACP_API_URL=http://127.0.0.1:8000

curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

Expect `"allowed": true` for a registered agent.

---

## 7. Path C — Step 5: Hand off to integrators (Task 2)

Give client-of-client teams **only**:

```bash
export ACP_API_URL=http://YOUR_HOST_OR_DNS:8000
```

Plus their registered `agent_id`, `project_id`, and `role`.

**Integration doc:** [`docs/CLIENT_INTEGRATION.md`](../../docs/CLIENT_INTEGRATION.md)

They **must not** receive: `.env.production`, `REDIS_PASSWORD`, or raw `production-config/` unless they are also operators.

---

## 8. Operate

Run from `/opt/acp`:

| Task | Command |
|------|---------|
| Logs | `docker compose -f docker-compose.ghcr.yml -f docker-compose.production.yml --env-file .env.production logs -f acp-api` |
| Config change | Edit `production-config/*.yml`, then `docker compose ... restart acp-api` |
| Stop | `docker compose -f docker-compose.ghcr.yml -f docker-compose.production.yml --env-file .env.production down` |
| Upgrade image | `docker compose ... pull && docker compose ... up -d` |

Config loads **at API startup** — restart required after YAML edits.

---

## 9. Security checklist (customer sign-off)

- [ ] `REDIS_PASSWORD` is not `changeme` / default example text
- [ ] `.env.production` mode `600`, not in git
- [ ] `production-config/` not world-readable (`chmod 750`)
- [ ] WAN: reverse proxy + TLS (not raw `:8000` on public IP)
- [ ] `ACP_JWKS_URL` set if untrusted networks reach API
- [ ] 0.x disclaimer communicated — see [`docs/QUICKSTART.md`](../../docs/QUICKSTART.md)

---

## 10. Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `cd examples/minimal` fails | Path C uses `/opt/acp`, not repo tree | Stay in `/opt/acp` |
| GHCR `denied` | Not logged in or no package access | `docker login ghcr.io` |
| `acp-api` Restarting | Redis extra missing in old image | Pull latest `demo` tag or use compose **build** path in [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md) |
| `policy_rules_count: 8` | Wrong compose (demo only) | Add `docker-compose.production.yml` + host YAML |
| Empty health JSON | API still starting | `bash verify-pilot.sh` (retries 15×) |
| Client `allowed: false` | Agent not in `agents.yml` | Edit YAML + restart API |

macOS Docker Compose issues: [`PRODUCTION_DEPLOY.md`](PRODUCTION_DEPLOY.md) § macOS.

---

## 11. Operator sign-off checklist

- [ ] Path C chosen; install dir created **without** requiring git on customer server
- [ ] All bundle files present (§ Step 1 table)
- [ ] `.env.production` customized; Redis password strong
- [ ] `verify-pilot.sh` exits 0
- [ ] Allow + deny evaluate smoke passes
- [ ] `ACP_API_URL` documented for integrators
- [ ] Security checklist (§9) complete

---

## 12. What this does NOT include

- PyPI install (`pip install ai-control-plane`) — post–GA track
- PB-9 maintainer soak evidence — internal only
- MCP git facade production guarantee — `[mcp-unverified]`
- 30-day production soak (PB-10 / GA)

---

**Last updated:** 2026-07-01 · Evidence: [`mac-pilot-deploy-2026-06-30`](../../docs/governance/practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md)
