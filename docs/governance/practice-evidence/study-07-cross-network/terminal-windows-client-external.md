# Study 07 — Terminal — Laptop Windows client (WSL)

**Captured:** 2026-06-25  
**Host:** MSI Laptop WSL  
**Client Tailscale:** `<CLIENT_TAILSCALE_IP>`

## Client config

```bash
export ACP_API_URL=http://<VPS_TAILSCALE_IP>:8000
```

## Drills

```bash
curl -v "$ACP_API_URL/health"
# → 200, policy_rules_count: 8

agentctl gov status
# → rules 8, PB-9 IN_PROGRESS

agentctl assign rust-gateway agent2 git_read --json
# → task_id: 6206697f-eab5-49c8-83e0-0dcf887d4999

bash scripts/soak_staging.sh
# → 2026-06-25T11:18:21Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

**Verdict:** 7-1 through 7-5 PASS via Tailscale only.
