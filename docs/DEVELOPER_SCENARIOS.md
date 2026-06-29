# Developer Scenarios — Fork, Clone, and Client Usage

> **End-user / evaluator / app integrator?** Start with **[`QUICKSTART.md`](QUICKSTART.md)** (5 min, two doors).  
> This document is the **advanced map** for contributors, operators, and multi-host setups.

**Document ID:** ACP-DEV-SCENARIOS-001  
**Status:** Active (pre–Public Beta)  
**Audience:** Evaluators, contributors, operators, remote clients  
**Related:** [`CONTRIBUTING.md`](../CONTRIBUTING.md) · [`examples/README.md`](../examples/README.md) · [`RUNBOOK.md`](RUNBOOK.md) · [`PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md)

---

## How to use this document

1. **Pick your role** (table below) → open the linked scenario.
2. **Answer three setup questions** before running commands:
   - **Where does the API run?** (your laptop, Docker, VPS, WSL behind portproxy)
   - **Which config profile?** (A fixture / B shipped / C Docker image)
   - **Are you API host or client?** (`ACP_API_URL` is for **clients only**)
3. **Follow one scenario end-to-end** — do not mix host env vars from one scenario with client steps from another.

| Role | Start here | Fork? | Clone? |
|------|------------|-------|--------|
| **Evaluator** — try policy in ≤15 min | [K1](#k1--evaluator-quick-try-15-minutes) | No | Yes |
| **Docs contributor** | [K2](#k2--docs-only-contributor) | Yes | Fork → clone fork |
| **Code contributor** | [K3](#k3--code-contributor) | Yes | Fork → clone fork |
| **Daily native dev** | [K4](#k4--daily-native-dev-no-docker) | No* | Yes |
| **Staging / pre-prod** | [K5](#k5--staging-with-shipped-config) | No* | Yes |
| **Remote client** (Mac, CI, second machine) | [End-user clients](#end-user-and-client-usage) · [U1](#u1--wsl2-remote-client-on-lan) | No | No** |
| **Operator** (PB-9 soak, dual-host) | [S1](#s1--dual-host-pb-9-soak-msi--vps) | No | Yes (maintainer) |
| **Governance-only adopter** | [S2](#s2--governance-framework-without-api) | Optional | Yes |

\* Maintainers with push access clone upstream directly.  
\** Remote clients only need `ACP_API_URL` pointing at a running API — no repo required unless using `agentctl` from source.

### Fork vs clone — decision

| Action | When | Purpose |
|--------|------|---------|
| **`git clone`** | Evaluate, run locally, daily dev | Working copy on your machine |
| **`git fork` + clone fork** | Open a PR to upstream | Your branches; no direct push to `master` |
| **Read-only / audit** | Enterprise security review | Docs + practice evidence; API optional |

**Pre–PB-12:** repository is **private** — clone requires org access.  
**Post–PB-12 (~2026-07-10):** public — **Evaluate → clone** · **Contribute → fork**.

---

## Config profiles (pick one per scenario)

| Profile | `ACP_CONFIG_DIR` | Rules | Use when |
|---------|------------------|-------|----------|
| **A** | `tests/fixtures/config` | 8 | Dev, CI, smoke, Docker minimal, PB-7/PB-9 parity |
| **B** | unset → `config/` (shipped) | 10 | Staging closer to production |
| **C** | Baked in Docker image (fixture) | 8 | `examples/minimal` compose, PB-9 soak |

Config loads **once at API startup**. Changing env on a client shell does not change a running API. See [U2](#u2--acp_config_dir-set-but-api-unchanged).

---

## A. Five common scenarios

### K1 — Evaluator quick try (≤15 minutes)

**Who:** LLM app builder, technical evaluator ([`PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md) Tier 2)  
**Fork/clone:** Clone only (public after PB-12)  
**Path:** Docker — matches PB-7 clean-machine gate

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -sf http://localhost:8000/health | python3 -m json.tool
curl -sf -X POST http://localhost:8000/policy/evaluate \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}' \
  | python3 -m json.tool
