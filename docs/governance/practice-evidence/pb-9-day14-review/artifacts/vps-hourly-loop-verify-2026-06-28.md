# VPS — Hourly soak loop verify @ 2026-06-28

**Document ID:** ACP-GOV-PRACTICE-PB9-VPS-HOURLY-2026-06-28  
**Host:** `ubuntu-vps` · `root@ubuntu-vps`  
**Repo:** `/root/AI-Control-Plane` @ **`98f193c`** (`git pull` post #119/#120)  
**Service:** `acp-soak.service` (CUR-04 `--repo-log`)

## Verdict

**PASS** — hourly loop confirmed (`08:29:20Z` → `09:29:20Z`, Δ3600s). Dual log parity `/var/log/` + `vps-soak-iteration.log`.

## Procedure & output

```bash
export ACP_REPO=/root/AI-Control-Plane
cd "$ACP_REPO" && git pull origin master   # e76d203..98f193c — docs only; no service restart

sudo systemctl status acp-soak.service --no-pager
tail -5 /var/log/acp-soak-staging.log
tail -5 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
```

### `systemctl status` (excerpt)

- **Active:** `active (running)` since `2026-06-28 08:29:20 UTC`
- **CGroup:** `soak_staging.sh --loop 3600` + `sleep 3600`
- **Journal:** `08:29:20Z` and `09:29:20Z` — `soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok`

### `/var/log/acp-soak-staging.log` (tail)

```text
2026-06-28T08:29:20Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-06-28T09:29:20Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

(Older lines `07:14`–`08:24` pre-CUR-04 restart — SEV-3 documented.)

### `vps-soak-iteration.log` (tail)

```text
2026-06-28T08:29:20Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
2026-06-28T09:29:20Z soak_iter health=ok policy_allowed=True tokens_remaining=2000000.0 apex=ok
```

## Notes

- `git pull` to `98f193c` did **not** require `systemctl restart` (CHANGELOG + go-no-go only).
- Completes operator follow-up from [`vps-soak-parity-cur04-2026-06-28.md`](../../governance-status-v13-verify/artifacts/vps-soak-parity-cur04-2026-06-28.md).

**Not claimed:** PB-9 Day 14 PASS · catalog `gates_remaining` change.
