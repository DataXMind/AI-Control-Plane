# Study 08 — Checklist

- [x] Gate B approved for Study 08
- [x] VPS `ubuntu-vps` reachable via Tailscale
- [x] Stop fixture Docker: `docker compose -f examples/minimal/docker-compose.yml down`
- [x] Start API with shipped config (see RUNBOOK)
- [x] `GET /health` → `policy_rules_count: 10`
- [x] `agents_loaded` includes `agent4`
- [x] `projects_loaded` includes `datax-analytics`
- [x] Remote soak from laptop → rules=10 path @ 2026-06-26T10:36:10Z
- [x] Artifacts saved under `artifacts/`
- [x] `RESULTS.md` updated PASS
