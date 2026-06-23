# Claude Task Packet — Config Tool Naming Policy (P0-2b, #8, D3)

> **Status:** CLOSED — Option A (2026-06-23, Phase 2 P2-0). Implementation: `core/tool_names.py`.

## Context

AI Control Plane uses a **dual notation** for tool/action names:

| Layer | Convention | Example |
|-------|------------|---------|
| Shipped `config/*.yml` | dot notation (human-authored) | `git.read`, `k8s.apply` |
| `PolicyEngine` / tests / MCP | snake_case canonical | `git_read`, `k8s_apply_prod` |
| Adapter | `config/loader.normalize_tool_name()` at load time | `git.read` → `git_read` |

**Current state (Milestone A + Phase 1 v2):**

- `resolve_policy_tool_name()` at API ingress and MCP policy gate — dot notation and MCP aliases work at runtime.
- Shipped `config/policies.yml` still uses **dot notation** in YAML source (architect decision pending).
- Issue **#8 (P0-2b)** and **D3**: standardize whether to migrate shipped files or document adapter-only permanently.

## Goal

Produce an **architecture decision** and (if approved) a **Cursor execution packet** for one of:

1. **Option A — Adapter-only (document):** Keep shipped YAML dot notation; document as intentional human-facing format; engine stays snake_case.
2. **Option B — Migrate shipped config:** Rewrite `config/policies.yml`, `config/agents.yml` model `allowed_tasks`, and `tests/fixtures/config` to snake_case; simplify or narrow `normalize_tool_name()` scope.
3. **Option C — Hybrid:** Shipped config snake_case for `allowed_actions` only; keep dot notation in docs/examples with code generation.

## Non-goals

- Do not change `PolicyEngine` evaluation logic or fail-closed semantics.
- Do not rename MCP tool names (`git_status`, etc.) — those are a separate namespace.
- Do not touch Milestone B (Redis, persistence).

## Invariants (must hold after any change)

1. `core/policies.py` — custom engine unchanged in behavior.
2. `normalize_tool_name()` must remain idempotent for snake_case input.
3. SMK-01..05 must pass without weakening assertions.
4. Fixture `tests/fixtures/config` must stay aligned with production schema (NEW-2).

## Questions for architect

1. Which option (A/B/C) for **public beta** and **fork ergonomics**?
2. If Option B: single PR or split (policies → agents → docs)?
3. Should `model_profiles.allowed_tasks` use dot or snake_case?
4. Backward compatibility: accept both notations in loader during transition period?
5. Update `ARCHITECTURE.md` tool naming section — exact wording?

## Acceptance criteria (after Cursor execution)

- [ ] Decision recorded in `ARCHITECTURE.md` § Tool naming
- [ ] If migrate: `config/` + fixtures updated; `pytest tests/` green; smoke pass
- [ ] If document-only: `docs/DEVELOPMENT_PROTOCOL.md` trap table updated; #8 closed as wont-fix with rationale
- [ ] No regression in `test_policies.py`, `test_loader.py`, `test_mcp_git_server.py`

## Files likely touched

| File | Change |
|------|--------|
| `config/policies.yml` | dot → snake (Option B) |
| `config/agents.yml` | `allowed_tasks` notation |
| `tests/fixtures/config/*` | mirror shipped |
| `config/loader.py` | adapter rules / deprecation warnings |
| `ARCHITECTURE.md` | decision + convention table |
| `docs/DEVELOPMENT_PROTOCOL.md` | P0-2b status |

## Verify gate

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
```

## Output requested from Claude

1. **Verdict:** A, B, or C with 2–3 sentence rationale.
2. **Cursor prompt** (if B/C): step-by-step patch order, traps, test expectations.
3. **Issue comment text** for GitHub #8 and D3 to close or re-scope.

## References

- `ARCHITECTURE.md` — Tool naming convention
- `docs/DEVELOPMENT_PROTOCOL.md` §4 P0-2b row
- `tests/test_loader.py` — `normalize_tool_name` tests
- Issue #8, D3 in `scripts/create_milestone_a_issues.sh`
