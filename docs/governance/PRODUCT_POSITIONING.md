# ACP Product Positioning — 0.x

**Document ID:** ACP-GOV-POSITIONING-001  
**Date:** 2026-06-29  
**Status:** DECIDED (pre-GA)  
**Baseline:** `master` @ `72571db`  
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

## Competitive Landscape

| Alternative | Difference |
|---|---|
| OPA (Open Policy Agent) | OPA is general-purpose; ACP is AI-agent-native (ABAC with agent roles) |
| AWS Cedar | Cedar is Rust, AWS-ecosystem; ACP is Python, cloud-agnostic |
| Casbin | Casbin has no agent model or AI-native concepts |
| LangSmith | Observability, not policy enforcement |
| None (custom code) | ACP provides governance framework, fail-closed default, and audit log out of box |

---

## Governance Framework — Standalone Value

The Karpathy 6-layer governance + PACE + LESSONS P-01..P-13 can be adopted independently of the policy engine. See [`ACP_KARPATHY_REARCHITECTURE_PLAN.md`](ACP_KARPATHY_REARCHITECTURE_PLAN.md) (plan referenced `docs/governance/README.md` — not yet published; Karpathy plan is SSOT).

**Target audience:** Teams using AI coding assistants who want structured governance.

---

**Last updated:** 2026-06-29 · Catalog v1.3.3 · `master` @ `72571db`
