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
| 2026-06-22 | ☐ | ☐ | ☐ | ☐ | 0 | Soak clock started (approved) |
| 2026-06-23 | ☐ | | | | | |
| … | | | | | | |
| 2026-07-06 | ☐ | | | | | Day 14 review |

---

## Day 14 review criteria

- [ ] Zero SEV-1/2 attributed to control plane
- [ ] `POST /policy/evaluate` p99 < 500 ms (sample from logs)
- [ ] Telemetry/task files under `ACP_DATA_DIR` grow predictably (no disk runaway)
- [ ] Close #77 → open PB-10 (#78) if pass

---

**Operator:** DataXMind maintainers
