# PB-7 — Fork-user flow (MSI WSL WARM) — partial PASS

**Date:** 2026-06-27  
**Host:** MSI WSL (`/mnt/d/Projects/ai-control-plane`)  
**Label:** **WARM** — pre-existing clone, `.venv`, Docker `minimal-acp-api-1`  
**Does NOT close PB-7** — CLEAN machine fork still required before PB-12

## Commands (PACE Check — fork onboarding)

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
curl -sf -X POST "$ACP_API_URL/policy/evaluate" -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}'
curl -sf -X POST "$ACP_API_URL/policy/evaluate" -H "Content-Type: application/json" \
  -d '{"agent_id":"unknown-agent","project_id":"rust-gateway","tool_name":"git_read"}' | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
```

## Operator output

**`/health`:** `status: ok`, `config_loaded: true`, `policy_rules_count: 8`, agents `agent1..3`

**`/policy/evaluate` (allow):** `{"allowed":true,"reason":"action permitted",...}`

**`/policy/evaluate` (deny — CS-06):** `allowed: false`, `reason: "unknown agent or role"`

**Runtime verify:**

```text
OK: governance/status runtime verify 1.3.3 13 patterns
```

## Verdict

| Check | Result |
|-------|--------|
| L4 fail-closed wire (`/health` + policy allow) | ✅ |
| L4 deny unknown agent (CS-06) | ✅ `allowed: false` |
| L5 governance UX (`verify_governance_status_runtime.sh`) | ✅ v1.3.3 · 13 patterns |
| PB-7 ≤15 min clean fork | ⏳ **Not claimed** — WARM only |

**Next:** Full Path A on **CLEAN** laptop per [`RUNBOOK.md`](../RUNBOOK.md).
