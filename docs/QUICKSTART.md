# ACP Quickstart — 5 Minutes, Two Doors

**Document ID:** ACP-QUICKSTART-001  
**Audience:** End-users, evaluators, app integrators (not contributors)  
**Advanced map:** [`DEVELOPER_SCENARIOS.md`](DEVELOPER_SCENARIOS.md) · **Contribute:** [`CONTRIBUTING.md`](../CONTRIBUTING.md)

### End-user doc tiers (Task 1 vs Task 2)

| Tier | Document | Who | Git / fork? |
|------|----------|-----|-------------|
| **T0** | **This file** | First 5 min RUN or CONNECT | Clone optional (RUN) · none (CONNECT) |
| **T1 — Task 1** | [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) | Operator hosts ACP for a team | **No** (vendor bundle @ `/opt/acp`) |
| **T2 — Task 2** | [`CLIENT_INTEGRATION.md`](CLIENT_INTEGRATION.md) | App dev / client-of-client | **No** — only `ACP_API_URL` |
| **T3** | [`examples/integrate/`](../examples/integrate/README.md) | Runnable Python samples | Optional |
| **Maintainer** | [`PRODUCTION_DEPLOY.md`](../examples/minimal/PRODUCTION_DEPLOY.md) | Full repo + evidence | Clone |

Answer **one question**:

> **Who runs the ACP API?**

