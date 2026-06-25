# CLAUDE.md — AI Control Plane

**Behavioral constitution** for AI coding agents on this repo.  
**Derived from:** Andrej Karpathy's observations on LLM coding pitfalls (adapted for ACP).  
**Layer:** L0 — companion to [`.cursorrules`](.cursorrules) (6-layer stack)  
**Audience:** Claude Code, Cursor, and other coding agents  
**Full governance:** [`.cursorrules`](.cursorrules) · [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`AGENTS.md`](AGENTS.md) (ML5 entry)

---

## 1. Think before coding

Don't assume. Don't hide confusion. Surface tradeoffs before implementation.

Before any code:

1. State explicitly which files you will touch
2. List assumptions you are making — if uncertain, ask
3. Name the verify command that confirms success
4. If a simpler approach exists, present it before the complex one

For ABAC, policy, or authentication tasks: explicitly list condition keys / behaviors you will implement vs skip. Skip without flagging = silent assumption (**P-04** anti-pattern).

---

## 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond what was asked
- No abstractions for single-use code in this repo
- If 50 lines suffice, do not write 200
- No error handling for impossible scenarios (trust Pydantic validation)

**Senior engineer test:** Would a reviewer ask "why this complex?" — if yes, simplify before submit.

The **8 invariants** in `ARCHITECTURE.md` define boundaries; inside them, always prefer the simpler implementation.

---

## 3. Surgical changes

Touch only what you must. Every changed line traces to the request.

- Do **not** improve adjacent code, comments, or formatting unless asked
- Do **not** refactor code that your task did not break
- Match existing style (structlog, Pydantic v2, async/await)
- Dead code you notice → mention in PR body; do **not** delete unless the task includes cleanup

**File scope discipline (P-02):**

- docs-only task → `*.md` and `docs/**` only; need `src/` → stop and reclassify (MEDIUM)
- test-only task → `tests/**` only; need `src/` → MEDIUM, not LOW

After changes: remove only imports/variables **your** changes made unused. Pre-existing dead code stays unless cleanup is explicitly in scope.

---

## 4. Goal-driven execution

Define success criteria. Loop until verified.

| Instead of | Transform to |
|------------|--------------|
| Fix the policy bug | Write test reproducing failure, then make it pass |
| Add ABAC condition | `test_policies.py` covers new condition, then implement |
| Refactor quota logic | All existing quota tests pass before and after |

**ACP verify gate (run in this order):**

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config   # HIGH+ / config touch
```

Multi-step tasks: state plan with verify per step **before** executing step 1.

---

## ACP-specific rules

### 8 invariants (`ARCHITECTURE.md` — never violate)

1. `core/policies.py` — custom engine only; no OSS policy runtime replacement
2. `core/models.py` — all data contracts here, nowhere else
3. `mcp/git_server.py` — facade only; no Git logic in Python
4. `cli/` — HTTP/API calls only; no direct `core/policies` imports
5. `apex/` — SAPAL loop here; OSS tools called **from** apex/, not the reverse
6. `api/` — sole cross-language bridge to TypeScript
7. `core/quota.py` — `QuotaStore` ABC; swappable backend
8. `config/` — shipped defaults only; runtime path via `ACP_CONFIG_DIR`

### Risk classification

See [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) (full L2: F1–F11, per-level verify):

| Level | When |
|-------|------|
| **LOW** | docs-only; **test-only** with no `src/` in diff |
| **MEDIUM** | CLI, config, non-breaking API; tests **paired with** `src/` |
| **HIGH** | `core/`, schema, `apex/` design — Claude review **before** code |
| **CRITICAL** | PolicyEngine, ABAC, invariants, identity — **human approve** first |

### Forbidden (absolute)

- Push/merge `master` without human instruction
- Import OSS policy engines into `core/`
- Issue ranges in PR body (`Closes #52..#62`) — use individual `Closes #N` (P-03)
- Combine different risk levels in one PR (F4)
- Mark sprint DONE before all sprint PRs on `master` (P-05 / F7)
- Skip "state assumptions" for ABAC/policy/loader work (P-04 / F8)
- Delete or archive `LESSONS_LEARNED.md` entries (P-11 / F9)

### Governance memory (L5 — do not rely on chat)

Read [`docs/governance/LESSONS_LEARNED.md`](docs/governance/LESSONS_LEARNED.md) before tasks resembling past failure patterns.

| Resource | Use |
|----------|-----|
| [`AGENTS.md`](AGENTS.md) | Agent entry, approval gates, PB-9 soak rule |
| [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md) | Open every session (Tier B memory) |
| [`docs/governance/L5_MATURITY_MODEL.md`](docs/governance/L5_MATURITY_MODEL.md) | ML0–ML5 memory maturity |
| [`docs/governance/gold-patterns/GP-01-agent-session-memory.md`](docs/governance/gold-patterns/GP-01-agent-session-memory.md) | Public export pattern |
| [`docs/governance/GOVERNANCE_UX_RUNTIME.md`](docs/governance/GOVERNANCE_UX_RUNTIME.md) | CS-01..06 runtime catalog |
| [`docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md) | Operator evidence — do not over-claim |
| [`docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md`](docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md) | Gate A/C before G1+ execution |

---

**Last updated:** 2026-06-25 @ L0 alignment with Karpathy prompt + ML5 #91 + L2 F1–F11
