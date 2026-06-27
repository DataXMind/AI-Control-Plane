# PB-9 — Staging soak log

**Issue:** [#77](https://github.com/DataXMind/AI-Control-Plane/issues/77)  
**Approved start:** 2026-06-22 (maintainer: *Approve đi tiếp*)  
**Target end:** 2026-07-06 (≥14 calendar days)  
**Stack:** `examples/minimal/docker-compose.yml` + `ACP_DATA_DIR=/data/acp`

**Agent rule (ML5):** Soak evidence lives **only** in this file. Operator chat *"đã tick ngày YYYY-MM-DD"* → update that row; do not store soak state in chat or other docs.

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
| 2026-06-27 | ☑ | ☑ | ☑ | ☑ | 0 | Local: Docker `minimal-acp-api-1` healthy; `/tmp/acp-soak-staging.log` PASS @ 06:51, 06:58 UTC; hourly loop PID 3195 (`nohup --loop 3600`) |
| … | | | | | | |
| 2026-07-06 | ☐ | ☐ | ☐ | ☐ | 0 | Day 14 review |

---

## Day 14 review criteria

- [ ] Zero SEV-1/2 attributed to control plane
- [ ] `POST /policy/evaluate` p99 < 500 ms (sample from logs)
- [ ] Telemetry/task files under `ACP_DATA_DIR` grow predictably (no disk runaway)
- [ ] Close #77 → open PB-10 (#78) if pass

---

**Operator:** DataXMind maintainers
