# k6 Fleet Load Test Plan — Post-Flip (Operator-Run)

**Document ID:** ACP-GOV-K6-FLEET-PLAN-001  
**Status:** PROPOSED (plan only — no execution in this document)  
**Baseline:** `master` @ `2ea2ad8` · catalog v1.5.0  
**Related:** [`LOAD_CHARACTERISTICS.md`](LOAD_CHARACTERISTICS.md) · [`benchmarks/k6/policy_evaluate.js`](../../benchmarks/k6/policy_evaluate.js) · [`practice-evidence/k6-policy-smoke/`](../practice-evidence/k6-policy-smoke/)

> **STATUS: PROPOSED — implementation sau PB-12 flip (~2026-07-10), không kích hoạt trước**

---

## Hiện trạng

| Item | Status |
|------|--------|
| P-15 closure | **PASS** @ 10 VUs — load **smoke**, not fleet SLO |
| Script | `benchmarks/k6/policy_evaluate.js` |
| Evidence | [`practice-evidence/k6-policy-smoke/RESULTS.md`](../practice-evidence/k6-policy-smoke/RESULTS.md) |
| CI gate | **No** — operator-run only @ 0.x |

Smoke @ 10 VUs (~87 req/s, p95 9.33ms) validates **low-concurrency** correctness. It does **not** prove production fleet SLO.

---

## Fleet test plan (post-flip)

| Stage | VUs | Duration (indicative) | p99 design target | Notes |
|-------|-----|----------------------|-------------------|-------|
| F1 | 50 | 60s | < 200ms | Warm fleet |
| F2 | 100 | 60s | < 200ms | Target from `LOAD_CHARACTERISTICS.md` |
| F3 | 500 | 30s | exploratory | Burst / stress — label separately from SLO |

**Endpoint:** `POST /policy/evaluate` (same payload as smoke).

**Paths under load:** Policy hot path + optional Redis quota (`core/quota.py`) if enabled in staging config.

---

## Môi trường

- **Staging host riêng** — dedicated instance or compose stack
- **KHÔNG** chạy trên PB-9 soak host (MSI/VPS calendar soak)
- **KHÔNG** chạy against production without maintainer sign-off

**Runner:** `bash scripts/run_k6_policy_smoke.sh` with `K6_VUS` / `K6_DURATION` overrides, or direct `k6 run`.

---

## Explicit non-goals @ 0.x

- **Không làm CI gate** cho 0.x — operator-run only, post-flip
- **Không** sửa `benchmarks/k6/policy_evaluate.js` trong plan PR
- **Không** thêm `.github/workflows/` job

Results (when run) → `docs/governance/practice-evidence/k6-fleet-*/` with `RESULTS.md` + `k6-summary.json`.

---

## Trigger để mở implementation task

Mở fleet execution khi **cả hai**:

1. **PB-12 flip** xong, **và**
2. Pilot / production thật yêu cầu biết **SLO** @ >10 concurrent agents

Absent (2), smoke @ 10 VUs remains sufficient for 0.x Public Beta evidence.

---

**Activation:** Chỉ schedule fleet runs sau PB-12 flip; maintainer approves staging window.

**Last updated:** 2026-06-30
