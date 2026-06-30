# ECC × ACP Integration Analysis — 48H SSOT

**Document ID:** ACP-GOV-ECC-48H-001  
**Plan:** 48H · 5 phases · baseline `master` @ `da7bf12`  
**External reference:** [affaan-m/ECC](https://github.com/affaan-m/everything-claude-code) v2.0 (harness OS)  
**Internal analyst source:** `ECC Analysts/repo ECC Analysts.md` (Exa research, 2026-06)

---

## 1. Relationship (do not conflate)

| | **ECC** | **ACP (this repo)** |
|--|---------|---------------------|
| Role | Agent harness OS (skills, hooks, rules, MCP surface) | Policy engine + Karpathy 6-layer governance |
| Runtime | IDE / multi-harness local | `POST /policy/evaluate` · YAML policy |
| Moat | Context budget, skill library | Fail-closed ABAC + practice evidence + catalog UX |

```text
Agent session → ECC (how to work) ──tool intent──► ACP (allow/deny) ──► resources
```

**48H rule:** Adopt **ideas and docs** only. **No** ECC plugin install, no skill/agent copy.

---

## 2. ADOPT → ACP artifact (this 48H)

| ID | ECC concept | ACP deliverable | Phase |
|----|-------------|-----------------|-------|
| A1 | MCP connector minimalism | `MCP_INTEGRATION_CONTRACT.md` §Decision matrix | 2 |
| A2 | Least agency / lethal trifecta | `THREAT_MODEL.md` §6; `PRODUCT_POSITIONING.md` | 2 |
| A3 | Official sources / supply chain | `SECURITY.md` §Harness artifacts | 2 |
| A4 | pass@k vs pass^k | `EVAL_METHODOLOGY.md` | 3 |
| A5 | Skill / hook / rule separation | `ECC_ACP_LAYER_MAP.md` | 3 |
| A6 | Iterative retrieval (subagent) | `AGENTS.md`; `DEVELOPMENT_PROTOCOL.md` | 4 |
| A7 | Session adapter (compare only) | `ACP_SESSION_CONTRACT_v1.md` | 4 |
| A8 | MCP context tax | P-17 + catalog v1.5.0 | 5 |

---

## 3. ADAPT (pattern only, no ECC code)

| ECC artifact | ACP adaptation |
|--------------|----------------|
| `ecc.session.v1` | Compare in `ACP_SESSION_CONTRACT_v1` — keep `SESSION_ANCHOR_TEMPLATE` for PB gates |
| MCP inventory / secret redaction | Defer Study 09 post-flip; cite in P-17 |
| Worktree-lifecycle | Existing P-01 + `split-to-prs` skill — no ECC Rust tooling |
| Stop-hook continuous learning | GP-01 ML5 + LESSONS — no ECC instinct/evolve import |
| AgentShield | Defer v0.2.x; self-audit checklist in Study 09 plan |

---

## 4. REJECT (48H and 0.x)

| Item | Reason |
|------|--------|
| Install ECC plugin / 261 skills / 64 agents | P-02 scope creep; wrong product identity |
| Hermes, control-pane TUI, Discord bot | Separate operator product |
| ECC Rust “control-plane” alpha | Name collision with AI Control Plane |
| Model routing tables (Haiku/Sonnet/Opus) | Harness billing — not ACP SSOT |
| kubernetes-patterns skill pack | Out of scope 0.x |
| ECC Pro commercial features | `BUSINESS_MODEL.md` path differs |

**Quyết định này là FINAL cho 0.x** — xem [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md) §Drift guard.

---

## 5. DEFER (post PB-12)

- Study 09 harness/MCP config audit  
- Optional `ecc-agentshield` npm (official sources only)  
- k6 load test pass^k closure (P-15)  
- Cross-harness session adapter implementation  

---

## 6. 48H enforcement

| Rule | Detail |
|------|--------|
| Window | T0 → T+48h — all phase PRs merged or plan FAIL |
| PR | 1 task = 1 branch = 1 PR |
| Track | Docs-only except Phase 5 catalog (`governance_catalog.py`) |
| Smoke | 8/8 every PR |
| Version bump | **Only** Phase 5 → v1.5.0 (P-17 MINOR) |
| PB-9 | No soak machine lines in ECC PRs |

**Results SSOT:** [`ECC_48H_RESULTS.md`](ECC_48H_RESULTS.md) (Phase 5 closeout).

---

## 7. Value alignment (`VALUE_AUDIT_MATRIX`)

| ACP moat | ECC strengthens via |
|----------|---------------------|
| Fail-closed policy | Least agency narrative (A2) |
| 16 LESSONS + PACE | P-17 MCP context tax (A8) |
| Governance catalog | DOC_LINKS + EVAL metrics (A4) |
| Practice evidence | Deferred Study 09 — not blocking 48H |

---

**Last updated:** 2026-06-30 · 48H complete · Catalog v1.5.0
