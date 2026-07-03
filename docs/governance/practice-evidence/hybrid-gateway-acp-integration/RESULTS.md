# Hybrid AI Gateway × ACP — Integration evidence (Product A)

**Document ID:** ACP-PRACTICE-HYBRID-GATEWAY-ACP-001  
**Status:** **ACP CONNECT door — PASS** (MSI + Mac, 2026-07-03)  
**Gateway repo wire:** **PARTIAL** (local MSI only; not merged on `DataXMind/Hybrid-AI-Gateway`)  
**ACP baseline:** `master` @ `aeca32a` ([#188](https://github.com/DataXMind/AI-Control-Plane/pull/188))  
**ACP host:** VPS `ubuntu-vps` · Tailscale `100.94.21.33:8000` · Profile B · `policy_rules_count: 10`

---

## 1. Scope — what “done” means

| Layer | Question | This evidence |
|-------|----------|---------------|
| **Product A** | May agent X call tool Y? | **PASS** — HTTP evaluate, fail-closed, 2 machines |
| **SACP / Gateway LLM** | Chat routing, budget | Out of scope — separate product |
| **Karpathy / ECC** | Governance OS on repo | Out of scope — optional Tier 3 |

**Mission (Tier 1–2 integrator):** Wire `POST /policy/evaluate` before tool execution for Antigravity + Gateway team.  
**Not required for this mission:** Gateway GitHub merge, Antigravity IDE built-in hook, Rust `kubectl` middleware, published case study.

---

## 2. Environment

| Node | Role | `ACP_AGENT_ID` | `ACP_ROLE` | Runner |
|------|------|----------------|------------|--------|
| MSI (WSL) | infra | `agent1` | `infra` | Antigravity |
| Mac Mini | backend | `agent2` | `backend` | Antigravity / IDE |
| VPS | policy plane | — | — | ACP API `:8000` |

Project: `rust-gateway` · Config: `/opt/acp/production-config` (build-local path, not GHCR Path C).

---

## 3. Verification matrix (2026-07-03)

| # | Check | MSI | Mac | Script / method |
|---|-------|-----|-----|-----------------|
| 1 | `GET /health` → 10 rules | ✓ | ✓ | `curl` |
| 2 | agent1 `git_read` allow | ✓ | — | `run_tool_guarded` / curl |
| 3 | agent2 `build.rust` allow | ✓ | ✓ | `run_tool_guarded` |
| 4 | agent2 `k8s_apply` rbac deny | ✓ | ✓ | curl / `run_tool_guarded` exit=1 |
| 5 | agent3 `k8s_apply` deny | ✓ | — | `policy_smoke_matrix.sh` |
| 6 | unknown agent deny | ✓ | — | smoke matrix |
| 7 | Enforce subprocess | ✓ | ✓ | `run_tool_guarded.py` |
| 8 | Fail-closed ACP down | ✓ | — | `fail_closed_drill.sh` |
| 9 | Gateway Docker `/acp/status` | ✓ | — | MSI `request-router` rebuild |
| 10 | Scripts on `master` | ✓ | ✓ | PR #188 `aeca32a` |

---

## 4. Commands (SSOT paths — ai-control-plane repo root)

```bash
export ACP_API_URL=http://100.94.21.33:8000
export ACP_PROJECT_ID=rust-gateway

# Smoke (all roles)
bash examples/integrate/shell/policy_smoke_matrix.sh

# Per-machine identity — NOT in git (.env gitignored)
export ACP_AGENT_ID=agent1   # MSI
export ACP_ROLE=infra
# export ACP_AGENT_ID=agent2  # Mac
# export ACP_ROLE=backend

python3 examples/integrate/python/run_tool_guarded.py --tool git_read -- git status
bash examples/integrate/shell/fail_closed_drill.sh
```

**Doc index:** [`docs/integrations/HYBRID_AI_GATEWAY.md`](../../../integrations/HYBRID_AI_GATEWAY.md)

---

## 5. Remaining (honest backlog)

| Item | Owner | Blocker |
|------|-------|---------|
| Merge `orchestrator/acp_client.py` to **Hybrid-AI-Gateway** remote | Gateway maintainer | Local MSI only |
| Antigravity **built-in** tool auto-hook | IDE / wrapper | No single hook in Gateway repo |
| `mlops-engine` kubectl pre-check | Gateway Rust PR | Follow-up |
| `verify-pilot.sh` formal tick on VPS | Operator | Ops hygiene |
| Dog-fooding case study publish | Gateway repo | Post-implementation |
| PB-9 soak 07-04..07-06 | Operator | Calendar |

---

## 6. Session mistakes & anti-patterns (audit trail)

| # | Mistake | Impact | Fix applied |
|---|---------|--------|-------------|
| M1 | Scripts first created only under `Hybrid-AI-Gateway-Clean/scripts/acp/` | MSI ran from wrong repo → `No such file` | Duplicated to `examples/integrate/` + #188 |
| M2 | Docs pointed to `scripts/acp/` without repo qualifier | Context drift across 5–6 sessions | SSOT: ACP repo `examples/integrate/` |
| M3 | Assumed `git pull` syncs `ACP_AGENT_ID` | User confusion MSI vs Mac | Documented: `.env` per-machine, gitignored |
| M4 | `evaluation_path: default_allow` looked like “no policy” | False alarm on ALLOW cases | Explained RBAC pass-through → default_allow |
| M5 | Mac `git stash pop` on PB9 log | Merge conflict | `git checkout --ours` + drop stash |
| M6 | Integration scripts not pushed before Mac test | Mac `No such file` after pull | Branch `low/integration-enforce-examples` → #188 |

**Rule for next sessions:** Integration runnable paths live in **this repo** `examples/integrate/`; Gateway repo is optional duplicate (`scripts/acp/`).

---

## 7. Sign-off

| Role | Verdict | Date |
|------|---------|------|
| Operator evidence | ACP Product A path **PASS** MSI + Mac | 2026-07-03 |
| Gateway remote | **OPEN** — merge PR on Hybrid-AI-Gateway | — |

**Do not claim:** full Gateway repo integration merged, Antigravity automatic tool gate, PB-12/Public Beta flip.
