# Governance Changelog

## Versioning Scheme
`governance_version` uses MAJOR.MINOR.PATCH semantics:
- **MAJOR:** Breaking change to PACE protocol, session anchor format,
  or L0-L5 layer definition
- **MINOR:** New LESSON pattern (P-xx), new gate type,
  new practice evidence category
- **PATCH:** Doc fix, drift correction, reconciliation update,
  clarity improvement, new DOC_LINKS entry

## v1.4.0 (current — 2026-06-30)
**Type:** MINOR
- Added: THREAT_MODEL.md (P-16 resolved)
- Added: REDIS_FAILURE_MODES.md (C2 resolved)
- Added: ROLLBACK_PROTOCOL.md (A3 resolved)
- Added: DATA_FLOW.md (A2 resolved)
- Added: ADR-001 Control/Data Plane Separation (C1 documented)
- Added: MCP_INTEGRATION_CONTRACT.md (C4 resolved)
- Added: LOAD_CHARACTERISTICS.md (C3/P-15 resolved)
- Added: BUSINESS_MODEL.md (F1/F3 decision)
- Added: PRODUCT_POSITIONING.md (F1 resolved)
- Added: SAPAL_LEGAL_ASSESSMENT.md (F3 resolved)
- Added: GOVERNANCE_CHANGELOG.md (E2 resolved)
- Added: DEPENDENCY_AUDIT.md (A5 documented)
- Added: PB12_SUCCESSION_PLAN.md (E4 resolved)
- Updated: LESSONS_LEARNED.md P-14/P-15/P-16
- Updated: SECURITY.md threat surfaces
- Updated: CONTRIBUTING.md quick-start onramp
- Updated: README.md positioning + 177 tests
- Added: `docs/DEVELOPER_SCENARIOS.md` (fork/clone + client usage); `DOC_LINKS.developer_scenarios`
- Added: `docs/QUICKSTART.md` (RUN/CONNECT); `examples/integrate/`; `DOC_LINKS.quickstart`
- Added: `scripts/acp-up.sh`, `docker-compose.ghcr.yml`, GHCR publish workflow (demo image)

## v1.3.3 (2026-06-28)
**Type:** PATCH
- Fixed: SESSION_ANCHOR_TEMPLATE.md synced to master @ 20e4fc3
- Fixed: TASK_AUDIT baseline SHA corrected (527eb5d → 20e4fc3)
- Fixed: PB9_DAY14_REVIEW_TEMPLATE "proceed PB-8" → "PB-12 prep only"
- Added: Full technical audit report PROJECT_STATUS_FULL_TECHNICAL_REPORT
- Added: VPS hourly verify + session anchor sync

## v1.3.2 (2026-06-27)
**Type:** PATCH
- Added: PB-7 CLEAN PASS evidence (Ubuntu @ MSI)
- Added: security@ live test PASS
- Added: VPS soak CUR-04 hourly verify
- Added: PR #119 go/no-go practice sync
- Added: PR #120 CHANGELOG expand

## v1.3.1 (2026-06-26)
**Type:** PATCH
- Added: PB-9 soak evidence window opened (first iteration)
- Fixed: Gap 2026-06-22→25 documented in soak log

## v1.3.0 (2026-06-24)
**Type:** MINOR
- Added: Catalog 3-stream convergence (gates_remaining 7)
- Added: Case studies CS-01..CS-06
- Added: LESSONS P-01..P-13
- Added: practice_evidence studies 1-8 tracking

## v1.2.x → v1.0.x (historical)
Milestones A → C+ governance maturity progression.
See docs/governance/LESSONS_LEARNED.md for full pattern history.
