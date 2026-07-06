# Hybrid AI Gateway × ACP Integration

**Document ID:** ACP-INTEG-HYBRID-GATEWAY-001  
**Gateway repo:** [DataXMind/Hybrid-AI-Gateway](https://github.com/DataXMind/Hybrid-AI-Gateway)  
**ACP repo:** AI-Control-Plane (this project)  
**Integration status:** **ACP side PASS** @ `aeca32a` ([#188](https://github.com/DataXMind/AI-Control-Plane/pull/188)) · evidence: [`practice-evidence/hybrid-gateway-acp-integration/RESULTS.md`](../governance/practice-evidence/hybrid-gateway-acp-integration/RESULTS.md)

---

## 0. Naming — do not conflate

| Name | Product | Role |
|------|---------|------|
| **ACP** (this repo) | AI **Agent** Policy Engine | `POST /policy/evaluate` before **agent tool calls** (git, k8s, build…) |
| **SACP** (gateway README) | **Sovereign** AI Control Plane | LLM **gateway** — routing, budget, compliance on chat completions |

They are **complementary**:

```text
Antigravity / VS Code agents ──tool intent──► ACP (allow/deny)
Hybrid AI Gateway ─────────────────────────► LLM providers (Claude, GPT…)
Gateway compliance (H-2) ───────────────────► content / tenant policy on HTTP chat
```

See [`ECC_ACP_INTEGRATION_ANALYSIS.md`](../governance/ECC_ACP_INTEGRATION_ANALYSIS.md).

---

## 1. Doc tiers for this integration

| Step | Who | Doc |
|------|-----|-----|
| Host ACP | Platform / DevOps | [`customer-bundle/HUONG_DAN_CAI_DAT.md`](../../customer-bundle/HUONG_DAN_CAI_DAT.md) (VI) or [`CUSTOMER_INSTALL.md`](../../examples/minimal/CUSTOMER_INSTALL.md) |
| Wire agents (enforce) | Antigravity / shell / CI | [`examples/integrate/python/run_tool_guarded.py`](../../examples/integrate/python/run_tool_guarded.py) + [`examples/integrate/README.md`](../../examples/integrate/README.md) |
| Wire agents (HTTP ref) | Any language | [`CLIENT_INTEGRATION.md`](../CLIENT_INTEGRATION.md) |
| Gateway PR spec (SSOT) | Hybrid-AI-Gateway maintainers | [`HYBRID_AI_GATEWAY_PR_SPEC.md`](HYBRID_AI_GATEWAY_PR_SPEC.md) |
| Python sample | Copy or import pattern | [`examples/integrate/python/gateway_antigravity_hook.py`](../../examples/integrate/python/gateway_antigravity_hook.py) |

**No fork** of ACP required for integration — only `ACP_API_URL`.

---

## 2. Agent mapping (shipped `production-config/`)

Default bundle templates register Hybrid AI Gateway under `rust-gateway`:

| ACP `agent_id` | Name | Runner | Role | Machine (pilot) |
|----------------|------|--------|------|-----------------|
| `agent1` | infra-antigravity | antigravity | infra | MSI |
| `agent2` | backend-vscode | vscode | backend | Mac Mini |
| `agent3` | reviewer-cli | cli | reviewer | — |

Customize `customer-bundle/production-config/agents.yml` for your tenant.

### Per-machine env (not in git)

`.env` is **gitignored**. Same repo clone on MSI + Mac; **different** runtime identity:

```bash
# Shared
export ACP_API_URL=http://<acp-host>:8000
export ACP_PROJECT_ID=rust-gateway

# MSI — agent1
export ACP_AGENT_ID=agent1
export ACP_ROLE=infra

# Mac — agent2
export ACP_AGENT_ID=agent2
export ACP_ROLE=backend
```

---

## 3. Deploy ACP for gateway team

```bash
# Operator: install bundle to /opt/acp (see HUONG_DAN_CAI_DAT.md)
export ACP_API_URL=http://<acp-host>:8000
bash verify-pilot.sh   # from /opt/acp after compose up
```

Share `ACP_API_URL` with Antigravity shells, dev laptops, and Gateway services that invoke tools.

---

## 4. Integration choke point (Task 2)

### Enforce — shell / Antigravity terminal (recommended @ 0.x)

From **ai-control-plane** repo root (paths on `master` since #188):

```bash
export ACP_API_URL=http://<acp-host>:8000
export ACP_AGENT_ID=agent1    # or agent2 on Mac
export ACP_ROLE=infra       # or backend

python3 examples/integrate/python/run_tool_guarded.py --tool git_read -- git status

# k8s + ABAC args (agent1 infra)
python3 examples/integrate/python/run_tool_guarded.py --tool k8s_apply \
  --args-json '{"environment":"dev","plan_submitted":true}' \
  -- kubectl apply -f deployment.yaml
```

Shell gate only (no subprocess wrapper):

```bash
bash examples/integrate/shell/acp_evaluate.sh git_read && your-command
```

### Python (in-process)

```python
from examples.integrate.python.gateway_antigravity_hook import acp_allow_tool

acp_allow_tool(agent_id="agent1", tool_name="k8s_apply", role="infra")
# ... proceed with tool ...
```

### Antigravity IDE auto-hook (zsh)

```bash
bash examples/integrate/shell/install_antigravity_hook.sh
# Requires ACP_API_URL + ACP_AGENT_ID + ACP_ROLE in env; open new terminal
# Wraps: kubectl apply/delete, git status/commit/push, cargo build/run/test
```

Disable per session: `export ACP_SHELL_GUARD=0`

### Hybrid-AI-Gateway `request-router`

Merged on GitHub **`main`** ([#4](https://github.com/DataXMind/Hybrid-AI-Gateway/pull/4)): `orchestrator/acp_client.py`, `GET /acp/status`, `docs/ACP_INTEGRATION.md`.

### Rust (`src/rust-gateway`) — production

Tracks B1/B2 merged ([#10](https://github.com/DataXMind/Hybrid-AI-Gateway/pull/10), [#12](https://github.com/DataXMind/Hybrid-AI-Gateway/pull/12)):

- `GET /acp/status` — observability (B1)
- `POST /admin/v1/tenants/:id/freeze` — `acp_gate` middleware (B2)

Operator evidence 2026-07-06: VPS `acp_reachable: true`. Chat completions remain H-2 (no ACP gate).

See Gateway [`sacp-acp-gap/RESULTS.md`](https://github.com/DataXMind/Hybrid-AI-Gateway/blob/main/docs/governance/practice-evidence/sacp-acp-gap/RESULTS.md).

---

## 5. Fail-closed vs gateway compliance

| Layer | Default on error | Scope |
|-------|------------------|-------|
| **ACP** `/policy/evaluate` | **Deny** | Agent tool / action |
| **Gateway H-2** `compliance_policy` | Allow (except `prohibited`) | Chat completion content |

Stack both where appropriate — do not conflate.

---

## 6. Verification checklist

Operator evidence 2026-07-03 — see [RESULTS.md](../governance/practice-evidence/hybrid-gateway-acp-integration/RESULTS.md).

- [x] ACP production up — VPS `policy_rules_count: 10`
- [x] `agent1` allow + unknown agent deny
- [x] `agent2` allow `build.rust` + deny `k8s_apply` (Mac)
- [x] Antigravity / dev shells have `ACP_API_URL` + per-machine `ACP_AGENT_ID`
- [x] Tool path calls evaluate before execution — `run_tool_guarded.py`
- [x] ACP down → tool path denies — `fail_closed_drill.sh`
- [x] Runnable scripts on `master` — #188, #189
- [x] Gateway repo `orchestrator/acp_client` merged — [Hybrid-AI-Gateway #4](https://github.com/DataXMind/Hybrid-AI-Gateway/pull/4)
- [x] Antigravity shell auto-gate — `antigravity_shell_hook.zsh` + `install_antigravity_hook.sh`
- [x] Production client bundle — `customer-bundle/integrations/`
- [x] Rust prod `/acp/status` (B1) — VPS 2026-07-06
- [x] Rust admin ACP middleware (B2) — freeze route evaluate + allow HTTP 200
- [ ] Dog-fooding case study published (Gateway repo — optional)

---

## 7. Next steps

| Priority | Action | Repo |
|----------|--------|------|
| 1 | Daily use: `install_antigravity_hook.sh` + `~/.acp-agent.env` | ACP `customer-bundle/integrations/` |
| 2 | Gateway Docker: `docker compose up` + `/acp/status` | Hybrid-AI-Gateway `main` |
| 3 | Optional Rust kubectl pre-check | Gateway `mlops-engine` |
| 4 | PB-9 Day 14 PASS — PB-12 prep | Operator — [`pb-9-day14-review/RESULTS.md`](../governance/practice-evidence/pb-9-day14-review/RESULTS.md) |
| 5 | VPS policy sync runbook | `scripts/sync_vps_acp_admin_freeze.sh` (root on VPS) |
| 6 | NGROK rotate (SACP Track C) | Operator — ngrok.com + VPS systemd |
| 7 | LLM hot-path ACP (optional future) | Gateway new track — out of B1/B2 scope |

ACP side stays **HTTP-only** — no import of gateway code into `ai_control_plane`.

---

**Last updated:** 2026-07-06 · CONNECT CLOSED · SACP B1+B2 VPS CLOSED (admin scope)
