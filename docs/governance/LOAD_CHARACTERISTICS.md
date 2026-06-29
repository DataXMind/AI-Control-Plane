# ACP Load Characteristics & Soak Scope — 0.x

**Document ID:** ACP-GOV-LOAD-CHARS-001  
**Baseline:** `master` @ `cc4e442` · Catalog v1.3.3  
**Related:** [`PB9_STAGING_SOAK_LOG.md`](PB9_STAGING_SOAK_LOG.md) · [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md)

---

## PB-9 Soak — What It Tests vs What It Doesn't

### DOES test

- Service availability over 14 calendar days
- Fail-closed behavior persistence
- Policy evaluation correctness at low load (~1 req/hour automated)
- Disk growth under minimal telemetry write rate
- Redis connection stability over time
- Docker container health — MSI + VPS

### Does NOT test (known scope limitation)

- Concurrent load (multiple agents simultaneously)
- Burst patterns (100+ requests < 1 second)
- Memory behavior under sustained medium load
- Redis eviction under memory pressure
- Policy evaluation latency at realistic production RPS
- Long-tail requests (complex multi-rule evaluation)
- Network partition / split-brain scenarios

---

## Honest SLO Statement

The **p99 < 500ms** target in [`PUBLIC_BETA_GO_NO_GO.md`](PUBLIC_BETA_GO_NO_GO.md) is a **DESIGN TARGET**, not a verified production SLO. It has been assessed at **low load only** (~1 req/hour during PB-9).

**Operator guidance:** If you expect **>10 concurrent agents**, run your own load test before relying on ACP for production decisions. Recommended: **locust** or **k6** against `POST /policy/evaluate` with your expected agent count and request rate.

---

## Planned Load Testing (v0.2.x)

- **Benchmark:** 50 / 100 / 500 concurrent agents
- **Target:** p99 < 200ms at 100 concurrent
- **Tool:** k6 with ACP policy evaluation scenario
- **Issue:** [to be created post-flip]

---

## Soak Architecture Note

Current soak runs on:

- **MSI WSL** — Docker (`examples/minimal/docker-compose.yml`)
- **ubuntu-vps** — systemd (`acp-soak.service`)

These are **developer-grade machines**, not production infrastructure. Production deployment should be sized based on your agent fleet concurrency.

---

**Last updated:** 2026-06-29 · Catalog v1.3.3 · `master` @ `cc4e442`
