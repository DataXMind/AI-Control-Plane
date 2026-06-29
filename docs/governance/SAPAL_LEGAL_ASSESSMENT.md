# SAPAL Legal & Regulatory Assessment

**Status:** PRE-IMPLEMENTATION — review required before any SAPAL ML code
**Date:** 2026-06-29
**Baseline:** master @ 1a072e4
**Author:** Architecture review — Claude (Anthropic)
**Operator decisions:** EU users YES · Phase 0 v0.2.x YES

## 1. What SAPAL Does (Planned)

SAPAL (Sense → Analyze → Predict → Act → Learn) is the adaptive
policy learning loop in apex/. Current state (0.x):
- apex/loop.py: SAPAL orchestrator — MVP heuristic, no ML
- apex/learn.py: proposals = [] (stub — human decision: implement)
- apex/act.py: bypasses PolicyEngine for risk_level=high
  (circular dependency — must resolve before ML implementation)

Planned implementation phases: see §3.

## 2. Regulatory Triggers

### 2.1 GDPR (EU General Data Protection Regulation)

**Applies:** ACP targets EU users — GDPR compliance is
MANDATORY for SAPAL implementation, not optional.
Training on behavioral data where agent_id may map to EU
individuals requires lawful basis before any data collection.

**Requirements:**
- Lawful basis required for ML training on personal data
  (Article 6 — legitimate interest or explicit consent)
- Right to erasure (Article 17): if individual requests deletion,
  model weights derived from their data may require retraining
- Data minimization: SAPAL must train on anonymized policy
  outcomes only — never on raw agent_id strings

**Mitigation required before Phase 1:**
- Anonymize agent_id before use as training signal
- Document lawful basis in Privacy Policy
- Implement data deletion capability for training corpus

### 2.2 EU AI Act (Regulation 2024/1689)

**Applies:** ACP targets EU users. SAPAL must undergo conformity
assessment under Annex III given EU user base.
Healthcare/finance domain governance triggers mandatory
high-risk AI system classification.

**Requirements regardless of risk classification:**
- Human oversight mechanism (Article 14) — mandatory
- Explainability of proposals (Article 13)
- Audit trail for every proposal generated and decision made
- Conformity assessment before deployment in EU market

**Non-negotiable:**
- SAPAL proposals MUST NEVER auto-apply without human approval
- Every proposal must include: rationale, affected_rules,
  expected_impact, confidence_score
- Complete audit trail: proposal → human decision → outcome

### 2.3 Multi-Tenant Data Isolation

**Trigger:** Multi-tenancy confirmed for v1.x (human decision).
SAPAL must not learn from Tenant A data to propose policies
affecting Tenant B.

**Requirements:**
- Per-tenant SAPAL models OR federated learning approach
- Training data tagged with tenant_id, never cross-tenant aggregated
- Model weights stored per-tenant, not shared globally
- Explicit opt-in required for any cross-tenant aggregation

**Risk if violated:** Cross-tenant policy leakage via model
weights — GDPR violation + breach of contract with tenants.

### 2.4 Liability for AI-Proposed Policies

**Scenario:** SAPAL proposes policy → operator applies it →
agent causes harm under new policy.

**Position:** ACP is a tool. Operator bears full responsibility
for applied policies. SAPAL proposals are advisory only.

**Required before SAPAL feature flag enabled:**
- Terms of Service: explicit statement that SAPAL proposals
  are advisory — operator assumes full liability for applied changes
- API/UI: proposals labeled "SAPAL suggestion — human review required"
  — never presented as auto-applied or recommended-to-accept

## 3. Safe Implementation Path (Phase-Gated)

### Phase 0 — Prerequisite (v0.2.x — CONFIRMED)
Resolve apex/act.py circular dependency via dependency injection:
- PolicyEngine injected as constructor argument to ActAdapter
- Not imported at module level (current pattern causing bypass)
- Required because act.py currently bypasses PolicyEngine for
  risk_level=high — SAPAL must not inherit this bypass
- Gate: must pass before any data collection begins

### Phase 1 — Observation Only (v0.2.x, after Phase 0)
- Collect anonymized policy evaluation outcomes:
  {action_type, role, decision, latency} — no raw agent_id
- No proposals generated, no ML model trained
- Goal: understand data distribution before model commitment
- GDPR: anonymization pipeline must exist before collection

### Phase 2 — Proposal Generation (v0.3.x)
- Train on Phase 1 corpus (anonymized, per-tenant isolated)
- Proposals include: rationale, affected_rules,
  confidence_score, expected_impact
- Mandatory human review gate — proposals NEVER auto-apply
- Proposal API: GET /apex/proposals (read-only, operator-facing)
- Gate: legal counsel review required before this phase

### Phase 3 — Feedback Loop (v0.4.x)
- Operator marks proposals: accepted / rejected / modified
- Feedback incorporated into next training cycle
- Per-tenant model refinement based on operator decisions
- Cross-tenant aggregation: explicit opt-in + fully anonymized only

### Phase 4 — Multi-Tenant Production (v1.x)
- Per-tenant isolated model storage and training
- Federated learning option for opted-in tenants
- Full audit trail: proposal → human decision → policy outcome
- EU AI Act conformity assessment completed before launch

## 4. Non-Negotiable Requirements

- [ ] SAPAL proposals NEVER auto-apply without explicit human approval
- [ ] Training data anonymization pipeline exists before data collection
- [ ] Per-tenant model isolation from first multi-tenant deployment
- [ ] apex/act.py circular dep resolved (Phase 0, v0.2.x) before Phase 1
- [ ] Terms of Service updated before SAPAL feature flag enabled
- [ ] Legal counsel review before Phase 2 (v0.3.x)
- [ ] EU AI Act conformity assessment before EU market deployment

## 5. Timeline

| Phase | Target | Key Prerequisite |
|---|---|---|
| Phase 0 — act.py DI fix | v0.2.x | Engineering sprint |
| Phase 1 — Observation | v0.2.x (after P0) | Anonymization pipeline + Privacy Policy |
| Phase 2 — Proposals | v0.3.x | Phase 1 corpus + legal counsel sign-off |
| Phase 3 — Feedback | v0.4.x | Phase 2 validated in production |
| Phase 4 — Multi-tenant | v1.x | Phase 3 + per-tenant infra |

Minimum time Phase 0 → Phase 2: 6-9 months from legal counsel engagement.
**Rushing SAPAL without this path = existential regulatory risk.**

## 6. Operator Decisions (Confirmed)

- [x] EU users included: **YES** — GDPR + EU AI Act mandatory
- [x] Phase 0 (act.py DI fix): **v0.2.x** — confirmed
- [ ] Engage legal counsel: target before v0.3.x
- [ ] Jurisdiction: additional regions beyond EU? (document when known)
- [ ] Cross-tenant aggregation as product feature: YES / NO

## 7. Reference Documents

- DATA_FLOW.md — agent_id PII handling and operator responsibility
- THREAT_MODEL.md — policy engine trust model (§T-2 supply chain)
- BUSINESS_MODEL.md — commercial tier includes managed SAPAL (Phase 3+)
- ADR-001 — Control/Data plane separation (Phase 3 prerequisite)
- DEPENDENCY_AUDIT.md — supply chain security context
