# Study 01 — Terminal 2 (client / gates)

**Role:** Profile A — curl, agentctl, pytest  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study01/terminal2.md`

---

## Environment

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_API_URL=http://localhost:8000
export ACP_CONFIG_DIR=tests/fixtures/config   # for pytest only
```

---

## A1 — Health

```json
{
  "status": "ok",
  "config_loaded": true,
  "policy_rules_count": 8,
  "agents_loaded": ["agent1", "agent2", "agent3"],
  "projects_loaded": ["rust-gateway"],
  "model_profiles_loaded": [
    "claude-pro-backend",
    "claude-team-infra",
    "claude-team-review"
  ]
}
```

---

## A2 — Governance UX

**CLI (`agentctl gov status`):**

- Framework: `6-layer-karpathy` (v1.0)
- Policy rules: **8**
- Public Beta: PB-9 staging soak (#77-#80)
- Case studies: CS-01 through CS-06 listed

**API (`GET /governance/status`):** `policy_rules_count: 8`, milestones all CLOSED except `public_beta: IN_PROGRESS`

---

## A3 — Policy allow

```json
{
  "allowed": true,
  "reason": "action permitted",
  "requires_approval": false,
  "policy_id": null,
  "latency_ms": 0.57
}
```

Request: `agent2`, `rust-gateway`, `git_read`, role `backend`

---

## A4 — Policy deny (CS-06)

```json
{
  "allowed": false,
  "reason": "agent 'unknown-agent' not authorized for project 'rust-gateway'",
  "requires_approval": false,
  "policy_id": null,
  "latency_ms": 0.006616999598918483
}
```

---

## A5 — Smoke gate

```
pytest tests/test_smoke.py -v -m smoke --tb=short
8 passed, 1 warning in 2.19s
```

| Test | Result |
|------|--------|
| test_smk01_core_import_python | PASSED |
| test_smk02_health_readiness | PASSED |
| test_smk03_policy_allow_critical_path | PASSED |
| test_smk04_policy_deny_fail_closed | PASSED |
| test_smk05_quota_dependency_read | PASSED |
| test_smk06_identity_verify_valid_token | PASSED |
| test_smk06b_identity_verify_invalid_token | PASSED |
| test_smk06c_identity_verify_unknown_agent | PASSED |
