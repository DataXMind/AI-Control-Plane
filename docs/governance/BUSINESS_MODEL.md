# ACP Business Model — Decision Record

**Date:** 2026-06-29  
**Status:** DECIDED (pre-GA)  
**Decider:** DataXMind maintainers  
**Baseline:** `master` @ `fdc8542`

## Chosen Model: Option C → Option A (phased)

**Phase 1 (Now → GA):** Developer Tool + Community Free

- Core policy engine + governance framework: MIT, always free
- No agent count limits for community use
- Target: Tier 2 (LLM builders, AI DevOps) — bottom-up adoption

**Phase 2 (GA → GA+6 months):** Enterprise License

- Free for deployments ≤ 100 agents
- Annual license for deployments > 100 agents (per deployment, not per-agent)
- Includes: SLA, email support, security advisory priority
- Target: Tier 1 (Enterprise AI Platform)

**Phase 3 (GA+6 months → GA+18 months):** Open Core

- Core: MIT (policy engine, governance framework, CLI)
- Commercial tier: Multi-tenant SaaS, SSO/SAML, audit export, SIEM integration, managed SAPAL, dedicated support
- Model reference: HashiCorp Vault / Gitea Enterprise pattern

## What Will Always Be Free (Community Commitment)

- `POST /policy/evaluate` — policy engine core
- Karpathy 6-layer governance framework + LESSONS P-01..P-xx
- PACE protocol + SESSION_ANCHOR pattern
- CLI (`agentctl`) full functionality
- Single-tenant self-hosted deployment, any agent count
- All documentation, examples, practice evidence studies

## What Will Be Commercial (Phase 2+)

- Annual license for enterprise deployments > 100 agents (Phase 2)
- Multi-tenant SaaS hosting (Phase 3)
- Enterprise SSO/SAML integration (Phase 3)
- Managed SAPAL with per-tenant model isolation (Phase 3)
- SLA-backed support tiers (Phase 2+)
- Audit export connectors: SIEM, SOC2 evidence packages (Phase 3)

## What This Means for Open Source Contributors

- All contributions to core (MIT) remain free forever
- Contributors retain credit; DataXMind does not claim exclusivity
- Commercial revenue funds continued open source development
- SAPAL ML contributions welcome; training data governance rules apply — see `docs/governance/SAPAL_LEGAL_ASSESSMENT.md` (to be created in Phase 4 of 48h governance plan)

## What This Means for Enterprise Buyers (0.x Beta)

- **Current:** free, no SLA, community support via GitHub Discussions
- Enterprise license available from GA (1.0.0)
- Early adopter program available — contact to discuss beta terms
- **Contact:** `maintainer@dataxmind.com` (mailbox provisioned; live test pending — reference pattern: `practice-evidence/security-email-live-test/RESULTS.md`)

## Review Cadence

- Review at GA (1.0.0) planning — adjust based on community adoption data
- Review at GA+6 months — assess open core readiness
- Owner: DataXMind maintainers
