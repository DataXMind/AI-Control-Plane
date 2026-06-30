# P-15 — k6 policy evaluate load smoke — Results

**Document ID:** ACP-GOV-PRACTICE-K6-001  
**Status:** **PASS** (load smoke — not PB-9 soak replacement)  
**Run date:** 2026-06-30  
**Operator:** ubuntu@MSI (WSL)  
**Baseline:** `master` @ `2fce5f5` · catalog **v1.5.0**

---

## Verdict

| Overall | Thresholds | Blocks PB-12? |
|---------|------------|---------------|
| **PASS** | `http_req_failed < 1%` · `p(99)<500ms` design target @ 10 VUs | **No** — closes P-15 skeleton gap; not production SLO proof |

---

## Test matrix

| ID | Step | Expected | Actual | Result |
|----|------|----------|--------|--------|
| K6-1 | API healthy | `GET /health` 200 | 8 rules, 3 agents | ✅ |
| K6-2 | Policy allow baseline | `allowed: true` | `action permitted` | ✅ |
| K6-3 | k6 run | 10 VUs × 15s | 1393 reqs · 0% failed | ✅ |
| K6-4 | Latency | p95 < 500ms (design) | p95 **9.33ms** · max **137ms** | ✅ |
| K6-5 | Checks | 100% pass | 2786/2786 | ✅ |

---

## Run parameters

| Field | Value |
|-------|-------|
| Tool | k6 v0.57.0 (project `.tools/k6` or system PATH) |
| Script | `benchmarks/k6/policy_evaluate.js` |
| `ACP_API_URL` | `http://127.0.0.1:8000` |
| Container | `minimal-acp-api-1` (Docker Compose) |
| VUs | 10 |
| Duration | 15s |
| Throughput | ~87 req/s |

---

## Machine profile

See [`artifacts/machine-profile.md`](artifacts/machine-profile.md).

---

## Artifacts

- [x] [`artifacts/k6-summary.json`](artifacts/k6-summary.json) — machine-readable metrics
- [x] [`artifacts/k6-run.log`](artifacts/k6-run.log) — terminal output
- [x] [`artifacts/health.json`](artifacts/health.json)
- [x] [`artifacts/policy-allow-sample.json`](artifacts/policy-allow-sample.json)

---

## Honest scope

This PASS validates **low-concurrency load smoke** on a single host. It does **not** replace PB-9 calendar soak, burst testing (100+ RPS), or multi-host fleet proof. Label as **P-15 closure** per `LOAD_CHARACTERISTICS.md`.

**Re-run:** `bash scripts/run_k6_policy_smoke.sh` with API up; set `K6_ARTIFACT_DIR` to export summary JSON.
