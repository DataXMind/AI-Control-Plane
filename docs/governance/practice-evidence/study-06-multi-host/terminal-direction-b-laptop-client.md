# Study 06 — Direction B — Laptop client (WSL)

**Captured:** 2026-06-25  
**Role:** Client (round 2)

## Phase 1 — gov status (@ 17:03)

```bash
export ACP_API_URL=http://192.168.1.99:8000
agentctl gov status
```

→ rules **8**; PB-9 IN_PROGRESS; CS-01..CS-06 listed.

## Phase 2 — full policy + assign (@ 17:34)

```bash
curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}'
# → allowed: true, latency_ms: 1.47

agentctl assign rust-gateway agent2 git_read --json
# → task_id: ae6c13a4-0281-4321-b6fc-95a9e37ff777, state: PENDING
```

**Verdict:** Round B full suite PASS (6-2 through 6-4).
