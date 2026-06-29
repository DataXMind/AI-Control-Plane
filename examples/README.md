# ACP Examples

Fork-and-run in **≤15 minutes** — SSOT for Public Beta technical gate PB-5.

**Which path?** End-user: [`docs/QUICKSTART.md`](../docs/QUICKSTART.md) · Advanced map: [`docs/DEVELOPER_SCENARIOS.md`](../docs/DEVELOPER_SCENARIOS.md).

| Example | Use when |
|---------|----------|
| [`scripts/acp-up.sh`](../scripts/acp-up.sh) | One-command RUN door: `bash scripts/acp-up.sh` |
| [**minimal/**](minimal/README.md) | Docker/native, fixture config (8 rules), PB-9 soak parity |
| [**integrate/**](integrate/README.md) | CONNECT door: Python before tool call, health gate, quota |

## Quick start (Docker — recommended)

```bash
# One command (from repo root)
bash scripts/acp-up.sh

# Or compose directly
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
