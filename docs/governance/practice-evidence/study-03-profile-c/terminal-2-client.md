# Study 03 — Terminal 2 (client / soak)

**Role:** Profile C — curl, soak script, agentctl  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study03/terminal02-cs03.md`

---

## Environment

```bash
export ACP_API_URL=http://localhost:8000
```

---

## C1 — Health (via Docker-published port)

```json
{
  "status": "ok",
  "config_loaded": true,
  "policy_rules_count": 8,
  "agents_loaded": ["agent1", "agent2", "agent3"],
  "projects_loaded": ["rust-gateway"],
  "model_profiles_loaded": [
    "claude-pro-backend",
    "claude-team-infra",
    "claude-team-review"
  ]
}
```

Matches **Study 01 fixture** — expected for minimal compose stack.

---

## C2/C4 — PB-9 soak script

**Command:** `bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log`

| Run | Timestamp (UTC) | Line |
|-----|-----------------|------|
| 1 | 2026-06-25T05:39:51Z | `soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok` |
| 2 | 2026-06-25T05:40:47Z | same shape |

**Log file (`cat /tmp/acp-soak-staging.log`):** 2 lines — both PASS.

---

## C3 — Governance UX

**CLI (`agentctl gov status`):**

- Policy rules: **8**
- Public Beta: PB-9 staging soak (#77-#80)
- Case studies CS-01..CS-06 listed (ran twice — identical)
