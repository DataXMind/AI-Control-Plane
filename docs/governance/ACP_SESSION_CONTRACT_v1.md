# ACP Session Contract v1 — Compare Only

**Document ID:** ACP-GOV-SESSION-001  
**Status:** **Specification compare** — no runtime implementation in 0.x  
**SSOT for operators:** [`SESSION_ANCHOR_TEMPLATE.md`](../prompts/SESSION_ANCHOR_TEMPLATE.md) (PB gates, PACE verify)  
**Related:** [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md) A7 · [`ECC_ACP_LAYER_MAP.md`](ECC_ACP_LAYER_MAP.md)

---

## Purpose

Document how an external harness session envelope (`ecc.session.v1`) relates to ACP's existing session anchor — **without** replacing PB-9/PB-12 gate fields or importing ECC code.

---

## Two session models

| Field | **ACP `SESSION_ANCHOR_TEMPLATE`** | **ECC `ecc.session.v1` (external)** |
|-------|-----------------------------------|-------------------------------------|
| Owner | ACP maintainers | ECC harness OS |
| Primary use | PB gates, catalog baseline, PACE verify | Cross-harness resume, context budget |
| Durable tier | Tier C (`practice-evidence/`, soak logs) | Harness session store / adapter |
| Policy truth | `POST /policy/evaluate` | Not policy — workflow state only |
| Required at session start | Yes (Cursor/Claude on this repo) | Optional (ECC plugin users) |

**Rule:** PB-12 blockers and `gates_approved` live **only** in the ACP anchor — never inferred from ECC session JSON.

---

## Conceptual field map (compare, not merge)

| ECC-style concept | ACP equivalent | Notes |
|-------------------|----------------|-------|
| `baseline_commit` | Anchor one-liner SHA | Same intent |
| `gates_approved[]` | Anchor `gates_approved` | ACP SSOT for G1+ |
| `risk_tier` | `CURSOR_RISK_POLICY` classification | State in anchor before Act |
| `file_allowlist` | Risk policy allowlist | HIGH+ tasks |
| `context_budget` | N/A in anchor | Defer to harness; cite P-17 at flip |
| `mcp_connectors[]` | `MCP_INTEGRATION_CONTRACT.md` | 0–1 default; inventory Study 09 |
| `resume_token` | Chat summary ≠ durable memory | Write Tier C, not chat alone |

---

## When to use which

| Situation | Use |
|-----------|-----|
| Work on **this repo** (ACP) | `SESSION_ANCHOR_TEMPLATE.md` every session |
| Compare harness portability | This doc + A1 analysis |
| Implement cross-harness adapter | **Defer** post PB-12 (§5 ECC analysis) |
| Policy allow/deny on tool call | ACP API only |

---

## Non-goals (0.x)

- No `ecc.session.v1` parser in `src/`
- No ECC plugin dependency
- No duplicate anchor template — pointer only

---

**Last updated:** 2026-06-30 · Catalog v1.5.0
