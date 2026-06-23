# Milestone B — Backlog (governance)

> **Status:** ACTIVE backlog after Milestone A close (#38)  
> **Source:** Phase 1 v2 re-audit + `scripts/create_milestone_a_issues.sh` MB7  
> **Tracking:** [GitHub Issues](https://github.com/DataXMind/AI-Control-Plane/issues) label `milestone-b`

---

## MB7 — Guardrails + kill_switch from policies.yml

**Priority:** P1 (governance completeness)

**Problem:** Shipped `config/policies.yml` defines `guardrails:` and `kill_switch:` but `config/loader.load_policies()` does not load them. `PolicyEngine._evaluate_guardrails()` exists but receives no `rule_type: guardrail` rules from YAML in Milestone A.

**Acceptance criteria (Milestone B):**

- [ ] `_load_guardrails(raw)` maps `guardrails[].applies_to` → `PolicyRule` with `rule_type: guardrail`, `check`, `actions`, `roles`
- [ ] `kill_switch.enabled` → global deny at policy eval (or documented HTTP 503 path)
- [ ] `tests/test_loader.py` + `tests/test_policies.py` cover plan_required, tests_passed, branch_allowed from YAML
- [ ] `ARCHITECTURE.md` table updated — guardrails row → ✅
- [ ] SMK-01..05 still pass

**Non-goals:** Redis persistence, MCP HTTP transport.

**Dependencies:** P0-2 ingress normalize (✅ Phase 1 v2).

---

## Related Milestone B items (existing issues #29–37)

| Area | Issue theme |
|------|-------------|
| Persistence | Redis quota, task store (#29–31) |
| CLI live | `approve`, `quota`, `logs` subcommands |
| Identity | JWT validation, SMK-06 |
| ABAC full | `approval_status`, `role_not_in`, `read_only` conditions |
| Quotas | `by_model_profile`, `by_agent` enforcement |
| MCP | HTTP transport |

---

## How to open on GitHub

```bash
gh issue create --repo DataXMind/AI-Control-Plane \
  --title "MB7: Load guardrails and kill_switch from policies.yml" \
  --label "milestone-b,spec-gap" \
  --body "See docs/governance/MILESTONE_B_BACKLOG.md § MB7"
```

---

**Last updated:** 2026-06-23 (Phase 1 v2 execution)
