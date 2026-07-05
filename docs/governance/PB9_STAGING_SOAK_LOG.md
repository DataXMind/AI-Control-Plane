# PB-9 — Staging soak log

**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Approved start:** 2026-06-22 (maintainer: *Approve đi tiếp*)  
**Target end:** 2026-07-06 (≥14 calendar days)  
**Stack:** `examples/minimal/docker-compose.yml` + `ACP_DATA_DIR=/data/acp`

**Agent rule (ML5):** Soak evidence lives in this file **and** [`PB9_SOAK_ITERATION_LOG.md`](PB9_SOAK_ITERATION_LOG.md). Operator chat *"đã tick ngày YYYY-MM-DD"* → update daily row; do not store soak state in chat or other docs.

> **⚠️ Scope note:** PB-9 is a STABILITY SOAK at low load (~1 req/hour automated), NOT a load test or performance benchmark. p99 SLO targets are design targets only, not verified at production load. See [LOAD_CHARACTERISTICS.md](LOAD_CHARACTERISTICS.md) for full scope boundaries.

---

## Soak clock vs evidence window (resolved 2026-06-27)

| Concept | Date | SSOT |
|---------|------|------|
| **Calendar clock** | Start **2026-06-22** (maintainer approve) | `governance_catalog.py` · `soak_started` |
| **Day 14 review target** | **~2026-07-06** | From calendar clock |
| **Evidence window** | First logged iteration **2026-06-26** | This file + iteration log |
| **Gap 06-22 → 06-25** | **Documented** — deploy deferred Day 0; no local Docker/log | Not a soak *failure*; low evidence density |

**Review rule:** Day 14 uses calendar date **2026-07-06** with explicit note that machine evidence begins 2026-06-26. If SEV/anomaly count is clean, gap does not extend review date. See [`ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md`](ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md).

**Persistence:** Hourly loop must use `--repo-log` (see below). `/tmp/` or `/var/log/` alone is not sufficient for ML5.

| Host | Command | Machine log path |
|------|---------|------------------|
| **MSI WSL** | `bash scripts/restart_soak_loop.sh` | `docs/governance/PB9_SOAK_ITERATION_LOG.md` (repo) |
| **VPS** | `acp-soak.service` | `practice-evidence/pb-9-day14-review/artifacts/vps-soak-iteration.log` (host-local, gitignored) + `/var/log/acp-soak-staging.log` |

Do **not** append raw lines into this daily table — machine lines belong in the iteration logs above.

---

## Day 0 — deploy

```bash
# From repo root
docker compose -f examples/minimal/docker-compose.yml up -d --build
export ACP_API_URL=http://localhost:8000
curl -sf "$ACP_API_URL/health" | python3 -m json.tool
bash scripts/soak_staging.sh --log /tmp/acp-soak-staging.log
```

**Hourly workload (background):**

```bash
nohup bash scripts/soak_staging.sh --loop 3600 --log /tmp/acp-soak-staging.log &
```

---

## Daily checklist

