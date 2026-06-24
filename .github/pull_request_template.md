## Risk level

- [ ] **LOW** — docs/comments only (≤50 LOC)
- [ ] **MEDIUM** — tests, CLI, config (≤200 LOC)
- [ ] **HIGH** — core/, API schema, new endpoints (≤300 LOC)
- [ ] **CRITICAL** — PolicyEngine, ABAC, invariants (human approved)

Policy: [`docs/governance/CURSOR_RISK_POLICY.md`](../docs/governance/CURSOR_RISK_POLICY.md)

## Assumptions

- Files touched:
- Assumptions made:
- Verify commands run:

## Summary

<!-- What and why -->

## Issues

<!-- Individual Closes #N — NO ranges like Closes #52..#62 -->

## Test plan

- [ ] `ruff check src/ tests/`
- [ ] `mypy src/ai_control_plane/ --strict`
- [ ] `pytest tests/ -v`
- [ ] `pytest tests/test_smoke.py -v -m smoke`
- [ ] `pytest tests/test_shipped_config_parity.py -v -m shipped_config`
