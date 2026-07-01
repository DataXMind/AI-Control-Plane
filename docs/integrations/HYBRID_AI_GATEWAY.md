# Hybrid AI Gateway × ACP Integration

**Document ID:** ACP-INTEG-HYBRID-GATEWAY-001  
**Gateway repo:** [DataXMind/Hybrid-AI-Gateway](https://github.com/DataXMind/Hybrid-AI-Gateway)  
**ACP repo:** AI-Control-Plane (this project)

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
| Wire agents | Gateway / Antigravity devs | [`CLIENT_INTEGRATION.md`](../CLIENT_INTEGRATION.md) |
| Gateway PR spec (SSOT) | Hybrid-AI-Gateway maintainers | [`HYBRID_AI_GATEWAY_PR_SPEC.md`](HYBRID_AI_GATEWAY_PR_SPEC.md) |
| Python sample | Copy into gateway or agent runner | [`examples/integrate/python/gateway_antigravity_hook.py`](../../examples/integrate/python/gateway_antigravity_hook.py) |

**No fork** of ACP required for integration — only `ACP_API_URL`.

---

## 2. Agent mapping (shipped `production-config/`)

Default bundle templates register Hybrid AI Gateway under `rust-gateway`:

| ACP `agent_id` | Name | Runner | Role | Use for |
|----------------|------|--------|------|---------|
| `agent1` | infra-antigravity | antigravity | infra | K8s, helm, CI — **Antigravity Sonnet/Opus** |
| `agent2` | backend-vscode | vscode | backend | Rust/Python code, `git_read`, `build.rust` |
| `agent3` | reviewer-cli | cli | reviewer | Read-only review |

Customize `customer-bundle/production-config/agents.yml` for your tenant.

---

## 3. Deploy ACP for gateway team

```bash
# Operator: install bundle to /opt/acp (see HUONG_DAN_CAI_DAT.md)
export ACP_API_URL=http://<acp-host>:8000
bash verify-pilot.sh   # from /opt/acp after compose up
```

Share `ACP_API_URL` with:

- Antigravity IDE agent runners (Shell env)
- `Hybrid-AI-Gateway` services that invoke tools
- Local dev machines building `src/rust-gateway`

---

## 4. Integration choke point (Task 2)

### Python (request-router / agent scripts)

Before any tool execution in gateway or agent harness:

```python
from examples.integrate.python.gateway_antigravity_hook import acp_allow_tool

acp_allow_tool(agent_id="agent1", tool_name="k8s_apply", role="infra")
# ... proceed with tool ...
```

Or copy `acp_allow()` from [`CLIENT_INTEGRATION.md`](../CLIENT_INTEGRATION.md) — same HTTP contract.

### Rust (`src/rust-gateway`)

Add middleware or pre-tool hook calling `POST /policy/evaluate` — see Rust example in [`CLIENT_INTEGRATION.md`](../CLIENT_INTEGRATION.md) §5.

Suggested env:

```bash
ACP_API_URL=http://acp.internal:8000
ACP_AGENT_ID=agent2
ACP_PROJECT_ID=rust-gateway
```

### Shell (Antigravity / CI)

```bash
export ACP_API_URL=http://127.0.0.1:8000
curl -sf -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent1","project_id":"rust-gateway","tool_name":"git_read","role":"infra"}' \
  | python3 -c "import sys,json; b=json.load(sys.stdin); sys.exit(0 if b.get('allowed') else 1)"
```

Exit non-zero → **do not run tool** (fail-closed).

### TypeScript (PolicyClient path)

Gateway TS clients should use the same contract as documented in ACP OpenAPI — `allowed` + `reason` on 200; deny on timeout.

---

## 5. Fail-closed vs gateway compliance

| Layer | Default on error | Scope |
|-------|------------------|-------|
| **ACP** `/policy/evaluate` | **Deny** | Agent tool / action |
| **Gateway H-2** `compliance_policy` | Allow (except `prohibited`) | Chat completion content |

Do not replace gateway compliance with ACP — **stack both** where appropriate.

---

## 6. Verification checklist

- [ ] ACP bundle up — `verify-pilot.sh` PASS @ `/opt/acp`
- [ ] `agent1` allow + unknown agent deny via curl
- [ ] Antigravity runner has `ACP_API_URL`
- [ ] One tool path in gateway/agent calls evaluate before execution
- [ ] ACP down → tool path denies (fail-closed test)

---

## 7. Next steps in Hybrid-AI-Gateway repo

**Canonical PR spec (ACP SSOT):** [`HYBRID_AI_GATEWAY_PR_SPEC.md`](HYBRID_AI_GATEWAY_PR_SPEC.md) — `orchestrator/acp_client.py` API, tests, env, Antigravity `k8s_apply` sequence diagrams.

Recommended PRs (gateway repo, not ACP):

1. Add `orchestrator/acp_client.py` — per PR spec §4 (based on `gateway_antigravity_hook.py`)
2. Env `ACP_API_URL` in docker-compose / K8s for staging
3. Optional Rust middleware in `rust-gateway` for edge policy on internal admin tools

ACP side stays **HTTP-only** — no import of gateway code into `ai_control_plane`.

---

**Last updated:** 2026-07-02
