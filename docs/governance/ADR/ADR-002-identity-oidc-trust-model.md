# ADR-002: Identity / OIDC Trust Model

**Status:** PROPOSED (not IMPLEMENTED)  
**Date:** 2026-06-30  
**Deciders:** DataXMind maintainers (pending)  
**Baseline:** `master` @ `a493e98` · catalog v1.5.0

> **STATUS: PROPOSED — implementation sau PB-12 flip (~2026-07-10), không kích hoạt trước**

---

## Context

ACP 0.x authenticates agent identity on `POST /identity/verify` and policy paths using:

- **HS256 dev stub** when `ACP_JWKS_URL` is unset (local / fixture / smoke)
- **JWKS RS256** when `ACP_JWKS_URL` is set (`core/identity.py` — Milestone B)

**Risk (THREAT_MODEL §S-1):** An agent (or compromised client) may **spoof another agent's identity** if callers trust `role` / `agent_id` supplied only in the **request body** without cryptographic binding to a verified token. ABAC would then evaluate the **wrong role** — fail-closed still applies on deny paths, but **wrong allow** is possible when rules are role-sensitive.

Related: [`THREAT_MODEL.md`](../THREAT_MODEL.md) S-1 · SMK-06/06b/06c · [`DATA_CLASSIFICATION.md`](../../DATA_CLASSIFICATION.md) (JWT RESTRICTED).

---

## Decision options (not chosen yet)

| Option | Summary | Target |
|--------|---------|--------|
| **(a) JWKS required in production** | `ACP_JWKS_URL` mandatory when `ACP_ENV=production`; reject unsigned/stub tokens | v0.2.x post-flip |
| **(b) mTLS agent identity** | Client cert binds agent_id; complements token auth | v0.3.x (THREAT_MODEL planned mitigation) |
| **(c) OIDC federation** | Multi-tenant IdP (enterprise SSO); map claims → `AgentIdentity` | v0.3.x+ pilot-driven |

**0.x position:** No option is implemented. JWKS remains **optional** to preserve fork-friendly local dev and smoke gate.

---

## Module impact

| Module | Impact if implemented | Notes |
|--------|----------------------|-------|
| `api/server.py` | Identity verify + policy evaluate ingress | Validate token before trusting body fields |
| `core/models.py` | `AgentIdentity` | May add `idp_issuer`, `tenant_id` — **Invariant #2** |
| `config/` | JWT / OIDC settings | New env vars; shipped defaults unchanged for 0.x |
| `MCP_INTEGRATION_CONTRACT.md` | `agent_id` provenance | MCP adapter must not invent role without token |
| `cli/` | HTTP-only | Token forwarding via env / config |
| **`core/policies.py`** | **No change** | ABAC engine already role-aware; trust boundary is **identity layer** |
| `tests/test_jwks_identity.py` | Extend coverage | No change until implementation PR |

---

## Backward compatibility constraint

- `ACP_JWKS_URL` **must remain optional** for 0.x local dev, CI smoke, and fixture config.
- Fail-closed default **unchanged:** missing/invalid identity → deny; never default-allow on error.
- Shipped `examples/minimal` and `tests/fixtures/config` must work **without** external IdP.

---

## Rejection criteria

Do **not** implement identity/OIDC work unless:

1. **PB-12 flip** completed and maintainer opens a dedicated identity branch, **and**
2. At least **one enterprise pilot** explicitly requires **multi-tenant** or production IdP federation.

Absent (2), option (a) JWKS-required-production may suffice as a smaller follow-up — still requires maintainer approval.

---

## Effort estimate

**Multi-sprint** (not one PR): schema + config + API contract + parity tests + operator runbook + THREAT_MODEL update. Expect 3–5 PRs minimum post-flip.

---

## Related

- ADR-001 (control/data plane) — identity hot path stays on Data Plane in v0.3.x split
- [`ECC_ACP_INTEGRATION_ANALYSIS.md`](../ECC_ACP_INTEGRATION_ANALYSIS.md) — harness vs policy boundary
- [`SESSION_ANCHOR_TEMPLATE.md`](../../prompts/SESSION_ANCHOR_TEMPLATE.md) §Drift guard

---

**Activation:** Chỉ mở implementation task sau khi (1) PB-12 flip xong, (2) maintainer approve branch riêng cho identity work.

**Last updated:** 2026-06-30 · ADR index: [`README.md`](README.md)
