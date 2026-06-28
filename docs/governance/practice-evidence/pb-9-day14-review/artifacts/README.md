# PB-9 Day 14 — VPS soak artifacts

**Host:** `ubuntu-vps` · systemd `acp-soak.service`  
**Path:** `vps-soak-iteration.log` (append-only, **gitignored**)

## Format

Same as MSI machine log — one line per iteration:

```text
2026-06-28T03:05:52Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

## Verify on VPS

```bash
export ACP_REPO=/root/AI-Control-Plane
tail -5 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
tail -3 /var/log/acp-soak-staging.log
```

## Day 14

Include `tail` excerpts from this file and `/var/log/acp-soak-staging.log` in [`../RESULTS.md`](../RESULTS.md) when complete. Do not commit `vps-soak-iteration.log` routinely.
