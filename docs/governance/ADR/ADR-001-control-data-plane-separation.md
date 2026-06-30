# ADR-001: Control Plane / Data Plane Separation

**Status:** PROPOSED (0.x monolithic; separation target v0.3.x)  
**Date:** 2026-06-29  
**Deciders:** DataXMind maintainers  
**Baseline:** `master` @ `cfacac9`

---

## Context

ACP 0.x runs as a monolithic service. All of the following share one process:

- **Policy Engine** (`POST /policy/evaluate`) — latency-critical
- **Governance UX** (`GET /governance/status`) — consistency-critical
- **Health API** (`GET /health`) — availability-critical
- **Telemetry writer** (`ACP_DATA_DIR`) — throughput-critical
- **SAPAL apex layer** (`/apex/trigger`) — batch-critical

This creates resource contention and makes targeted scaling impossible.

---

## Decision

**0.x:** Accept monolithic. Document limitation. No action.

**v0.2.x:** Extract Governance UX and Health API to separate FastAPI routers with independent rate limiting. Still same process, separate routing.

**v0.3.x:** Split into two deployable units:

- **Control Plane:** `GET /governance/status`, `GET /health`, `agentctl`, SAPAL
- **Data Plane:** `POST /policy/evaluate` (stateless, horizontally scalable)
- **Communication:** Control Plane pushes policy config to Data Plane cache. Data Plane does **not** call Control Plane on the hot path.

---

## Consequences

**Positive:**

- Data Plane can be deployed at edge (low latency for agents)
- Control Plane can have different HA requirements
- Scaling policy evaluation independently from governance reporting

**Negative:**

- Config sync latency (policy changes take N seconds to propagate to Data Plane)
- Operational complexity (two services to monitor)
- Breaking API change if clients assume same host

---

## Rejection Criteria

Do not implement if:

- Monolithic p99 < 10ms at target load (separation overhead not worth it)
- Team size < 3 engineers (operational burden too high)

---

## Reactivation Trigger

ADR-001 review must be **reopened** (not auto-implemented) if **any one** of the following occurs:

1. **`apex/` module growth exceeds baseline** — current baseline @ `master` `5ea0aef`: **8 Python files**, **~411 LOC** under `src/ai_control_plane/apex/`. Reopen if file count **> 8** or LOC **> 500** (50% growth buffer).
2. **SAPAL Phase 2 (proposal generation)** is approved per [`SAPAL_LEGAL_ASSESSMENT.md`](../SAPAL_LEGAL_ASSESSMENT.md).
3. **Production incident** involving resource contention between policy evaluation (`POST /policy/evaluate`) and governance reporting (`GET /governance/status` / telemetry writer).

If **none** of the above occur → ADR-001 remains **PROPOSED**; no separation work.

---

## Related

- C1 finding: Architecture Assessment 2026-06-28
- [`THREAT_MODEL.md`](../THREAT_MODEL.md) D-1 (DoS risk on shared process)
- [`OPEN_SOURCE_READINESS.md`](../../OPEN_SOURCE_READINESS.md) Phase 3 GA requirements

---

**Last updated:** 2026-06-29 · Catalog v1.3.3 · ADR index: [`README.md`](README.md)
