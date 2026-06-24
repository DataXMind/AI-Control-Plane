# Cursor prompt template v2 (6-layer)

**Use for:** All new `docs/prompts/CLAUDE_PROMPT_*.md` packets after Phase R1.  
**Policy:** [`CURSOR_RISK_POLICY.md`](../governance/CURSOR_RISK_POLICY.md) · **Plan:** [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](../governance/ACP_KARPATHY_REARCHITECTURE_PLAN.md)

---

## Risk: [LOW | MEDIUM | HIGH | CRITICAL]

## File allowlist

- Allowed:
- Forbidden:

## Assumptions (Cursor must fill before any code)

1. Files I will touch:
2. Assumptions I am making:
3. If wrong, I will stop and ask:

## Task

[Description]

## Acceptance criteria

- [ ]

## Verify

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -v
pytest tests/test_smoke.py -v -m smoke
# Add task-specific tests below
```

## PR body checklist

- [ ] Risk level stated
- [ ] Individual `Closes #N` (no ranges)
- [ ] Verify commands run green
