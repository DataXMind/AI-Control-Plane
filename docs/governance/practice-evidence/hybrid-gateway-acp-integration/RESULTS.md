# Hybrid AI Gateway × ACP — Integration evidence (Product A)

**Document ID:** ACP-PRACTICE-HYBRID-GATEWAY-ACP-001  
**Status:** **CONNECT PASS — CLOSED** (MSI + Mac + Gateway remote, 2026-07-03)  
**ACP baseline:** `master` @ post-#190 (after integration close PR)  
**Gateway baseline:** `main` @ `35bf124` ([#4](https://github.com/DataXMind/Hybrid-AI-Gateway/pull/4))  
**ACP host:** VPS `ubuntu-vps` · Tailscale `100.94.21.33:8000` · Profile B · `policy_rules_count: 10`

---

## 1. Scope — sign-off

| Layer | Verdict |
|-------|---------|
| **Product A** — policy before tool, fail-closed | **PASS** |
| **Gateway `orchestrator/acp_client`** on GitHub | **PASS** — Hybrid-AI-Gateway #4 |
| **Antigravity IDE shell auto-hook** | **PASS** — `antigravity_shell_hook.zsh` + `install_antigravity_hook.sh` |
| **Production client bundle** | **PASS** — `customer-bundle/integrations/` |
| SACP / Karpathy / ECC | Out of scope |
| **AEOS × ACP** | **Separate track** — [`aeos-acp-integration/RESULTS.md`](../aeos-acp-integration/RESULTS.md) · Phase 2 PASS 2026-07-05 |
| Rust `kubectl` middleware, case study | Follow-up (not blocking CONNECT) |

---

## 2. Environment

| Node | `ACP_AGENT_ID` | `ACP_ROLE` | Verified |
|------|----------------|------------|----------|
| MSI (WSL) | `agent1` | `infra` | smoke + enforce + Docker `/acp/status` |
| Mac Mini | `agent2` | `backend` | allow `build.rust` / deny `k8s_apply` |
| VPS | — | — | production-config 10 rules |

---

## 3. Verification matrix

| # | Check | MSI | Mac | Artifact |
|---|-------|-----|-----|----------|
| 1 | Health 10 rules | ✓ | ✓ | curl |
| 2 | policy_smoke_matrix 5/5 | ✓ | ✓ | ACP `examples/integrate/shell/` |
| 3 | run_tool_guarded enforce | ✓ | ✓ | #188 |
| 4 | fail_closed_drill | ✓ | — | shell script |
| 5 | Gateway `/acp/status` | ✓ | — | request-router Docker |
| 6 | Gateway remote merge | ✓ | — | Hybrid-AI-Gateway #4 |
| 7 | zsh auto-hook kubectl/git/cargo | ✓ | install ready | `antigravity_shell_hook.zsh` |
| 8 | Scripts on ACP master | ✓ | ✓ | #188, #189, close PR |

---

## 4. Install paths (end-user)

### ACP repo (integrators)

```bash
git pull origin master
cp customer-bundle/integrations/antigravity-acp.env.example ~/.acp-agent.env
# edit ACP_AGENT_ID / ACP_ROLE per machine
source ~/.acp-agent.env
bash examples/integrate/shell/install_antigravity_hook.sh
```

### Gateway repo (request-router)

```bash
git pull origin main   # includes #4
cp .env.example .env
docker compose build request-router && docker compose up -d request-router
curl -sf http://localhost:8082/acp/status
```

---

## 5. Follow-up (non-blocking)

| Item | Owner |
|------|-------|
| `mlops-engine` kubectl HTTP pre-check | Gateway Rust PR |
| Dog-fooding case study publish | Gateway docs |
| PB-9 soak 07-05..07-06 | VPS operator |
| GHCR Path C when PB-12 | Operator |
| **`export` in `~/.acp-agent.env`** (2026-07-04) | MSI/Mac — template fixed in bundle |

### 5.1 MSI env pitfall (2026-07-04)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `curl $ACP_API_URL/health` OK | Shell expands `$ACP_API_URL` | — |
| `python3` KeyError `ACP_API_URL` | Var not exported to children | `export` every line in `~/.acp-agent.env` |
| `run_tool_guarded` → `[Errno 111] Connection refused` | Python defaults `ACP_API_URL` to `127.0.0.1:8000` | Re-copy `antigravity-acp.env.example`, `source ~/.acp-agent.env` |

---

## 6. Session audit trail

See prior §6 in git history — key fix: SSOT paths in `examples/integrate/` (ACP) + `scripts/acp/` (Gateway).

---

## 7. Sign-off

| Role | Verdict | Date |
|------|---------|------|
| Operator evidence | Hybrid Gateway × ACP **CONNECT CLOSED** | 2026-07-03 |
| Gateway remote | **MERGED** #4 `35bf124` | 2026-07-03 |
| IDE auto-hook | **SHIPPED** zsh wrapper | 2026-07-03 |
