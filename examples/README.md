# ACP Examples

Fork-and-run in **≤15 minutes** — SSOT for Public Beta technical gate PB-5.

| Example | Use when |
|---------|----------|
| [**minimal/**](minimal/README.md) | Default: Docker or native uvicorn, fixture config (8 rules), PB-9 soak parity |

## Quick start (Docker — recommended)

```bash
# From repo root
docker compose -f examples/minimal/docker-compose.yml up --build

# Or from this example directory
cd examples/minimal
docker compose up --build
```

```bash
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/verify_governance_status_runtime.sh
```

## Clean-machine verify (PB-7)

Full ≤15 min evidence path: [`docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md`](../docs/governance/practice-evidence/pb-7-clean-machine-fork/RUNBOOK.md).

## Do not duplicate

Claude prompts that create a second `examples/docker-compose.yml` at repo root are **stale** — see [`docs/governance/PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md`](../docs/governance/PB_FINAL_BLOCKERS_PACKET_RECONCILIATION.md).
