# CLAUDE.md — AI Control Plane

**Layer:** L0 — Behavioral constitution (Karpathy 4 principles, ACP-adapted)  
**Audience:** Claude Code, Cursor, and other coding agents on this repo  
**Full stack:** [`.cursorrules`](../.cursorrules) (6-layer) · [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md)

---

## 1. Think before coding

Do not assume. Surface tradeoffs before implementation.

Before any code:
1. State files you will touch
2. List assumptions — if uncertain, ask
3. Name the verify command for success
4. If a simpler approach exists, present it first

For ABAC, policy, or auth tasks: explicitly list condition keys / behaviors you will implement vs skip. Skip without flagging = P-04 anti-pattern.

---

## 2. Simplicity first

Minimum code that solves the problem. Nothing speculative.

- No features beyond the request
- No abstractions for single-use code
- If 50 lines suffice, do not write 200
- No error handling for impossible scenarios (trust Pydantic where applicable)

**Senior engineer test:** Would a reviewer ask "why this complex?" — if yes, simplify first.

The 8 invariants in `ARCHITECTURE.md` define boundaries; inside them, prefer the simpler implementation.

---

## 3. Surgical changes

Touch only what the task requires. Every changed line traces to the request.

- Do not improve adjacent code, comments, or formatting unless asked
- Do not refactor unrelated broken code
- Match existing style (structlog, Pydantic v2, async/await)
- Dead code: mention in PR body, do not delete unless tasked

**File scope (P-02):**
- docs-only → `*.md`, `docs/**` only; need `src/` → reclassify to MEDIUM
- test-only → `tests/**`; need `src/` → MEDIUM

Remove only imports/variables **your** changes made unused.

---

## 4. Goal-driven execution

Every task needs verifiable success criteria.

| Instead of | Transform to |
|------------|--------------|
| Fix the policy bug | Test reproduces failure, then pass |
| Add ABAC condition | `test_policies.py` covers it, then implement |
| Refactor quota | All quota tests pass before and after |

**Verify gate (run in order):**

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config
```

Multi-step tasks: state plan with verify per step before step 1.

---

## ACP-specific rules

### 8 invariants (`ARCHITECTURE.md` — never violate)

1. `core/policies.py` — custom engine only; no OSS policy runtime in core
2. `core/models.py` — all data contracts here
3. `mcp/git_server.py` — facade only; no git logic in Python
4. `cli/` — HTTP/API only; no direct `core/policies` import
5. `apex/` — SAPAL loop here; OSS tools called FROM apex
6. `api/` — sole cross-language bridge
7. `core/quota.py` — QuotaStore ABC; swappable backend
8. `config/` — defaults only; runtime via `ACP_CONFIG_DIR`

### Risk classification

See [`docs/governance/CURSOR_RISK_POLICY.md`](docs/governance/CURSOR_RISK_POLICY.md):

| Level | When |
|-------|------|
| LOW | docs, tests, comments |
| MEDIUM | CLI, config, non-breaking API |
| HIGH | core/, schema, apex |
| CRITICAL | PolicyEngine, ABAC, invariants, identity |

### Forbidden (absolute)

- Push/merge `master` without human instruction
- OSS policy engines in `core/`
- Issue ranges in PR body (`Closes #52..#62`)
- Different risk levels in one PR
- Sprint DONE before all PRs on master (P-05)
- Delete `LESSONS_LEARNED.md` entries (P-11 audit trail)

### Governance memory

- Failure patterns: [`docs/governance/LESSONS_LEARNED.md`](docs/governance/LESSONS_LEARNED.md)
- Agent entry + ML5: [`AGENTS.md`](AGENTS.md) · [`L5_MATURITY_MODEL.md`](docs/governance/L5_MATURITY_MODEL.md)
- Session anchor: [`docs/prompts/SESSION_ANCHOR_TEMPLATE.md`](docs/prompts/SESSION_ANCHOR_TEMPLATE.md)
- Gold pattern GP-01: [`docs/governance/gold-patterns/GP-01-agent-session-memory.md`](docs/governance/gold-patterns/GP-01-agent-session-memory.md)
- Runtime case studies: [`docs/governance/GOVERNANCE_UX_RUNTIME.md`](docs/governance/GOVERNANCE_UX_RUNTIME.md)
- Operator evidence: [`docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md)
- Drift reconciliation: [`docs/governance/GOVERNANCE_DRIFT_RECONCILIATION.md`](docs/governance/GOVERNANCE_DRIFT_RECONCILIATION.md)

Read lessons before tasks resembling past failure patterns.

---

**Last updated:** 2026-06-25
