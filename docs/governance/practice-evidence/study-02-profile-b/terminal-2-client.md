# Study 02 — Terminal 2 (client)

**Role:** Profile B — curl, agentctl  
**Captured:** 2026-06-25  
**Source:** operator log `TestCase/Study02/terminal02-casestudy02.md`

---

## Environment

```bash
cd /mnt/d/Projects/ai-control-plane
source .venv/bin/activate
export ACP_API_URL=http://localhost:8000
```

---

## B1 — Health

```json
{
  "status": "ok",
  "config_loaded": true,
  "policy_rules_count": 10,
  "agents_loaded": ["agent1", "agent2", "agent3", "agent4"],
  "projects_loaded": ["datax-analytics", "rust-gateway"],
  "model_profiles_loaded": [
    "claude-pro-backend",
    "claude-team-analytics",
    "claude-team-infra",
    "claude-team-review"
  ]
}
```

---

## B2 — Governance UX

**CLI (`agentctl gov status`):**

- Framework: `6-layer-karpathy` (v1.0)
- Policy rules: **10**
- Case studies: CS-01 through CS-06

---

## B3 — CLI assign (HTTP path)

```json
{
  "task_id": "5fcbe7f5-c943-4e0e-9e3e-d3897597f5ae",
  "project_id": "rust-gateway",
  "agent_id": "agent2",
  "task_type": "git_read",
  "state": "PENDING"
}
```

Command: `agentctl assign rust-gateway agent2 git_read --json`

T1 correlated: `POST /policy/evaluate` + `POST /tasks` @ 12:29:28 with `X-Agent-Id: agent2`.
