# ACP Threat Model — 0.x Beta

**Version:** 0.1 (aligned with governance catalog v1.3.3)  
**Methodology:** STRIDE-lite (Spoofing, Tampering, Repudiation, DoS, Elevation)  
**Scope:** `POST /policy/evaluate` · `GET /health` · Redis layer · Agent identity  
**Out of scope:** LLM output content, prompt injection, user-facing application layer

---

## 1. Trust Boundaries

| Boundary | From | To | Trust Level |
|----------|------|-----|-------------|
| TB-1 | AI Agent | ACP Policy Engine | Authenticated (token) |
| TB-2 | ACP Policy Engine | Redis | Internal network only |
| TB-3 | Operator | ACP via agentctl/API | Admin token |
| TB-4 | ACP | Downstream resources | N/A (ACP advises, does not act) |

---

## 2. STRIDE Analysis

### S — Spoofing

- **S-1:** Agent spoofs another agent's identity → ABAC evaluates wrong role
  - Likelihood: MEDIUM (token theft possible)
  - Impact: HIGH (wrong policy applied)
  - Mitigation 0.x: Token-based auth (SMK-06/06b/06c). No mTLS.
  - Mitigation planned: mTLS agent identity v0.3.x

### T — Tampering

- **T-1:** Redis policy cache poisoned
  - Likelihood: LOW (requires Redis access)
  - Impact: HIGH (all agents get wrong policy)
  - Mitigation 0.x: Redis AUTH required. TLS recommended.
- **T-2:** `governance_catalog.py` tampered in supply chain
  - Likelihood: LOW (dependency audit in CI policy — see `DEPENDENCY_AUDIT.md` when published)
  - Impact: CRITICAL (governance state corrupted)
  - Mitigation 0.x: Pin dependencies. Verify CI SHA.

### R — Repudiation

- **R-1:** Agent denies making policy-violating call
  - Likelihood: MEDIUM
  - Impact: MEDIUM (audit gap)
  - Mitigation 0.x: Structlog records `agent_id` + decision per request.
  - Gap: Log integrity not cryptographically guaranteed in 0.x.

### D — Denial of Service

- **D-1:** Flood `POST /policy/evaluate` → fail-closed → agent fleet halted
  - Likelihood: HIGH (no rate limiting in 0.x)
  - Impact: CRITICAL (all agents stop working)
  - Mitigation 0.x: Deploy behind nginx with rate limiting (operator responsibility).
  - Mitigation planned: Built-in rate limiting v0.2.x
- **D-2:** Redis unavailable → ACP fail-closed
  - Likelihood: LOW
  - Impact: HIGH
  - Mitigation 0.x: Operator monitors Redis health. `acp-soak.service` alerts on failure.

### E — Elevation of Privilege

- **E-1:** Low-privilege agent obtains admin token
  - Likelihood: LOW
  - Impact: CRITICAL
  - Mitigation 0.x: Token scoping in ABAC config. Separate admin vs agent tokens.

---

## 3. Residual Risks Accepted for 0.x Beta

| Risk | Acceptance Rationale | GA Mitigation |
|------|----------------------|---------------|
| No rate limiting | 0.x beta; operator-managed via proxy | v0.2.x built-in |
| No mTLS agent identity | Token auth sufficient for beta | v0.3.x |
| No log integrity guarantee | Beta use case; not forensic-grade | v1.x with signed logs |
| Single-tenant only | Multi-tenancy in scope for v1.x | v1.x |

---

## 4. Assets to Protect (Priority Order)

1. Policy decision integrity (fail-closed contract)
2. Agent identity (ABAC correct role assignment)
3. Redis policy cache (correctness)
4. Governance catalog (tamper evidence)
5. Telemetry/audit log (completeness)

---

## 5. Review Cadence

- Review with each minor version bump (0.x → 0.x+1)
- Mandatory re-review before GA (1.0.0)
- Owner: DataXMind security@ · SSOT: this file

---

## 6. Least agency and harness context (48H)

**Principle (adapted from industry harness security practice):** The real safety boundary is **policy between model intent and action** — not system prompt alone.

| Concept | ACP interpretation |
|---------|-------------------|
| **Least agency** | Agents get minimum tool scope; `/policy/evaluate` is the enforcement gate |
| **Lethal trifecta** | Private data + untrusted content + outbound tools in one runtime → high injection risk |
| **ACP scope** | We enforce **tool/action** gate (TB-1); we do **not** inspect LLM output (out of scope) |

**Operator pairing:** Use ACP with harness configs that minimize default MCP connectors ([`MCP_INTEGRATION_CONTRACT.md`](MCP_INTEGRATION_CONTRACT.md)). Prompt safety without action policy is insufficient for production agents.

**Integration SSOT:** [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md)

---

**Last updated:** 2026-06-30 · Catalog v1.5.0
