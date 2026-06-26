# Study 08 — Remote soak (client phase, partial)

**Captured:** 2026-06-26T09:33:59Z UTC  
**Client:** MSI Laptop (WSL) `100.102.105.47`  
**API:** `http://100.94.21.33:8000` (ubuntu-vps)  
**Gate B:** Approved by operator 2026-06-26

## Command

```bash
export ACP_API_URL=http://100.94.21.33:8000
bash scripts/soak_staging.sh --log /tmp/acp-study08-soak.log
```

## Log excerpt

```
2026-06-26T09:33:59Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

## Verdict

| Check | Result |
|-------|--------|
| Remote soak path (G-07 apex) | ✅ PASS |
| Profile B rules=10 | ❌ **BLOCKED** — VPS still fixture Profile A (`policy_rules_count: 8`) |

**Next:** Operator SSH → `bash scripts/study08_vps_preflight.sh` on VPS, then re-run soak.