| Date | Health OK | Policy allow | Quota read | Apex trigger | SEV-1/2 | Notes |
|------|-----------|--------------|------------|--------------|---------|-------|
| 2026-06-22 | ☐ | ☐ | ☐ | ☐ | 0 | Soak clock started (approved); deploy deferred |
| 2026-06-23 | ☐ | ☐ | ☐ | ☐ | 0 | No local soak evidence |
| 2026-06-24 | ☐ | ☐ | ☐ | ☐ | 0 | No local soak evidence |
| 2026-06-25 | ☐ | ☐ | ☐ | ☐ | 0 | No local soak evidence |
| 2026-06-26 | ☑ | ☑ | ☑ | ☑ | 0 | Local: Docker `minimal-acp-api-1` healthy; `/tmp/acp-soak-staging.log` PASS @ 03:33, 03:43 UTC; hourly loop restarted. Remote drill (non-PB-9): laptop→VPS TS @ 04:33Z; VPS Docker @ 04:32Z |
| 2026-06-27 | ☑ | ☑ | ☑ | ☑ | 0 | AM: soak PASS @ 06:51, 06:58 UTC; hourly loop PID 3195. **PM tick (post-merge #118):** `master` @ `375ef14`; PACE smoke 8/8 + governance 1.3.3 + OpenAPI 13 paths; soak PASS @ 11:53Z |
| 2026-06-28 | ☑ | ☑ | ☑ | ☑ | 0 | MSI: PACE 8/8 · governance/OpenAPI verify · soak @ 02:23Z — [`pace-verify-msi-2026-06-28.md`](practice-evidence/governance-status-v13-verify/artifacts/pace-verify-msi-2026-06-28.md). **VPS:** CUR-04 deploy + hourly PASS `08:29Z`/`09:29Z` · pull `98f193c` — [`vps-hourly-loop-verify-2026-06-28.md`](practice-evidence/pb-9-day14-review/artifacts/vps-hourly-loop-verify-2026-06-28.md) |
| 2026-06-29 | ☑ | ☑ | ☑ | ☑ | 0 | MSI gap 13h Docker stop → restarted 01:20Z; VPS continuous | RECONCILED 2026-06-30: Docker inspect confirms RestartCount=0 on current container — gap window 2026-06-29 13h + iteration log silence until 2026-06-30T10:32:30Z is consistent with manual rebuild/restart (not crash), verified during PR #163-168 testing cycle. Final classification: SEV-3 (planned restart). No SEV-1/2 evidence found across full gap window. |
| 2026-06-30 | ☑ | ☑ | ☑ | ☐ | 0 | Live verify 2026-06-30: health=ok (8 rules, 3 agents, 1 project); policy/evaluate allowed=true evaluation_path=default_allow latency=5.34ms; quota tokens_remaining=2000000.0. Container `minimal-acp-api-1` StartedAt=2026-06-30T10:32:30Z, RestartCount=0 (manual restart during PR #163-168 verification, not a crash/fail-open). Soak iteration log gap 2026-06-29T11:26:07Z → restart: classified SEV-3 (planned/manual restart per PB9_DAY14_REVIEW_TEMPLATE.md criteria) — no data loss, no fail-open observed, health/policy/quota all green post-restart. Apex not independently re-tested today; last known good from iteration log: 2026-06-29T11:26:07Z apex=ok. |
| 2026-07-01 | ☑ | ☑ | ☑ | ☑ | 0 | **MSI WSL (PB-9 fixture):** `docker compose -f examples/minimal/docker-compose.yml` — `minimal-acp-api-1` healthy (8 rules); `soak_staging.sh` PASS health/policy/quota/**apex**; `restart_soak_loop.sh` → hourly `--repo-log`. **PACE:** smoke 8/8 (`.venv`) · `verify_governance_status_runtime.sh` → 1.5.0·17. **Docs:** PR [#176](https://github.com/DataXMind/AI-Control-Plane/pull/176) merged → `master` @ `2202f16` (Mac pilot evidence). **Mac Mini:** pilot stack (10 rules) + verify OK — parallel Tier A, not PB-9 soak SSOT. PM verify: container down → SEV-3 `soak_iter` fail @ 06:51Z → rebuild; recovery `apex=ok` @ 07:09Z (see iteration log). |
| 2026-07-02 | ☑ | ☑ | ☑ | ☑ | 0 | **AM (#181):** iteration log catch-up; VPS services active through 07-01T06:29:30Z. **PM (#185):** agent verify @ 07:18:16Z — container `Exited (255)` ~17h → rebuild; `soak_staging.sh --repo-log` PASS; smoke 8/8 · gov 1.5.0·17. **SEV-3** manual recovery. Hourly loop active (iter through 08:23:48Z). **Docs:** `master` @ `44a5fef` (#183 END_USER_VALUE · #185 anchor). |
| 2026-07-03 | ☑ | ☑ | ☑ | ☑ | 0 | **AM:** agent verify @ 04:13:19Z — container down overnight (~17h gap after 07-02T11:23:45Z) → `docker compose up -d --build`; `soak_staging.sh --repo-log` PASS; smoke 8/8 · gov 1.5.0·17. **SEV-3** manual recovery. Hourly loop restarted (`restart_soak_loop.sh`). Iter backlog 07-02 09–11Z in commit `d374780`. |
| 2026-07-04 | ☑ | ☑ | ☐ | ☐ | 0 | **VPS production (build path):** MSI `curl` health 10 rules @ `100.94.21.33:8000` OK; `minimal-acp-api-1` Running. **MSI enforce:** `run_tool_guarded` fail-closed — `~/.acp-agent.env` vars not `export`ed (python → `127.0.0.1:8000`); fix `antigravity-acp.env.example`. **VPS:** `minimal-redis-1 Waiting` = redis healthgate — wait, do not interrupt. PB-9 local fixture hourly not run today. |
| 2026-07-05 | ☑ | ☑ | ☑ | ☑ | 0 | **MSI WSL (PB-9 fixture):** `docker compose -f examples/minimal/docker-compose.yml up -d --build`; `restart_soak_loop.sh` → hourly `--repo-log` (PID 4681); `soak_staging.sh --repo-log` PASS @ 01:56:35Z; smoke 8/8 (`.venv`). **SEV-3** gap ~39h after 07-03T10:46:02Z (container stop overnight → manual rebuild). **VPS:** `acp-soak.service` + `acp-staging.service` **inactive** — dual-host soak not running; operator restart required before Day 14. |
| 2026-07-06 | ☐ | ☐ | ☐ | ☐ | 0 | Day 14 review |

---

## Day 14 review criteria

- [ ] Zero SEV-1/2 attributed to control plane
- [ ] `POST /policy/evaluate` p99 < 500 ms (sample from logs)
- [ ] Telemetry/task files under `ACP_DATA_DIR` grow predictably (no disk runaway)
- [ ] Close #77 → open PB-10 (#78) if pass

---

**Operator:** DataXMind maintainers
