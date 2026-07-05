# Current session anchor — copy-paste block (living snapshot)

**Document ID:** ACP-PROMPT-ANCHOR-CURRENT-001  
**Update rule:** Maintainer or closing agent updates this file after **major merge** to `master`.  
**Structure SSOT:** [`SESSION_ANCHOR_TEMPLATE.md`](SESSION_ANCHOR_TEMPLATE.md)

---

## Canonical one-liner (2026-07-04)

```text
SESSION ANCHOR: master @ post-#190 · pytest 221 · risk LOW
Hybrid Gateway × ACP: CONNECT CLOSED — MSI agent1 + Mac agent2 + Gateway main #4 (35bf124)
Enforce: examples/integrate/run_tool_guarded.py · export in ~/.acp-agent.env (required)
Client bundle: customer-bundle/integrations/antigravity-acp.env.example
ACP VPS: 100.94.21.33:8000 · rust-gateway · 10 rules · build path from ~/AI-Control-Plane
OPEN: MSI re-source env + acp-git retest, VPS redis healthgate patience, PB-9 07-05..06, PB-12
Verify: source ~/.acp-agent.env && python3 -c "import os; print(os.environ['ACP_API_URL'])"
SSOT: HYBRID_AI_GATEWAY.md · practice-evidence/hybrid-gateway-acp-integration/RESULTS.md
```

**Last updated:** 2026-07-04 · PB-9 tick · MSI `export` env pitfall documented
