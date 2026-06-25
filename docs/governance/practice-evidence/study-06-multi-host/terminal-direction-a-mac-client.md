# Study 06 — Direction A — Mac client

**Captured:** 2026-06-25  
**Role:** Client (round 1)  
**Path:** `~/AI-Control-Plane`  
**LAN:** `192.168.1.99` (`en0`)

## Phase 0

```bash
sudo tailscale up
tailscale status   # msi 100.102.105.47 online
ping -c 4 192.168.1.59   # 0% loss
```

## Client drills

```bash
export ACP_API_URL=http://192.168.1.59:8000

curl -v --connect-timeout 5 "$ACP_API_URL/health"
# → HTTP 200, rules 8

agentctl gov status
# → Framework 6-layer-karpathy; rules 8; PB-9 IN_PROGRESS

curl -s -X POST "$ACP_API_URL/policy/evaluate" \
  -H "Content-Type: application/json" \
  -d '{"agent_id":"agent2","project_id":"rust-gateway","tool_name":"git_read","role":"backend"}'
# → allowed: true, latency_ms: 4.17

agentctl assign rust-gateway agent2 git_read --json
# → task_id: 03c332db-645a-481f-834f-6b9420fb9375, state: PENDING
```

## Teardown round A

```bash
unset ACP_API_URL
```
