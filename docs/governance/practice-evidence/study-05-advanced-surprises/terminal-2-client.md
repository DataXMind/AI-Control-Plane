# Study 05 — Terminal 2 (client)

**Captured:** 2026-06-25  
**Source:** `TestCase/Study05/terminal02-cs05.md`

## 5a — API down (before T1 uvicorn)

```text
agentctl gov status     → RuntimeError: governance status unavailable
agentctl assign ...     → policy service unavailable
```

## 5b — Policy allow / deny

**Allow:**

```json
{"agent_id":"agent1","project_id":"rust-gateway","tool_name":"git_read","role":"infra"}
→ allowed: true, reason: "action permitted"
```

**Deny:**

```json
{"agent_id":"agent3","tool_name":"git_push","role":"reviewer",...}
→ allowed: false, reason: "tool 'git_push' denied for role 'reviewer'", policy_id: "rbac-reviewer"
```

## 5c — Invalid body

```json
{"agent_id":"agent2"} only
→ allowed: false, reason contains missing project_id, tool_name
```

(Server T1: HTTP 503 on `/policy/evaluate`)

## 5d — Docker port + stable rules

```text
uvicorn :8000 → Address already in use
curl health ×3 → policy_rules_count: 8, 8, 8
docker compose down
```

## 5f — Bad identity token

```bash
curl -X POST .../identity/verify -d '{"token":"not-a-valid-jwt","agent_id":"agent2"}'
```

```json
{"allowed": false, "reason": "invalid request", ...}
```

## 5g — Kill switch

Not executed (operator skip).
