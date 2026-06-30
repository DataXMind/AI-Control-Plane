# ECC ↔ ACP Layer Map

**Document ID:** ACP-GOV-ECC-LAYER-001  
**Purpose:** Prevent mixing harness artifacts with policy control plane  
**SSOT:** [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md)

---

## Two systems

| | **ECC (external harness)** | **ACP (this repo)** |
|--|---------------------------|---------------------|
| Question | *How should the agent work?* | *Is this action allowed?* |
| Examples | Skills, hooks, MCP connectors | `/policy/evaluate`, `agents.yml` |

---

## ECC 5-layer ↔ Karpathy 6-layer

| ECC surface | Role | ACP Karpathy layer | ACP artifact |
|-------------|------|-------------------|--------------|
| **Rules** | Always-on principles | L0–L2 | `.cursorrules`, `CLAUDE.md`, `CURSOR_RISK_POLICY.md` |
| **Skills** | Reusable workflows | L3–L4 | `docs/prompts/`, PACE, smoke scripts |
| **Hooks** | Hard enforcement events | L3–L4 | CI gates, pre-commit, smoke 8/8 |
| **Agents** | Scoped sub-delegation | L3 | Cursor Task / `AGENTS.md` delegation |
| **MCP** | External tool transport | L2 boundary | `MCP_INTEGRATION_CONTRACT.md` → policy API |

**Do not:** Put policy rules only in harness rules — runtime truth is `config/policies.yml` + API.

---

## Decision quick table

| I need… | Use |
|---------|-----|
| Deny unknown agent on tool call | ACP `POST /policy/evaluate` |
| Branch isolation / PR size | ACP P-01, `CURSOR_RISK_POLICY.md` |
| Session baseline / PB gates | `SESSION_ANCHOR_TEMPLATE.md` |
| Slash command workflow | ECC-style **skill** or `docs/prompts/` — not policy engine |
| Block bad git push | Harness **hook** + human review — plus ACP if agent action |

---

**Last updated:** 2026-06-30 · 48H Phase 3
