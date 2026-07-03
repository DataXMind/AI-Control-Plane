# Client integration bundle — Antigravity + Hybrid Gateway

Hand to **integration team** (not VPS operator secrets).

## Files

| File | Purpose |
|------|---------|
| [`antigravity-acp.env.example`](antigravity-acp.env.example) | Per-machine env template |
| [`README.md`](README.md) | This file |

## Install (developer laptop)

```bash
# From ai-control-plane repo root (after git pull master)
cp customer-bundle/integrations/antigravity-acp.env.example ~/.acp-agent.env
# Edit ACP_AGENT_ID / ACP_ROLE per machine

source ~/.acp-agent.env
bash examples/integrate/shell/install_antigravity_hook.sh
```

**MSI:** `ACP_AGENT_ID=agent1` `ACP_ROLE=infra`  
**Mac:** `ACP_AGENT_ID=agent2` `ACP_ROLE=backend`

## Docs

- [`docs/integrations/HYBRID_AI_GATEWAY.md`](../../docs/integrations/HYBRID_AI_GATEWAY.md)
- [`examples/integrate/README.md`](../../examples/integrate/README.md)
- Gateway repo: `docs/ACP_INTEGRATION.md` (after merge)

## Operator (VPS)

Host ACP only — [`HUONG_DAN_CAI_DAT.md`](../HUONG_DAN_CAI_DAT.md). Do **not** put `REDIS_PASSWORD` in this bundle.