| Door | You… | Start here |
|------|------|------------|
| **RUN** | Start ACP on your machine (Docker) | [§1 Run](#1-door-run-start-acp-locally) |
| **CONNECT** | Use an API someone else already runs | [§2 Connect](#2-door-connect-use-a-remote-acp) |

You do **not** need to pick config profiles, fork the repo, or read governance docs for either door.

---

## 1. Door RUN — Start ACP locally

**Time:** ~5 minutes (first Docker build may take longer)

### Prerequisites

- Docker + Docker Compose v2

### One command (recommended — from repo clone)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
bash scripts/acp-up.sh
```

`acp-up.sh` builds via docker compose, waits for `/health`, prints `ACP_API_URL`.

**No clone (GHCR):** after the demo image is published:

```bash
ACP_UP_MODE=ghcr bash scripts/acp-up.sh
```

If GHCR pull fails (`denied` / not found), the script **falls back to docker compose** when you are inside a repo clone. Use `--no-fallback` to disable.

#### Publish GHCR demo image (maintainer)

**Auto:** pushing changes to `governance_catalog.py` or `examples/minimal/Dockerfile` on `master` triggers [Publish GHCR demo image](https://github.com/DataXMind/AI-Control-Plane/actions/workflows/publish-ghcr.yml).

**Manual:** workflow_dispatch or tag `v0.1.*` / `docker-demo-*`.

1. Open Actions → **Publish GHCR demo image** → **Run workflow** (or `gh workflow run "Publish GHCR demo image"`)
2. Wait ~2–5 min for green check
3. **Verify local image:** `bash scripts/verify_ghcr_catalog.sh` (SKIP if image not pulled)
4. **Private repo:** log in before pull:
   ```bash
   echo YOUR_GITHUB_PAT | docker login ghcr.io -u YOUR_GITHUB_USER --password-stdin
   ```
   PAT needs scope `read:packages`.

CLI equivalent: `gh workflow run "Publish GHCR demo image"`

Image: `ghcr.io/dataxmind/ai-control-plane:demo`

**Catalog note:** GHCR `demo` republishes on `v0.1.*` / `docker-demo-*` tags — not on every governance MINOR. After catalog bump (e.g. v1.5.0), verify runtime with **compose build** or republish workflow before `verify_governance_status_runtime.sh` on GHCR.

### Manual compose (equivalent)

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build
```

Wait until healthy (~30s after first build):

```bash
curl -sf http://localhost:8000/health | python3 -m json.tool
```

**Expected:** `"status": "ok"`, `"config_loaded": true`, `"policy_rules_count": 8`

### Prove policy works (allow + deny)

```bash
# ALLOW — known agent
curl -sf -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool

# DENY — unknown agent (fail-closed)
curl -sf -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"unknown-agent","project_id":"rust-gateway","tool_name":"git_read"}' \
  | python3 -m json.tool
```

**Expected:** first → `"allowed": true` · second → `"allowed": false` with non-empty `"reason"`

### Optional: CLI on same machine

```bash
export ACP_API_URL=http://localhost:8000
pip install -e ".[dev]"   # once, from repo root
agentctl assign rust-gateway agent2 git_read --json
```

### What you are running

This uses **demo mode**: fixture config (8 policy rules) baked into the minimal Docker stack.  
For production-like shipped config (10 rules), see [`RUNBOOK.md`](RUNBOOK.md) — operator path, or [`examples/minimal/PRODUCTION_DEPLOY.md`](../examples/minimal/PRODUCTION_DEPLOY.md) for Docker pilot (Redis + host YAML bind mount).

**Pilot verify (from `examples/minimal/` after production stack up):**

```bash
bash verify-pilot.sh
cd ../.. && export ACP_API_URL=http://127.0.0.1:8000
bash scripts/verify_governance_status_runtime.sh   # expect 1.5.0 · 17 patterns
```

Evidence: [`mac-pilot-deploy-2026-06-30/RESULTS.md`](governance/practice-evidence/mac-pilot-deploy-2026-06-30/RESULTS.md).

### Stop

```bash
bash scripts/acp-up.sh --down
# or: docker compose -f examples/minimal/docker-compose.yml down
```

---

## 2. Door CONNECT — Use a remote ACP

**Time:** ~2 minutes

Someone else (your platform team) runs ACP. You only need the base URL.

### Step 1 — One environment variable

Copy [`.env.client.example`](../.env.client.example) — **replace the placeholder host, do not type angle brackets**:

```bash
# Same machine as ACP (after RUN door):
export ACP_API_URL=http://127.0.0.1:8000

# Another machine on your LAN (replace with real IP or hostname):
export ACP_API_URL=http://192.168.1.10:8000

# Corporate DNS example:
export ACP_API_URL=http://acp.internal:8000
```

**Wrong (bash error):** `export ACP_API_URL=http://<host-acp>:8000` — `<host-acp>` is doc placeholder only.

**Find your host IP (WSL API, client on same LAN):**

```bash
# On Windows (PowerShell): ipconfig → IPv4 of Wi-Fi/Ethernet
# On WSL host machine:
hostname -I | awk '{print $1}'
```

### Step 2 — Verify connectivity

```bash
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
```

If this fails → **do not call tools** (fail-closed). Fix network or ask the operator.

### Step 3 — Integrate into your app

Copy-paste examples from [`examples/integrate/`](../examples/integrate/README.md):

| File | When to use |
|------|-------------|
| [`before_tool_call.py`](../examples/integrate/python/before_tool_call.py) | Before every agent tool execution |
| [`startup_health_gate.py`](../examples/integrate/python/startup_health_gate.py) | Worker refuses to start if ACP is down |

**Minimal pattern (before a tool call):**

```python
import os, httpx

ACP = os.environ["ACP_API_URL"]

def acp_allow(agent_id: str, project_id: str, tool_name: str, role: str) -> None:
    r = httpx.post(
        f"{ACP}/policy/evaluate",
        json={
            "agent_id": agent_id,
            "project_id": project_id,
            "tool_name": tool_name,
            "role": role,
        },
        timeout=2.0,
    )
    r.raise_for_status()
    body = r.json()
    if not body["allowed"]:
        raise PermissionError(body["reason"])

acp_allow("agent2", "rust-gateway", "git_read", "backend")
# ... run your tool only after acp_allow succeeds ...
```

**Rules for clients:**

- Set **`ACP_API_URL` only** — do not set `ACP_CONFIG_DIR` on client machines
- `agent_id` must exist in the operator's `agents.yml`
- On timeout or HTTP error → treat as **deny**

### Run the example scripts

With ACP up (RUN door or remote):

```bash
export ACP_API_URL=http://localhost:8000
pip install httpx   # or pip install -e ".[dev]" from repo
python examples/integrate/python/startup_health_gate.py
python examples/integrate/python/before_tool_call.py
```

---

## 2.5 Performance (honest @ 0.x)

Load **smoke** (not production SLO): k6 @ **10 VUs**, **15s**, p95 **~9.33ms**, 0% failed — operator evidence only.

| Label | Meaning |
|-------|---------|
| **Load smoke** | Low-concurrency correctness check — [`k6-policy-smoke/RESULTS.md`](governance/practice-evidence/k6-policy-smoke/RESULTS.md) |
| **PB-9 soak** | Calendar stability @ ~1 req/hour — **not** a load benchmark |
| **Fleet SLO** | **Not verified** @ 0.x — see [`LOAD_CHARACTERISTICS.md`](governance/LOAD_CHARACTERISTICS.md) |

Reproduce (optional, requires k6): `bash scripts/run_k6_policy_smoke.sh`

---

## 3. What next?

| Goal | Go to |
|------|-------|
| Integrate app (Rust / Go / TS / Python, zero-git) | [`CLIENT_INTEGRATION.md`](CLIENT_INTEGRATION.md) |
| Host ACP for customers (no fork, vendor bundle) | [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) |
| Runnable Python samples | [`examples/integrate/README.md`](../examples/integrate/README.md) |
| OpenAPI / HTTP contract | http://localhost:8000/docs after RUN |
| Fork, PR, governance | [`CONTRIBUTING.md`](../CONTRIBUTING.md) |
| Staging, VPS, dual-host, profiles | [`DEVELOPER_SCENARIOS.md`](DEVELOPER_SCENARIOS.md) |
| Production operations (maintainer clone) | [`PRODUCTION_DEPLOY.md`](../examples/minimal/PRODUCTION_DEPLOY.md) · [`RUNBOOK.md`](RUNBOOK.md) |
| Governance OS for agent teams (**optional**) | [`prompts/AGENT_OPERATING_SYSTEM.md`](prompts/AGENT_OPERATING_SYSTEM.md) · [`END_USER_VALUE.md`](END_USER_VALUE.md) |
| Procurement — vs OPA/Cedar/Casbin | [`governance/PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md) §Feature comparison |
| Operator policy change / rollback | [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) §12 · [`governance/ROLLBACK_PROTOCOL.md`](governance/ROLLBACK_PROTOCOL.md) |

---

## Troubleshooting (common)

| Symptom | Fix |
|---------|-----|
| `connection refused` on CONNECT | Check `ACP_API_URL`, firewall, WSL portproxy ([`RUNBOOK.md`](RUNBOOK.md)) |
| GHCR `denied` on `--ghcr` | Run publish workflow; `docker login ghcr.io`; or use `bash scripts/acp-up.sh --compose` |
| GHCR verify shows old `governance_version` | Image stale vs `master` — `docker compose up --build` or republish GHCR; see [`ecc-48h-post-verify/RESULTS.md`](governance/practice-evidence/ecc-48h-post-verify/RESULTS.md) G-ECC-01 |
| `allowed: false` for known agent | Ask operator — your `agent_id` / `role` may not match their config |
| Changed config but API unchanged | Restart API host — config loads at startup only |
| After `git pull`, old governance version | `docker compose up --build -d` (not `restart` only) |

---

**Last updated:** 2026-07-02 · Catalog v1.5.0 · baseline `44a5fef` · Sonnet audit drift-close
