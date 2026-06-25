# AGENTS.md — AI Control Plane

**Purpose:** Single entry point for **all coding agents** (Cursor, Claude Code, Copilot, etc.) on this repo.  
**Framework:** 6-layer Karpathy governance · **Memory target:** [Maturity Level 5](docs/governance/L5_MATURITY_MODEL.md)  
**Companion:** [`.cursorrules`](.cursorrules) (L0–L5) · [`CLAUDE.md`](CLAUDE.md) (L0 summary)

---

## Start every session (mandatory)

1. **Anchor** — copy [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md), fill baseline commit, risk, gates, allowlist.
2. **Read SSOT** — `ARCHITECTURE.md` before non-trivial code; [`CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) before any patch.
3. **Runtime check** (when API up):

```bash
export ACP_API_URL=http://localhost:8000
agentctl gov status
```

4. **Scoped rules** — Cursor loads [`.cursor/rules/`](.cursor/rules/) by file context; do not fight higher layers.
5. **Governance phase work** — `@docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md` and state **approved gates** (A/B/C/D/E) before G1+ execution. No gate in anchor = planning only.

---

## Approval gates (G1+ / PB-12)

**SSOT:** [`GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md`](docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md) §11

| Gate | Maintainer says | Agent may |
|------|-----------------|-----------|
| **A** | Approve G1 execution | DEVELOPMENT_PROTOCOL Evolve, G1-4 addendum |
| **B** | Approve G2-{ids} | Named practice studies only |
| **C** | Approve meta-drift PR | Reconciliation §1 refresh, Karpathy §3.3 |
| **D** | PB-9 backfill + continue | Remind operator; **do not** tick soak log without human |
| **E** | PB-12 go | CRITICAL — all §8 blockers clear |

**New session rule:** Paste anchor with `gates_approved: ["A"]` (example) — not verbal chat alone.

---

## PB-9 soak (operator only)

- **Only** durable updates go to [`PB9_STAGING_SOAK_LOG.md`](docs/governance/PB9_STAGING_SOAK_LOG.md).
- Chat message from operator: *"đã tick ngày YYYY-MM-DD"* → agent may edit that row only.
- Agent **must not** invent soak results or tick days without explicit operator message.

---

## SSOT hierarchy (conflict resolution)

```text
code + ARCHITECTURE.md
  > practice-evidence/*/RESULTS.md + PRACTICE_STUDIES_AUDIT_01-07.md
  > GOVERNANCE_UX_RUNTIME.md (CS-01..06)
  > GOVERNANCE_DRIFT_RECONCILIATION.md
  > HTML governance artifacts (HISTORICAL)
```

---

## 6-layer map (where to look)

| Layer | Authority | Agent action |
|-------|-----------|--------------|
| **L0** | `.cursorrules`, `CLAUDE.md` | State assumptions before code; simplicity; surgical diff |
| **L1** | `ARCHITECTURE.md`, `DATA_CLASSIFICATION.md` | Module ownership; 8 invariants |
| **L2** | `CURSOR_RISK_POLICY.md` | Classify LOW/MED/HIGH/CRITICAL; file allowlist |
| **L3** | `.cursorrules` §L3, `CONTRIBUTING.md` | Branch naming; no `src/` in docs-only PR |
| **L4** | CI, `DEVELOPMENT_PROTOCOL.md` §5.5 | Verify gate before done |
| **L5** | `LESSONS_LEARNED.md`, plans, practice-evidence | Update after sprint close; never delete patterns |

---

## Memory tiers (L5 — do not rely on chat)

| Tier | What | When |
|------|------|------|
| **A — Auto** | `.cursorrules`, `.cursor/rules/`, user rules | Every session |
| **B — Session** | Session anchor + `@` files + issue/PR link | Every task |
| **C — Durable** | `LESSONS_LEARNED.md`, `practice-evidence/`, phase plans | Sprint close / operator runs |

Chat history is **not** durable memory. Write decisions to Tier C.

---

## Task packets & gold patterns

| Resource | Use |
|----------|-----|
| [`docs/prompts/_TEMPLATE.md`](docs/prompts/_TEMPLATE.md) | New Claude/Cursor task packets |
| [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md) | Open every Cursor session |
| [`docs/governance/gold-patterns/GP-01-agent-session-memory.md`](docs/governance/gold-patterns/GP-01-agent-session-memory.md) | **Public export** — adopt in any repo |

---

## Forbidden (absolute)

- Push/merge `master` without human instruction
- Weaken `ARCHITECTURE.md` invariants
- `Closes #52..#62` issue ranges in PR body
- Mix risk levels in one PR
- Delete `LESSONS_LEARNED.md` entries
- Claim CS-01/03/04 or PB-9 PASS without evidence (see practice audit)

---

## Verify before PR

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
bash scripts/verify_governance_memory.sh
```

---

**Last updated:** 2026-06-25 · ML5 memory pack
