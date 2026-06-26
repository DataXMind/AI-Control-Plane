# Study 08 — Checklist

- [ ] Gate B approved for Study 08
- [ ] VPS `ubuntu-vps` reachable via Tailscale
- [ ] Stop fixture Docker: `docker compose -f examples/minimal/docker-compose.yml down`
- [ ] Start API with shipped config (see RUNBOOK)
- [ ] `GET /health` → `policy_rules_count: 10`
- [ ] `agents_loaded` includes `agent4`
- [ ] `projects_loaded` includes `datax-analytics`
- [ ] Remote soak from laptop OR VPS local → rules=10 path
- [ ] Artifacts saved under `artifacts/`
- [ ] `RESULTS.md` updated PASS/FAIL
