# Governance Changelog

## Versioning Scheme
`governance_version` uses MAJOR.MINOR.PATCH semantics:
- **MAJOR:** Breaking change to PACE protocol, session anchor format,
  or L0-L5 layer definition
- **MINOR:** New LESSON pattern (P-xx), new gate type,
  new practice evidence category
- **PATCH:** Doc fix, drift correction, reconciliation update,
  clarity improvement, new DOC_LINKS entry

## v1.3.3 (current — 2026-06-28)
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

## Planned: v1.4.0 (Task 5.3 — end of 48h plan)
**Type:** MINOR (planned)
- Will add: All new DOC_LINKS from 48h governance plan
  (THREAT_MODEL, DATA_FLOW, ADR-001, MCP_CONTRACT,
   LOAD_CHARACTERISTICS, BUSINESS_MODEL, PRODUCT_POSITIONING,
   SAPAL_LEGAL, DEPENDENCY_AUDIT, PB12_SUCCESSION, P-14/15/16)
- Will bump: GOVERNANCE_VERSION "1.3.3" → "1.4.0"
- Gate: Task 5.3 only — not before
