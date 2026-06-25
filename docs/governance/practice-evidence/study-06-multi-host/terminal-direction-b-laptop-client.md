# Study 06 — Direction B — Laptop client (WSL)

**Captured:** 2026-06-25  
**Role:** Client (round 2)  
**Path:** `/mnt/d/Projects/ai-control-plane`

## Prior — round A server stopped

```bash
# uvicorn on :8000 Ctrl+C after Mac client drills
```

## Client drill

```bash
export ACP_API_URL=http://192.168.1.99:8000

agentctl gov status
```

**Output:**

- Framework: `6-layer-karpathy (v1.0)`
- Config loaded: True | Policy rules: **8**
- Milestones: A/B/C/C+ CLOSED; `public_beta: IN_PROGRESS`
- Case studies CS-01..CS-06 listed
- Docs: `docs/governance/GOVERNANCE_UX_RUNTIME.md`

## Not captured this round

- `POST /policy/evaluate` và `agentctl assign` — round A đã cover; round B chứng minh chiều ngược qua governance CLI.
