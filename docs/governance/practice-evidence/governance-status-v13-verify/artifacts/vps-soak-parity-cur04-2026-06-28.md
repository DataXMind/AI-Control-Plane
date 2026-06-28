# PACE verify — VPS soak parity + doc drift (CUR-04 / D)

**Document ID:** ACP-GOV-PRACTICE-PACE-2026-06-28-CUR04  
**Date:** 2026-06-28  
**Scope:** Docs-only + `scripts/soak_staging.sh` mkdir guard + `acp-soak.service` `--repo-log` (Karpathy: governance track, no `src/`)  
**Baseline:** `master` @ `c58b4cc` (pre-commit)

## PACE

| Step | Action | Outcome |
|------|--------|---------|
| **P** Pause | Confirmed separate VPS path vs MSI `PB9_SOAK_ITERATION_LOG.md` — no git conflict | ✅ |
| **A** Act | CUR-04 unit + `pb-9-day14-review/artifacts/` + doc drift (README, RUNBOOK, action plan) | ✅ |
| **C** Check | Smoke gate + script sanity | See below |
| **E** Evolve | Tier C: action plan CUR-04, reconciliation wired artifacts, Day 14 template | ✅ |

## Check (MSI WSL — DEVELOPMENT_PROTOCOL §5.4)

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
pytest tests/test_smoke.py -v -m smoke
```

**Expected:** 8/8 PASS (docs-only change; smoke confirms no regression).

**Actual (2026-06-28 MSI WSL):** **8 passed** in 1.66s.

## VPS operator follow-up (not run in this session)

```bash
export ACP_REPO=/root/AI-Control-Plane
cd "$ACP_REPO" && git pull origin master
sudo cp "$ACP_REPO/examples/minimal/systemd/acp-soak.service" /etc/systemd/system/
sudo sed -i "s|/root/AI-Control-Plane|$ACP_REPO|g" /etc/systemd/system/acp-soak.service
sudo systemctl daemon-reload
sudo systemctl restart acp-staging.service acp-soak.service
tail -3 "$ACP_REPO/docs/governance/practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log"
```

## Verdict

**PASS** (repo changes) — VPS runtime verify pending operator deploy after pull.

**Not claimed:** PB-9 Day 14 PASS · `gates_remaining` unchanged · OP-08 tag calendar.
