# ACP Product Positioning — 0.x

**Document ID:** ACP-GOV-POSITIONING-001  
**Date:** 2026-06-29  
**Status:** DECIDED (pre-GA)  
**Baseline:** `master` @ `44a5fef`  
**Related:** [`BUSINESS_MODEL.md`](BUSINESS_MODEL.md)

---

## Primary Identity

**AI Control Plane is an AI Agent Policy Engine** — the policy enforcement layer that sits between AI agents and the resources they act on.

---

## One-Line Pitch (for each audience)

| Audience | Pitch |
|---|---|
| LLM app builder | "Add DENY-by-default policy to your agent's tool calls in 15 minutes" |
| AI DevOps / MLOps | "Governance-as-code for your agent fleet. Policy decisions are auditable, versioned, and fail-closed." |
| Enterprise AI Platform | "The policy enforcement layer your AI agents need before touching production systems." |

---

## What ACP Is (Primary)

- **Policy engine:** evaluates agent action requests against rules → ALLOW/DENY
- **Fail-closed:** unknown agents always denied, API-down always denied
- **Config-driven:** policy rules in version-controlled config, not hardcoded

---

## What ACP Also Includes (Secondary)

- **Governance framework:** Karpathy 6-layer development governance (can be used independently)
- **CLI (`agentctl`):** operator tool for managing agents and inspecting policy state
- **Telemetry:** structured audit log for policy decisions

---

## What ACP Is NOT (Explicit Scope Boundary)

- NOT a content moderation layer (does not inspect LLM output)
- NOT a prompt injection filter
- NOT an observability platform (use LangSmith/W&B alongside ACP)
- NOT an agent orchestrator (use LangGraph/CrewAI alongside ACP)
- NOT a secret manager (use Vault/AWS Secrets alongside ACP)

---

## SAPAL / apex — Experimental (demoted @ 0.x)

**Do not lead with SAPAL in pitches.** The adaptive loop in `apex/` is an **MVP scaffold**, not a proven moat @ 0.x.

| Aspect | Status @ 0.x |
|--------|----------------|
| Moat strength | **Weak** — see [`VALUE_AUDIT_MATRIX.md`](VALUE_AUDIT_MATRIX.md) |
| Public Beta pitch | **Out of scope** — policy engine + governance OS are primary |
| When to mention | v0.3.x+ proposals only; legal posture in [`SAPAL_LEGAL_ASSESSMENT.md`](SAPAL_LEGAL_ASSESSMENT.md) |
| **Packaging decision target** | **Review @ v0.3.0** (calendar 2026-Q3): separate repo vs optional module vs archive — documented in CHANGELOG; **out of Tier 1/2 pitch through 1.0.0-GA** |

Tier 1/2 evaluators should judge ACP on **fail-closed policy + practice evidence**, not SAPAL depth.

---

## Security posture (least agency)

ACP implements **least agency** at the **action layer**: every tool call is evaluated; deny is default on error. This complements (does not replace) harness-level rules, hooks, and MCP minimalism. See [`THREAT_MODEL.md`](THREAT_MODEL.md) §6 and [`ECC_ACP_INTEGRATION_ANALYSIS.md`](ECC_ACP_INTEGRATION_ANALYSIS.md).

---

## Competitive Landscape

### Summary

| Alternative | Difference |
|---|---|
| OPA (Open Policy Agent) | General-purpose Rego; ACP is AI-agent-native (ABAC with agent roles, tool actions) |
| AWS Cedar | Rust, AWS-ecosystem; ACP is Python, cloud-agnostic |
| Casbin | RBAC/ACL library; no agent/project/tool model for AI workloads |
| LangSmith | Observability, not policy enforcement |
| None (custom code) | ACP ships fail-closed default, YAML governance-as-code, practice evidence |

### Feature comparison (action-layer policy)

| Dimension | OPA | Cedar | Casbin | ACP @ 0.x |
|-----------|-----|-------|--------|-----------|
| AI agent / `agent_id` model | Custom attributes | Custom entities | No native model | **Native** (`agents.yml`) |
| Tool / action name evaluation | Via Rego | Via policies | Via matcher | **Native** (`policies.yml`) |
| Project / fleet scope | Custom | Custom | Optional domains | **Native** (`projects.yml`) |
| Fail-closed when engine down | Integrator must implement | Integrator must implement | Integrator must implement | **Contract + SMK-03/04** |
| Governance-as-code (Git YAML) | Yes (bundle) | Yes | Yes (model file) | **Yes** (`ACP_CONFIG_DIR`) |
| HTTP evaluate API (integration) | Sidecar / bundle | Limited | Library embed | **`POST /policy/evaluate`** |
| Content / prompt moderation | Out of scope | Out of scope | Out of scope | **Explicit NOT** |
| Agent orchestration | No | No | No | **Explicit NOT** (use LangGraph/CrewAI) |
| Coding-agent governance OS (Karpathy) | No | No | No | **Secondary product** (optional) |
| Production fleet load SLO @ 0.x | Operator-proven | Operator-proven | Operator-proven | **Not verified** — k6 smoke @ 10 VUs only |

Do not claim superiority without your own benchmark on your workload. See [`LOAD_CHARACTERISTICS.md`](LOAD_CHARACTERISTICS.md) and [`practice-evidence/k6-policy-smoke/`](practice-evidence/k6-policy-smoke/).

---

## Governance Framework — Standalone Value

The Karpathy 6-layer governance + PACE + LESSONS P-01..P-17 can be adopted independently of the policy engine. See [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) (plan referenced `docs/governance/README.md` — not yet published; Karpathy plan is SSOT).

**Target audience:** Teams using AI coding assistants who want structured governance.

---

**Last updated:** 2026-07-02 · Catalog v1.5.0 · SAPAL packaging target v0.3.0
