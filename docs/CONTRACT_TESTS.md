# API Contract Tests (L4)

**Document ID:** ACP-CONTRACT-TESTS-001  
**Purpose:** Lock HTTP schemas consumed by TypeScript PolicyClient and integrators.  
**Enforcement:** `tests/test_api_contract_snapshot.py` + CI Full suite.

---

## Frozen endpoints @ Public Beta

| Method | Path | Schema | Breaking change policy |
|--------|------|--------|----------------------|
| GET | `/health` | `HealthResponse` | Additive fields OK until `1.0.0`; no removals |
| POST | `/policy/evaluate` | `PolicyEvaluateRequest` → `PolicyDecision` | `allowed` + `reason` required |
| POST | `/identity/verify` | JWT body → `AgentIdentity` | Auth fail = **401** (not 200+deny) |
| GET | `/quota/{project_id}` | `QuotaStatus` | — |
| GET | `/quota/agent/{agent_id}` | `QuotaStatus` | — |
| GET | `/quota/profile/{profile_id}` | `QuotaStatus` | — |

---

## Identity vs policy contract (invariant)

| Path | Deny semantics |
|------|----------------|
| `/identity/verify` | HTTP **401** — invalid JWT, unknown agent |
| `/policy/evaluate` | HTTP **200** + `allowed=false` + non-empty `reason` |

---

## Verify

```bash
pytest tests/test_api_contract_snapshot.py -v
```

Before Public Beta flip (#80): all contract snapshots green + OpenAPI export matches `docs/openapi/openapi.json`.

**Last updated:** 2026-06-22
