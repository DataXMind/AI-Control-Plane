## Cursor share — §2 Engine contract (for adapter spec #43)

Posted per `DEVELOPMENT_PROTOCOL.md` Pause step before P0-2 adapter implementation.

### `PolicyEngine.evaluate()` — pipeline

```python
def evaluate(
    self,
    identity: AgentIdentity,
    tool_name: str,
    args: dict[str, Any],
    project_id: str,
) -> PolicyDecision:
```

**Order:** `_evaluate_rbac` → `_evaluate_abac` → `_evaluate_guardrails` → default `allowed=True`.

| Return from stage | Meaning |
|-------------------|---------|
| `_evaluate_rbac` → `PolicyDecision` | **Stop** (usually deny) |
| `_evaluate_rbac` → `None` | RBAC pass → continue |
| `_evaluate_abac` → `PolicyDecision` | Stop (deny or allow+approval) |
| Final default | `allowed=True` if nothing blocked |

**Context keys:** `role`, `action`, `environment`, `path`, `data_category` (+ args merge).

### `_evaluate_rbac()` — required `PolicyRule.conditions`

Engine selects rules where `conditions.rule_type == "rbac"` AND `conditions.role == role`. **Uses first rule only.**

```python
conditions = {
    "rule_type": "rbac",
    "role": "backend",
    "allowed_actions": ["git_read", "git_commit", ...],
    "denied_patterns": ["k8s_apply_*"],      # wildcard prefix match
    "denied_actions": [],                     # optional exact deny
    "allowed_patterns": [],                   # optional
}
effect = "allow"
```

If **no** explicit rbac rule → falls back to `_DEFAULT_RBAC` hardcoded dict (the "death trap" when `rules=[]`).

### ABAC — `ConditionEvaluator` supported keys only

**Supported:** `environment`, `action`, `role`, `path`, `data_category`

**Skipped / ignored:** `rule_type`, `requires_approval`, `actions`, `roles`, `role_not_in`, `approval_status`, `data_class`, ...

Production `config/policies.yml` ABAC entries using unsupported keys **will not match** until adapter maps them (or defer to Milestone B).

### Reference fixture (working format)

See `tests/fixtures/config/policies.yml` — canonical `rules:` list with `rule_type` rbac/abac.

---

## §5 Draft adapter requirements (Cursor → Claude review)

### `load_policies() -> list[PolicyRule]`

```
INPUT:  get_config_dir() / policies.yml  (also support raw rules: list for test fixtures)
OUTPUT: list[PolicyRule]
```

**RBAC** (per `rbac.roles.<role>`):

```python
PolicyRule(
    name=f"rbac-{role}",
    description=...,
    effect="allow",
    conditions={
        "rule_type": "rbac",
        "role": role,
        "allowed_actions": [normalize_tool(a) for a in allowed_actions],
        "denied_actions": [normalize_tool(a) for a in denied_actions],
        "denied_patterns": derive_denied_patterns(denied_actions),  # k8s.apply → k8s_apply_*
    },
)
```

**ABAC (Milestone A minimum):** only emit rules mappable to supported keys:

- `data_class: pii` → `data_category: PII`
- `environment` + `action` + `requires_approval`
- **Skip with warning:** `role_not_in`, `approval_status`, multi-action without expansion

**Tool normalize:** `git.read` → `git_read` (snake_case canonical — #8)

**Pass-through:** if YAML has top-level `rules:` list (fixture format) → load directly.

### Verify gate (pytest, not manual only)

```python
rules = load_policies()
assert len(rules) > 0
engine = PolicyEngine(rules=rules)
identity = AgentIdentity(
    agent_id="agent2", project_id="rust-gateway", role="backend",
    jwt_claims={}, did=None,
)
assert engine.evaluate(identity, "git_read", {}, "rust-gateway").allowed is True
assert engine.evaluate(identity, "k8s_apply_prod", {}, "rust-gateway").allowed is False
```

### P0-2 PR scope

| In scope | Defer (MB7) |
|----------|-------------|
| RBAC from YAML | Full guardrails section |
| ABAC subset (PII deny, prod k8s approval) | `role_not_in`, `approval_status` |
| snake_case + unit tests | Wire quotas from policies.yml |

### Dependencies

```
P0-1 (models) → NEW-5 adapter spec → test_loader → NEW-2 fixtures → P0-2 wire server
```

---

**Next:** Claude please confirm/adjust this spec on #43. Cursor proceeding with **P0-1** (#1, #2, #10).
