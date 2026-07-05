# Current session anchor — copy-paste block (living snapshot)

**Document ID:** ACP-PROMPT-ANCHOR-CURRENT-001  
**Update rule:** Maintainer or closing agent updates this file after **major merge** to `master`.  
**Structure SSOT:** [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md)

---

## Canonical one-liner (2026-07-05)

```text
SESSION ANCHOR: master @ post-#191 · pytest 221 · risk LOW
Hybrid Gateway × ACP: CONNECT CLOSED — MSI agent1 + Mac agent2 + Gateway main #4 (35bf124)
AEOS × ACP: PHASE 2 SMOKE PASS — aeos main @ 9be7e2a · POST /sessions HTTP 201 · VPS 100.94.21.33:8000
Enforce: examples/integrate/python/run_tool_guarded.py · export in ~/.acp-agent.env (required)
Client bundle: customer-bundle/integrations/antigravity-acp.env.example
ACP VPS: 100.94.21.33:8000 · rust-gateway (temp for AEOS) · 10 rules · build from ~/AI-Control-Plane
OPEN: VPS acp-soak + acp-staging inactive, aeos GitHub CI (#15–#21), SACP evidence, Day 14 07-06, PB-12 ~07-10
Verify AEOS: API_PORT=8002 · ACP_ENABLED in Ter 2 · curl 127.0.0.1:8002/health
SSOT: hybrid-gateway-acp-integration/RESULTS.md · aeos-acp-integration/RESULTS.md · aeos repo aeos-acp-integration/RESULTS.md
```

**Last updated:** 2026-07-05 · AEOS Phase 2 smoke PASS · PB-9 tick 07-05 · MSI fixture recovered; VPS soak services down