```

**Pass:** `status: ok` · `allowed: true` · unknown agent → `allowed: false` with non-empty `reason`.

```bash
export ACP_API_URL=http://localhost:8000
bash scripts/verify_governance_status_runtime.sh
```

**Anchor:** [`pb-7-clean-machine-fork/RUNBOOK.md`](governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md) Path A · [`examples/README.md`](../examples/README.md)

---

### K2 — Docs-only contributor

**Who:** Community contributor fixing typos, governance docs, examples README  
**Fork/clone:** Fork upstream → clone your fork → branch `docs/...`

```bash
git clone https://github.com/<you>/AI-Control-Plane.git
cd AI-Control-Plane
git remote add upstream https://github.com/DataXMind/AI-Control-Plane.git
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke   # 8/8 required before PR
git checkout -b docs/my-fix
```

**Rules:** Docs-only PR — `docs/**`, `*.md` only; no `src/` (P-02 scope creep).  
**Anchor:** [`CONTRIBUTING.md`](../CONTRIBUTING.md) Quick Start · [`CURSOR_RISK_POLICY.md`](governance/CURSOR_RISK_POLICY.md) F11

---

### K3 — Code contributor

**Who:** Developer changing policy engine, API, or CLI  
**Fork/clone:** Fork + branch `feat/...` or `fix/...`

```bash
# Same setup as K2
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
```

**Before coding:** read [`AGENTS.md`](../AGENTS.md) and [`CURSOR_RISK_POLICY.md`](governance/CURSOR_RISK_POLICY.md).  
**Invariant:** do not replace `core/policies.py` with an external OSS engine ([`ARCHITECTURE.md`](../ARCHITECTURE.md) §8).

---

### K4 — Daily native dev (no Docker)

**Who:** Maintainer or contributor on WSL / macOS / Linux  
**Fork/clone:** Clone (maintainers) or clone fork (contributors)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
cd AI-Control-Plane
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 127.0.0.1 --port 8000
```

**Second terminal (client):**

```bash
export ACP_API_URL=http://127.0.0.1:8000
agentctl assign rust-gateway agent2 git_read --json
curl -sf $ACP_API_URL/governance/status | jq .governance_version
```

Profile **A** — matches CI and smoke gate.

---

### K5 — Staging with shipped config

**Who:** AI DevOps preparing a deploy closer to production  
**Fork/clone:** Clone; customize `config/*.yml` on a branch (no secrets in git)

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
pip install -e .
# Do NOT set ACP_CONFIG_DIR → Profile B (10 rules in config/)
uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000
curl -sf http://localhost:8000/health | jq .policy_rules_count   # expect 10
```

**Optional:** `export ACP_DATA_DIR=/var/lib/acp` · `ACP_REDIS_URL=redis://...`  
**Anchor:** [`ARCHITECTURE.md`](../ARCHITECTURE.md) · Study 08 remote Profile B in [`PRACTICE_STUDIES_AUDIT_01-07.md`](governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md)

---

## B. Three edge scenarios (easy to get wrong)

### U1 — WSL2: remote client on LAN

**Situation:** API in WSL; Mac or another PC calls `curl` / `agentctl`.  
**Common mistakes:** `uvicorn --host 127.0.0.1` · client uses `127.0.0.1` on another machine · forgot Windows portproxy after WSL restart.

**API host (WSL):**

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --host 0.0.0.0 --port 8000
```

**Windows (Admin PowerShell) — portproxy:**

```powershell
# WSL_IP from: wsl hostname -I
netsh interface portproxy add v4tov4 listenport=8000 listenaddress=0.0.0.0 connectport=8000 connectaddress=<WSL_IP>
```

**Client (Mac / other PC):**

```bash
export ACP_API_URL=http://<WINDOWS_LAN_IP>:8000
curl -sf $ACP_API_URL/health
agentctl status rust-gateway --json
```

**Plan B:** Run API on Mac natively; laptop is client only.  
**Anchor:** [`TOPOLOGY_WINDOWS_MAC.md`](governance/practice-evidence/study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md) · [`RUNBOOK.md`](RUNBOOK.md)

---

### U2 — `ACP_CONFIG_DIR` set but API unchanged

**Situation:** Export env in client shell; API was started earlier with different config.  
**Root cause:** Config loads at **server startup** only.

**Fix:**

```bash
# Stop API → set env on the SAME host process → restart
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app ...
# Docker: set env in compose + docker compose up --build -d
```

**Wrong:** Set `ACP_CONFIG_DIR` on client only and expect policy to change.

---

### U3 — Stale catalog after `git pull`

**Situation:** After pull, `governance/status` still shows old `governance_version` or pattern count.  
**Root cause:** Old Docker image; `compose restart` does not rebuild.

**Fix:**

```bash
git pull origin master
docker compose -f examples/minimal/docker-compose.yml up --build -d
sleep 15
curl -s http://localhost:8000/governance/status | jq .governance_version
bash scripts/verify_governance_status_runtime.sh
```

Use `.governance_version` — not `.version` (returns `null`).

---

## C. Two special scenarios

### S1 — Dual-host PB-9 soak (MSI + VPS)

**Who:** Maintainer / operator — not a typical fork path  
**Goal:** 14-day calendar soak + dual-host evidence for Day 14 review

**MSI (WSL):**

```bash
git clone ...   # commit access required
docker compose -f examples/minimal/docker-compose.yml up -d --build
bash scripts/restart_soak_loop.sh
# Machine lines → docs/governance/PB9_SOAK_ITERATION_LOG.md
```

**VPS (ubuntu-vps):**

```bash
git clone /root/AI-Control-Plane
sudo systemctl enable --now acp-staging.service acp-soak.service
# Host-local log only — do NOT append VPS lines to PB9_SOAK_ITERATION_LOG.md
```

**Human tick:** [`PB9_STAGING_SOAK_LOG.md`](governance/PB9_STAGING_SOAK_LOG.md) daily table (operator only).  
**Anchor:** [`examples/minimal/systemd/README.md`](../examples/minimal/systemd/README.md) · P-14 catalog drift in [`LESSONS_LEARNED.md`](governance/LESSONS_LEARNED.md)

---

### S2 — Governance framework without API

**Who:** Team adopting PACE / LESSONS with Cursor or Claude — no control plane deploy  
**Fork/clone:** Fork optional; clone to copy docs

```bash
git clone https://github.com/DataXMind/AI-Control-Plane.git
# Adopt without running API:
#   .cursorrules, docs/prompts/SESSION_ANCHOR_TEMPLATE.md
#   docs/governance/LESSONS_LEARNED.md (P-01..P-16)
#   docs/DEVELOPMENT_PROTOCOL.md (PACE)
```

**Value:** Standalone governance moat — see [`VALUE_AUDIT_MATRIX.md`](governance/VALUE_AUDIT_MATRIX.md) Tier 3.

---

## End-user and client usage

This section is for people who **use** ACP (evaluate policy, call API, run `agentctl`) — not for opening PRs.

### Audience → scenario map

| End-user type | Goal | Scenario | Repo needed? |
|---------------|------|----------|--------------|
| **LLM app builder** | Prove deny-by-default in 15 min | K1 | Clone once |
| **App integrator** | Call `/policy/evaluate` from your agent | K1 or K5 + HTTP client | Clone or API URL only |
| **Operator** | Run staging, quotas, audit | K5 · [`RUNBOOK.md`](RUNBOOK.md) | Clone |
| **Desktop client** (Mac, second PC) | Talk to API on another host | [U1](#u1--wsl2-remote-client-on-lan) · Study 06/07 | No — `ACP_API_URL` only |
| **Security auditor** | Read threat model + evidence | S2 docs path | Optional clone |
| **Contributor** | Merge fix upstream | K2 or K3 | Fork + clone |

### Client-only checklist

If you are **not** starting the API:

1. Get **`ACP_API_URL`** from whoever runs the host (e.g. `http://192.168.1.10:8000`).
2. Verify connectivity:

   ```bash
   export ACP_API_URL=http://<host>:8000
   curl -sf $ACP_API_URL/health | python3 -m json.tool
   ```

3. **Policy check** (your agent’s identity must exist in host `agents.yml`):

   ```bash
   curl -sf -X POST $ACP_API_URL/policy/evaluate \
     -H "Content-Type: application/json" \
     -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}'
   ```

4. **CLI** (install from same repo revision as server, or matching release after PB-12):

   ```bash
   pip install -e ".[dev]"   # or future PyPI package
   export ACP_API_URL=http://<host>:8000
   agentctl assign rust-gateway agent2 git_read --json
   agentctl gov status
   ```

5. **Do not set** `ACP_CONFIG_DIR` on the client unless you also run the API on that machine.

### Host vs client environment variables

| Variable | Set on **API host** | Set on **client** |
|----------|---------------------|-------------------|
| `ACP_CONFIG_DIR` | Yes (Profile A or B) | No (unless you host API) |
| `ACP_DATA_DIR` | Yes (persist tasks) | No |
| `ACP_REDIS_URL` | Yes (if using Redis) | No |
| `ACP_API_URL` | Optional (local CLI) | **Yes** — base URL for HTTP |

### Integration patterns for application clients

| Pattern | When | Example |
|---------|------|---------|
| **HTTP evaluate** | Agent before tool call | `POST /policy/evaluate` → deny if `allowed: false` |
| **Health gate** | Startup probe | `GET /health` → fail app if not `ok` |
| **Quota** | Budget enforcement | `GET /quota/{project_id}` before LLM call |
| **Identity** | JWT-bound agents | `POST /identity/verify` (see smoke SMK-06) |
| **Governance UX** | Operator dashboards | `GET /governance/status` · `agentctl gov status` |

Fail-closed rule for integrators: if evaluate fails or times out, **deny the action** — same as unknown agent.

### Quick decision tree

```text
Need to change code/docs in repo?
  YES → Contribute? → fork + K2/K3
  NO  → Need API running locally?
          YES → Docker? → K1 (yes) / K4 (no)
          NO  → Only call remote API? → Client checklist + ACP_API_URL
                Only governance process? → S2
```

### One-page cheat sheet

```text
EVALUATE (15 min):     clone → docker compose up --build → health + policy curl
CONTRIBUTE DOCS:       fork → branch docs/* → smoke 8/8 → PR
CONTRIBUTE CODE:       fork → AGENTS.md → smoke + ruff + mypy → PR
DEV DAILY:             clone → venv → ACP_CONFIG_DIR=fixtures → uvicorn
STAGING:               clone → Profile B → ACP_DATA_DIR optional
REMOTE CLIENT:         ACP_API_URL=http://<host>:8000 (no repo required)
AFTER GIT PULL:        docker compose up --build -d (NOT restart only)
GOVERNANCE ONLY:       clone docs → SESSION_ANCHOR + LESSONS (no API)
```

---

## Runtime discovery

After API is up:

```bash
export ACP_API_URL=http://localhost:8000
curl -s $ACP_API_URL/governance/status | jq '.doc_links.developer_scenarios'
# → "docs/DEVELOPER_SCENARIOS.md"
```

---

**Last updated:** 2026-06-30 · Catalog v1.4.0 · See [`GOVERNANCE_CHANGELOG.md`](governance/GOVERNANCE_CHANGELOG.md)
