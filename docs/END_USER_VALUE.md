# End-User Value Map — Four Doors + Three Products

**Document ID:** ACP-END-USER-VALUE-001  
**Audience:** Evaluators, integrators, operators, gov adopters, architects  
**Baseline:** `master` @ `aeca32a` · catalog **v1.5.0** · **17** LESSON patterns · pytest **221** · smoke **8/8**  
**SSOT:** [`governance/VALUE_AUDIT_MATRIX.md`](governance/VALUE_AUDIT_MATRIX.md) · [`governance/PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md)

> **Positioning invariant:** Product A (policy engine) is the **primary pitch**. Products B/C are **optional** — CONNECT and RUN doors do **not** require Karpathy 6-layer or ECC depth.

---

## One-line pitch (Product A)

AI Control Plane is an **AI Agent Policy Engine** — before every tool call (git, Kubernetes, build), ask ACP **"allowed?"** Rules live in version-controlled YAML. **Fail-closed** by default.

---

## Four doors (read order)

| Door | You are… | Start here | Required for Tier 1–2? |
|------|----------|------------|------------------------|
| **RUN** | Evaluator — try in 5 min | [`QUICKSTART.md`](QUICKSTART.md) § RUN | Yes (eval only) |
| **CONNECT** | Integrator — wire HTTP into app | [`CLIENT_INTEGRATION.md`](CLIENT_INTEGRATION.md) | Yes (integration) |
| **GOVERN** | Gov adopter — agent team discipline | [`prompts/AGENT_OPERATING_SYSTEM.md`](prompts/AGENT_OPERATING_SYSTEM.md) | **No** — optional Tier 3 |
| **ARCHITECT** | Security / harness vs policy boundary | [`governance/ECC_ACP_LAYER_MAP.md`](governance/ECC_ACP_LAYER_MAP.md) | **No** — advanced only |

**Operator (Task 1 — host ACP):** [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) — not a fifth door; parallel path for whoever runs the API.

**Gateway + Antigravity:** [`integrations/HYBRID_AI_GATEWAY.md`](integrations/HYBRID_AI_GATEWAY.md) — **ACP CONNECT PASS** @ `aeca32a` ([#188](https://github.com/DataXMind/AI-Control-Plane/pull/188)); enforce via [`examples/integrate/python/run_tool_guarded.py`](../examples/integrate/python/run_tool_guarded.py). Evidence: [`practice-evidence/hybrid-gateway-acp-integration/RESULTS.md`](governance/practice-evidence/hybrid-gateway-acp-integration/RESULTS.md). Gateway repo PR wire: **open** (see PR spec). Dog-fooding case study: **post-implementation** in Gateway repo.

**Procurement / “why not OPA?”** [`governance/PRODUCT_POSITIONING.md`](governance/PRODUCT_POSITIONING.md) §Feature comparison.

**Policy change safety:** staging evaluate-before-apply — [`examples/minimal/CUSTOMER_INSTALL.md`](../examples/minimal/CUSTOMER_INSTALL.md) §12. Code dry-run tracked: [#184](https://github.com/DataXMind/AI-Control-Plane/issues/184).

**Incidents / rollback:** [`governance/ROLLBACK_PROTOCOL.md`](governance/ROLLBACK_PROTOCOL.md) (operator-owned).

---

## Three products in one repo (iceberg)

| Product | Question it answers | Runtime | Visibility @ 0.x |
|---------|---------------------|---------|------------------|
| **A — Policy Engine** | "May this agent call this tool?" | `POST /policy/evaluate` | **Surface** — README, QUICKSTART |
| **B — Governance OS** | "How should coding agents work on this repo?" | Rules in `.cursorrules`, CI, session anchor; catalog via `GET /governance/status` | **Hidden** — Tier 3 |
| **C — ECC 48H boundary** | "Harness vs policy engine — where is the line?" | Doc + P-17; **no** ECC plugin | **Hidden** — architect |

**Bridge:** [`ECC_ACP_LAYER_MAP.md`](governance/ECC_ACP_LAYER_MAP.md) maps ECC concepts → Karpathy L0–L5.

**Export pattern (copy to other repos):** [`governance/gold-patterns/GP-01-agent-session-memory.md`](governance/gold-patterns/GP-01-agent-session-memory.md).

---

## Evidence (honest counts)

| Corpus | Count / status | SSOT |
|--------|----------------|------|
| Core practice studies | **8** (`studies_completed` in catalog) — Studies **01–08** | [`practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md`](governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md) |
| Study 09 MCP inventory | **PASS** (separate from catalog `8`) | [`practice-evidence/study-09-mcp-inventory/`](governance/practice-evidence/study-09-mcp-inventory/) |
| k6 load smoke (P-15) | **PASS** @ 10 VUs — not fleet SLO | [`practice-evidence/k6-policy-smoke/`](governance/practice-evidence/k6-policy-smoke/) |
| ECC 48H post-verify | **PASS** | [`practice-evidence/ecc-48h-post-verify/`](governance/practice-evidence/ecc-48h-post-verify/) |
| PB-9 calendar soak | **IN PROGRESS** — ~1 req/hour, not load test | [`governance/PB9_STAGING_SOAK_LOG.md`](governance/PB9_STAGING_SOAK_LOG.md) |

Do **not** claim PB-9 or k6 @ 10 VUs replaces production fleet load proof. See [`governance/LOAD_CHARACTERISTICS.md`](governance/LOAD_CHARACTERISTICS.md).

---

## What you can skip

| Persona | Read first | Skip (unless you need it) |
|---------|------------|---------------------------|
| Evaluator 5 min | QUICKSTART RUN/CONNECT | Karpathy plan, 84× `docs/governance/` |
| Integrator | CLIENT_INTEGRATION | Full `.cursorrules`, AOS |
| Operator host | CUSTOMER_INSTALL | ECC plugin (none shipped) |
| Cursor agent on repo | AOS → [`ANCHOR_CURRENT.md`](prompts/ANCHOR_CURRENT.md) | Historical HTML governance artifacts |
| Architect due diligence | PRODUCT_POSITIONING (competitive table) + THREAT_MODEL + GOV_6LAYER_AUDIT_PASS | SAPAL depth for Tier 1/2 pitch |

---

## Maturity @ 0.x (plain language)

| Question | Answer |
|----------|--------|
| Pilot / internal try? | **Yes** — Mac Tier A pilot PASS, PB-7 ≤15 min PASS |
| Unmonitored production? | **Not recommended** — 0.x beta |
| Public repo? | **Conditional** — PB-12 ~2026-07-10 after PB-9 Day 14 ~2026-07-06 |
| Enterprise SLA? | After GA 1.0.0 — PB-10 deferred (#78) |

Runtime check: `GET /governance/status` → `framework: "6-layer-karpathy"`, `governance_version: "1.5.0"`, **17** `lessons_patterns`.

---

**Last updated:** 2026-07-02 · baseline `44a5fef` (#183, #185) · Sonnet audit drift-close
