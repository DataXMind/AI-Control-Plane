# Mac Mini — Tier A pilot deploy evidence

**Document ID:** ACP-GOV-PRACTICE-MAC-PILOT-001  
**Status:** **PASS** @ 2026-06-30  
**Host:** `dataxmind@DataXMinds-Mac-mini` · Docker Desktop · Compose v5.1.4  
**Baseline:** `master` @ **`8a4e7fa`** (PR [#175](https://github.com/DataXMind/AI-Control-Plane/pull/175) — `pip install -e ".[redis]"` in minimal Dockerfile)  
**Related:** [`examples/minimal/PRODUCTION_DEPLOY.md`](../../../examples/minimal/PRODUCTION_DEPLOY.md) · Profile **B** (10 rules) via bind mount

> **Scope:** Internal pilot — **not** PB-9 soak evidence. PB-9 remains fixture stack (`docker-compose.yml` only @ 8 rules).

---

## Verdict

| Check | Result |
|-------|--------|
| `docker compose` pilot stack up | **PASS** |
| `bash verify-pilot.sh` | **PASS** |
| `GET /health` | **PASS** — `policy_rules_count: 10`, 4 agents, 2 projects |
| `verify_governance_status_runtime.sh` | **PASS** — v1.5.0 · 17 patterns |
| Redis + `ACP_REDIS_URL` | **PASS** after Dockerfile `[redis]` extra (#175) |

---

## Stack used

```bash
cd examples/minimal
cp .env.production.example .env.production
mkdir -p production-config
cp ../../config/{policies,agents,projects}.yml production-config/

docker compose -f docker-compose.yml \
  -f docker-compose.production.yml \
  --env-file .env.production \
  up -d --build

bash verify-pilot.sh
```

---

## Health snapshot (operator-confirmed)

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

Governance: `OK: governance/status runtime verify 1.5.0 17 patterns`

---

## Issues encountered (resolved — do not re-debug)

| # | Symptom | Root cause | Fix |
|---|---------|------------|-----|
| 1 | `unknown shorthand flag: -f` / `unknown command: docker compose` | Compose plugin missing (CLI-only install) | Docker Desktop or `brew install docker-compose` |
| 2 | `.env.production.example` missing | Stale clone before PR #172 | `git pull` @ `b700a14+` |
| 3 | `cp` from repo root failed | Files under `examples/minimal/` | `cd examples/minimal` first |
| 4 | `acp-api` **Restarting (1)** | `ACP_REDIS_URL` set but image lacked `redis` pip extra | Dockerfile `pip install -e ".[redis]"` (#175) |
| 5 | `scripts/*` not found | Ran from `examples/minimal` | Repo root: `cd ../..` |
| 6 | `export ACP_CONFIG_DIR` on host | Does not mount into container | `ACP_HOST_CONFIG_DIR` in `.env.production` |

---

## Drift guards (agent / doc readers)

- **10 rules** = Profile **B** (`config/` bind mount) — **not** fixture **8** (PB-9 / smoke).
- **Pilot ≠ PB-9** — do not replace soak fixture stack for calendar evidence.
- **Scripts path:** `scripts/verify_*` from **repo root** only.
- **Mac compose:** require `docker compose version` or `docker-compose` before pilot docs.

---

**Operator:** DataXMind · **Date:** 2026-06-30
