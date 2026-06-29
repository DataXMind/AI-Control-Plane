# ACP Quickstart — 5 Minutes, Two Doors

**Document ID:** ACP-QUICKSTART-001  
**Audience:** End-users, evaluators, app integrators (not contributors)  
**Advanced map:** [`DEVELOPER_SCENARIOS.md`](DEVELOPER_SCENARIOS.md) · **Contribute:** [`CONTRIBUTING.md`](../CONTRIBUTING.md)

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
- Git (to clone) — or use a published image after PB-12 GHCR

### Steps

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
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
For production-like shipped config (10 rules), see [`RUNBOOK.md`](RUNBOOK.md) — operator path.

### Stop

```bash
docker compose -f examples/minimal/docker-compose.yml down
```

---

## 2. Door CONNECT — Use a remote ACP

**Time:** ~2 minutes

Someone else (your platform team) runs ACP. You only need the base URL.

### Step 1 — One environment variable

Copy [`.env.client.example`](../.env.client.example):

```bash
export ACP_API_URL=http://<acp-host>:8000
# Examples:
#   http://localhost:8000          — ACP on same machine (RUN door finished)
#   http://192.168.1.10:8000       — LAN (see RUNBOOK WSL portproxy if needed)
#   http://acp.internal:8000       — corporate DNS
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

## 3. What next?

| Goal | Go to |
|------|-------|
| Wire policy into your agent app | [`examples/integrate/README.md`](../examples/integrate/README.md) |
| OpenAPI / HTTP contract | http://localhost:8000/docs after RUN |
| Fork, PR, governance | [`CONTRIBUTING.md`](../CONTRIBUTING.md) |
| Staging, VPS, dual-host, profiles | [`DEVELOPER_SCENARIOS.md`](DEVELOPER_SCENARIOS.md) |
| Production operations | [`RUNBOOK.md`](RUNBOOK.md) |

---

## Troubleshooting (common)

| Symptom | Fix |
|---------|-----|
| `connection refused` on CONNECT | Check `ACP_API_URL`, firewall, WSL portproxy ([`RUNBOOK.md`](RUNBOOK.md)) |
| `allowed: false` for known agent | Ask operator — your `agent_id` / `role` may not match their config |
| Changed config but API unchanged | Restart API host — config loads at startup only |
| After `git pull`, old governance version | `docker compose up --build -d` (not `restart` only) |

---

**Last updated:** 2026-06-30 · Catalog v1.4.0
