# PB-7 CLEAN fork — Ubuntu @ MSI evidence

**Captured:** 2026-06-27  
**Operator:** ubuntu@MSI  
**Verdict:** **PASS** (Path A Docker, ≤15 min)

## Procedure summary

```bash
docker compose -f examples/minimal/docker-compose.yml up -d --build   # ~54s build
curl -sf http://localhost:8000/health | python3 -m json.tool          # ok
curl -sf -X POST http://localhost:8000/policy/evaluate ... role backend # allowed: true
curl -sf -X POST ... unknown-agent                                      # allowed: false
sed -i 's/\r$//' scripts/verify_governance_status_runtime.sh
export ACP_API_URL=http://localhost:8000
bash scripts/verify_governance_status_runtime.sh                        # 1.3.3 · 13 patterns
docker exec -e ACP_API_URL=http://127.0.0.1:8000 minimal-acp-api-1 \
  agentctl assign rust-gateway agent2 git_read --json
docker compose -f examples/minimal/docker-compose.yml down
```

## Key outputs

**Governance verify:**

```text
OK: governance/status runtime verify 1.3.3 13 patterns
```

**agentctl (optional):**

```json
{
  "task_id": "2e395f6a-6520-4a24-bf5e-3a24a1d3fec4",
  "project_id": "rust-gateway",
  "agent_id": "agent2",
  "task_type": "git_read",
  "state": "PENDING"
}
```

## Analysis

| Check | Result |
|-------|--------|
| Fork path SSOT | ✅ `examples/minimal/docker-compose.yml` |
| Health | ✅ |
| Policy allow/deny | ✅ fail-closed |
| Governance runtime | ✅ v1.3.3 |
| CLI | ✅ via container (host pip not required) |
| CLEAN label | ✅ Ubuntu user / fresh clone path (MSI hardware caveat) |
| CRLF on `/mnt/d` | ⚠️ fixed — recommend `.gitattributes` or clone on ext4 for operators |

**Catalog note:** Practice evidence PASS; `public_beta.gates_remaining` may still list PB-7 until maintainer catalog update @ flip.
