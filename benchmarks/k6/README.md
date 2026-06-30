# k6 load benchmarks — ACP policy path (P-15)

**Status:** Operator-run closure @ `practice-evidence/k6-policy-smoke/` — **not** a CI merge gate.

## Prerequisites

- [k6](https://k6.io/docs/get-started/installation/) installed
- ACP API running (`bash scripts/acp-up.sh`)

## Quick run

```bash
export ACP_API_URL=http://127.0.0.1:8000
bash scripts/run_k6_policy_smoke.sh
```

## Manual tuning

```bash
K6_VUS=50 K6_DURATION=60s k6 run benchmarks/k6/policy_evaluate.js
```

## Interpretation

| Threshold | Meaning |
|-----------|---------|
| `p(99)<500` | Design target @ low VUs — see `LOAD_CHARACTERISTICS.md` |
| `http_req_failed<1%` | No transport errors |

**Honest scope:** This does **not** replace PB-9 calendar soak. Label results as **load smoke**, not production SLO proof.

**SSOT:** [`docs/governance/LOAD_CHARACTERISTICS.md`](../../docs/governance/LOAD_CHARACTERISTICS.md)
