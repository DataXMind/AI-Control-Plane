# VPS runtime verify v1.3 — PASS

**Captured:** 2026-06-26 (UTC)  
**Host:** `ubuntu-vps` (`root@~/AI-Control-Plane`)  
**Master:** `a43524a`  
**Stack:** Docker + `acp-staging.service` (Profile A fixture, rules=8)

## Procedure

```bash
rm -f scripts/verify_governance_status_runtime.sh
git pull origin master
sudo systemctl restart acp-staging.service
export ACP_API_URL=http://127.0.0.1:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
```

## Health (sanity)

```json
{
  "status": "ok",
  "policy_rules_count": 8,
  "agents_loaded": ["agent1", "agent2", "agent3"],
  "projects_loaded": ["rust-gateway"]
}
```

## Runtime verify output

```text
OK: governance/status runtime verify 1.3.0 12 patterns
```

## Assertions (v1.3)

| ID | Check | Result |
|----|-------|--------|
| V13-1 | `governance_version` | `1.3.0` ✅ |
| V13-2 | `known_gaps` count | `7` ✅ |
| V13-3 | OPEN gaps | `G-05` only ✅ |
| V13-4 | `lessons_patterns` | `12` ✅ |
| V13-5 | `studies_completed` | `8` ✅ |
| V13-6 | `doc_links.risk_policy` | ✅ |

**Verdict:** **PASS** — 3-stream convergence runtime gate closed on VPS.
