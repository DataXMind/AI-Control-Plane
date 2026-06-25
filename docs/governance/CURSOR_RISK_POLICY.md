# Cursor Risk Policy (L2)

**Document ID:** ACP-GOV-CURSOR-RISK-001  
**Layer:** L2 — Risk Policy (agent-as-developer governance)  
**Authority:** Subordinate to `ARCHITECTURE.md` invariants; supersedes flat `.cursorrules` on conflict  
**Parent:** [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md)  
**Not to confuse with:** `config/policies.yml` — that governs **runtime agents**, not Cursor sessions.

---

## Purpose

Classify every Cursor task **before** coding. Prevents monolithic PRs, scope creep in doc-only PRs, and silent assumption drift documented in [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md).

**Priority stack:** L0 behavior > L1 context > **L2 risk** > L3 guardrails > L4 evaluation > L5 memory.

---

## Risk levels

| Level | Task examples | Pre-work | LOC limit (net diff) | Approval |
|-------|---------------|----------|----------------------|----------|
| **LOW** | `*.md`, `docs/**`, comment-only, test assertion fixes | State verify command | ≤ 50 | None — proceed |
| **MEDIUM** | New tests, CLI subcommands, `config/*.yml`, `api/schemas` non-breaking | Plan + file allowlist | ≤ 200 | Self-check plan |
| **HIGH** | `core/**`, new API endpoints, loader/schema changes, `apex/**` | Claude arch review **before** code | ≤ 300 | Human or Claude spec in prompt |
| **CRITICAL** | `core/policies.py`, ABAC/PolicyEngine, identity/JWT, invariant edits | Human explicit approve + Claude spec | ≤ 300 | Human must approve start |

**Waivers:** Path B monolithic PRs (#48, #63) were **one-time** exceptions — documented in `PHASE2_SPRINT1_CONSOLIDATED_AUDIT_FINAL.md`. **No new waivers** without human + entry in `LESSONS_LEARNED.md`.

---

## Forbidden operations (absolute)

1. Direct push or merge to `master` without human instruction.
2. Remove, rename, or weaken any of the **8 invariants** (`ARCHITECTURE.md`).
3. Import OSS policy engines (CrewAI, LangChain, etc.) into `core/`.
4. Combine tasks of **different risk levels** in one PR.
5. Commit without running the verify gate (`DEVELOPMENT_PROTOCOL.md` §5.5).
6. `Closes #52..#62` range syntax — use **individual** `Closes #53`, `Closes #54`, …
7. Doc-only PR touching `src/**` (scope creep — stop and reclassify).
8. Mark sprint DONE before all sprint PRs are merged to `master` (P-05).
9. Skip "state assumptions" for ABAC/policy/loader changes without documenting GAP (P-04).
10. Delete or archive entries in `LESSONS_LEARNED.md` (audit trail — P-11).
11. `core/` modules importing from `mcp/` or `cli/` (dependency direction).

---

## PR body template (mandatory for master)

```markdown
Risk level: [LOW / MEDIUM / HIGH / CRITICAL]

Files touched:
- [path] — [why]

Assumptions made:
- [assumption]
(or: No assumptions — task fully specified)

Scope reductions (if any):
- [item] → [milestone] because [reason]
(or: N/A)

Closes #N
Closes #M
(individual lines — no ranges)

Verify gate passed:
- [ ] ruff check src/ tests/
- [ ] mypy src/ai_control_plane/ --strict
- [ ] pytest tests/ -v
- [ ] pytest tests/test_smoke.py -v -m smoke
- [ ] pytest tests/test_shipped_config_parity.py -v -m shipped_config (if HIGH+)
```

---

## Waiver process

Waivers require human + documented entry in [`LESSONS_LEARNED.md`](LESSONS_LEARNED.md).  
PR body must include: `Waiver: [rule] because [reason], approved [date]`.  
Same waiver type not granted twice per milestone without new lesson row.

---

## File allowlists (L3 — enforce with risk level)

| Task type | Allowed paths | Forbidden |
|-----------|---------------|-----------|
| **docs-only** | `*.md`, `docs/**`, `CHANGELOG.md` | `src/**`, `tests/**` |
| **test-only** | `tests/**`, `tests/fixtures/**` | `src/**` (if needed → MEDIUM) |
| **core/** | `src/ai_control_plane/core/**`, `tests/test_{module}.py` | `api/**`, `mcp/**`, `cli/**` unless in scope |
| **api/** | `src/ai_control_plane/api/**`, related tests | `core/policies.py` without CRITICAL path |

---

## Module ownership (review triggers)

| Module | Default risk | Reviewer |
|--------|--------------|----------|
| `core/policies.py` | CRITICAL | Claude arch + human |
| `core/models.py` | HIGH | Claude arch |
| `config/loader.py` | HIGH | Claude arch |
| `api/server.py` | MEDIUM | Invariant checklist |
| `apex/**` | HIGH | Claude design spec first |
| `mcp/**` | MEDIUM | Invariant #3 |
| `tests/**`, `docs/**` | LOW | Self |

---

## PR hygiene

- Branch: `{risk}/{issue-id}-{short-desc}` (e.g. `low/pb7-readme-fork-verify`).
- PR body: risk level, assumptions, verify commands, individual `Closes #N`.
- HIGH/CRITICAL: diff summary comment — what changed and why per invariant.

---

## Verify gate (mandatory — L4)

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
pytest tests/test_shipped_config_parity.py -v -m shipped_config
```

Current baseline: **165** pytest, smoke **8/8** (not 156 — pre-R1 HTML artifact stale).

---

**Reconciliation:** [`GOVERNANCE_DRIFT_RECONCILIATION.md`](GOVERNANCE_DRIFT_RECONCILIATION.md)  
**Last updated:** 2026-06-25 @ post Studies 01–07
