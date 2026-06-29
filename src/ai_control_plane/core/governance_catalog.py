"""Governance UX catalog — SSOT for GET /governance/status (read-only, no I/O)."""

from __future__ import annotations

from typing import Any

GOVERNANCE_FRAMEWORK = "6-layer-karpathy"
# Semantic: MAJOR.MINOR.PATCH — see docs/governance/GOVERNANCE_CHANGELOG.md
GOVERNANCE_VERSION = "1.4.0"

VERIFY_GATE_COMMANDS: list[str] = [
    "ruff check src/ tests/",
    "mypy src/ai_control_plane/ --strict",
    "pytest tests/ -v",
    "pytest tests/test_smoke.py -v -m smoke",
    "pytest tests/test_shipped_config_parity.py -v -m shipped_config",
    "pip-audit  # dependency vulnerability scan — see DEPENDENCY_AUDIT.md",
]

DOC_LINKS: dict[str, str] = {
    "architecture": "ARCHITECTURE.md",
    "agents_md": "AGENTS.md",
    "behavioral_constitution": "CLAUDE.md",
    "claude_md": "CLAUDE.md",
    "cursorrules": ".cursorrules",
    "cursor_rules": ".cursor/rules/",
    "risk_policy": "docs/governance/CURSOR_RISK_POLICY.md",
    "cursor_risk_policy": "docs/governance/CURSOR_RISK_POLICY.md",
    "lessons_learned": "docs/governance/LESSONS_LEARNED.md",
    "session_anchor": "docs/prompts/SESSION_ANCHOR_TEMPLATE.md",
    "l5_maturity": "docs/governance/L5_MATURITY_MODEL.md",
    "pre_approval_audit": "docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md",
    "gold_patterns": "docs/governance/gold-patterns/README.md",
    "audit_pass": "docs/governance/GOV_6LAYER_AUDIT_PASS.md",
    "practice_evidence_index": "docs/governance/practice-evidence/README.md",
    "practice_audit": "docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md",
    "ux_runtime": "docs/governance/GOVERNANCE_UX_RUNTIME.md",
    "public_beta_plan": "docs/governance/PUBLIC_BETA_SPRINT_PLAN.md",
    "open_source_readiness": "docs/OPEN_SOURCE_READINESS.md",
    "runbook": "docs/RUNBOOK.md",
    "threat_model": "docs/governance/THREAT_MODEL.md",
    "redis_failure_modes": "docs/governance/REDIS_FAILURE_MODES.md",
    "rollback_protocol": "docs/governance/ROLLBACK_PROTOCOL.md",
    "data_flow": "docs/governance/DATA_FLOW.md",
    "adr_index": "docs/governance/ADR/README.md",
    "adr_001": "docs/governance/ADR/ADR-001-control-data-plane-separation.md",
    "mcp_contract": "docs/governance/MCP_INTEGRATION_CONTRACT.md",
    "load_characteristics": "docs/governance/LOAD_CHARACTERISTICS.md",
    "business_model": "docs/governance/BUSINESS_MODEL.md",
    "product_positioning": "docs/governance/PRODUCT_POSITIONING.md",
    "governance_changelog": "docs/governance/GOVERNANCE_CHANGELOG.md",
    "dependency_audit": "docs/governance/DEPENDENCY_AUDIT.md",
    "sapal_legal": "docs/governance/SAPAL_LEGAL_ASSESSMENT.md",
    "pb12_succession": "docs/governance/PB12_SUCCESSION_PLAN.md",
    "value_audit_matrix": "docs/governance/VALUE_AUDIT_MATRIX.md",
    "developer_scenarios": "docs/DEVELOPER_SCENARIOS.md",
}

LAYER_SUMMARY: dict[str, str] = {
    "L0": "Behavioral — think before coding; P-04 ABAC (see lessons_patterns)",
    "L1": "Context — ARCHITECTURE.md, DATA_CLASSIFICATION.md",
    "L2": "Risk — CURSOR_RISK_POLICY.md (LOW/MED/HIGH/CRITICAL)",
    "L3": "Guardrails — branch isolation; P-01/P-02 (see lessons_patterns)",
    "L4": "Evaluation — ruff, mypy, pytest, smoke, parity",
    "L5": "Memory — LESSONS P-03/P-05/P-07; AGENTS.md; GP-01 (see lessons_patterns)",
}

MILESTONE_STATUS: dict[str, str] = {
    "milestone_a": "CLOSED",
    "milestone_b": "CLOSED",
    "milestone_c": "CLOSED",
    "milestone_c_plus": "CLOSED",
    "public_beta": "IN_PROGRESS",
}

PUBLIC_BETA: dict[str, str | list[str]] = {
    "phase": "PB-9 staging soak",
    "open_issues": "#77-#80",
    "soak_started": "2026-06-22",
    "soak_review_target": "2026-07-06",
    "gates_remaining": [
        "PB-9 calendar soak (G-05)",
        "PB-7 clean-machine fork ≤15 min",
        "PB-10 production soak ≥30d",
        "PB-6 OpenAPI publish on flip",
        "PB-8 v0.1.0-rc.1 tag",
        "security@ mailbox live test (pre-PB-12)",
        "PB-12 human go/no-go",
    ],
    "gates_closed": [
        "PB-11 legal artifacts (SECURITY, CONTRIBUTING, CoC)",
        "docs/RUNBOOK.md operator SSOT",
        "Governance catalog 3-stream convergence",
        "GitHub Discussions enabled",
    ],
}

# Case studies — mapped to LESSONS_LEARNED patterns + operational gates
CASE_STUDIES: list[dict[str, Any]] = [
    {
        "id": "CS-01",
        "title": "Monolithic PR risk",
        "layer": "L3",
        "occurrence": "PR #48, #63 — scope >300 LOC, mixed tasks",
        "runtime_check": "Before merge: count LOC + risk levels in PR template",
        "action": "Split PR; max 300 LOC for HIGH per CURSOR_RISK_POLICY.md",
    },
    {
        "id": "CS-02",
        "title": "Doc-only PR scope creep",
        "layer": "L3",
        "occurrence": "agent4 config in doc-only PR #46",
        "runtime_check": "GET /governance/status → verify doc_links; PR file allowlist",
        "action": "docs-only PR: *.md and docs/** only — no src/",
    },
    {
        "id": "CS-03",
        "title": "GitHub auto-close failure",
        "layer": "L5",
        "occurrence": "PR #63 Closes #52..#62 — only #52 closed",
        "runtime_check": "PR body uses individual Closes #N",
        "action": "Never use issue ranges in PR body",
    },
    {
        "id": "CS-04",
        "title": "Silent policy-loader assumption",
        "layer": "L0",
        "occurrence": "GAP-ABAC-2 — role_not_in handling unclear",
        "runtime_check": "L0 pre-flight: list ABAC keys before loader edits",
        "action": "State assumptions before touching config/loader.py",
    },
    {
        "id": "CS-05",
        "title": "Staging soak gate (PB-9)",
        "layer": "L4",
        "occurrence": "Public Beta blocked until soak ≥14 days",
        "runtime_check": "curl /health + scripts/soak_staging.sh log",
        "action": "Monitor PB9_STAGING_SOAK_LOG.md until 2026-07-06 review",
    },
    {
        "id": "CS-06",
        "title": "Fail-closed policy path",
        "layer": "L4",
        "occurrence": "SMK-04 — unknown agent must deny with reason",
        "runtime_check": "POST /policy/evaluate + smoke SMK-03/04",
        "action": "On API down: TS PolicyClient DENY — no default-allow",
    },
]

# Practice evidence gap registry — synced with PRACTICE_STUDIES_AUDIT_01-07.md
KNOWN_GAPS: list[dict[str, str]] = [
    {
        "id": "G-01",
        "study": "05",
        "title": "Kill switch drill (5g)",
        "severity": "medium",
        "status": "CLOSED",
        "remediation": "study-05/artifacts/terminal-5g-g2-killswitch.md (G2-1)",
    },
    {
        "id": "G-02",
        "study": "05",
        "title": "Stale Docker image (5e)",
        "severity": "low",
        "status": "CLOSED",
        "remediation": "study-05/artifacts/terminal-5e-r-g2-docker.md (G2-2 / 05e-r)",
    },
    {
        "id": "G-03",
        "study": "07",
        "title": "Negative LAN path (7-0n)",
        "severity": "low",
        "status": "CLOSED",
        "remediation": "study-07/artifacts/terminal-7-0n-negative-lan.md (G2-4)",
    },
    {
        "id": "G-04",
        "study": "01-07",
        "title": "CS-01/03/04 process-layer only",
        "severity": "info",
        "status": "CLOSED",
        "remediation": "GOVERNANCE_UX_RUNTIME.md process-layer note (PR #99)",
    },
    {
        "id": "G-05",
        "study": "PB-9",
        "title": "14-day calendar soak",
        "severity": "info",
        "status": "OPEN",
        "remediation": "PB9_STAGING_SOAK_LOG.md daily until 2026-07-06",
    },
    {
        "id": "G-06",
        "study": "08",
        "title": "Profile B remote (shipped config)",
        "severity": "low",
        "status": "CLOSED",
        "remediation": "study-08/artifacts/remote-profile-b-health.json (G2-5)",
    },
    {
        "id": "G-07",
        "study": "08",
        "title": "apex/trigger with shipped config remote",
        "severity": "low",
        "status": "CLOSED",
        "remediation": "study-08/artifacts/remote-profile-b-soak.md (G2-5)",
    },
]

# LESSONS_LEARNED pattern registry (P-01..P-16) — summary only; full prose in markdown SSOT
LESSON_PATTERNS: list[dict[str, Any]] = [
    {
        "id": "P-01",
        "title": "Monolithic PR risk",
        "layer": "L3",
        "status": "ACTIVE",
        "rule_ref": "CURSOR_RISK_POLICY.md F4",
        "case_study_id": "CS-01",
        "prevention": "git diff master --stat | tail -1 → verify LOC",
    },
    {
        "id": "P-02",
        "title": "Scope creep in doc-only PRs",
        "layer": "L3",
        "status": "ACTIVE",
        "rule_ref": "CURSOR_RISK_POLICY.md F11",
        "case_study_id": "CS-02",
        "prevention": "git diff --name-only master → no src/ or tests/",
    },
    {
        "id": "P-03",
        "title": "GitHub auto-close failure (issue ranges)",
        "layer": "L5",
        "status": "ENCODED",
        "rule_ref": "CURSOR_RISK_POLICY.md F6",
        "case_study_id": "CS-03",
        "prevention": 'grep "Closes #.*\\.\\." PR body → 0 matches',
    },
    {
        "id": "P-04",
        "title": "Silent ABAC assumption (role_not_in skip)",
        "layer": "L0",
        "status": "ACTIVE",
        "rule_ref": "CURSOR_RISK_POLICY.md F8",
        "case_study_id": "CS-04",
        "prevention": "List ABAC keys handled vs skipped before loader edits",
    },
    {
        "id": "P-05",
        "title": "Step 7 timing (archive before merge)",
        "layer": "L5",
        "status": "ENCODED",
        "rule_ref": "DEVELOPMENT_PROTOCOL.md §5.6",
        "case_study_id": None,
        "prevention": "Sprint report close commit = post-merge master SHA",
    },
    {
        "id": "P-06",
        "title": "SAPAL scope reduction undocumented",
        "layer": "L2",
        "status": "ENCODED",
        "rule_ref": "CURSOR_RISK_POLICY.md §4",
        "case_study_id": None,
        "prevention": "PR body: Scope reduction: [item] → [milestone] because [reason]",
    },
    {
        "id": "P-07",
        "title": "Doc drift between sprints",
        "layer": "L5",
        "status": "ACTIVE",
        "rule_ref": "DEVELOPMENT_PROTOCOL.md §5.6 Evolve",
        "case_study_id": None,
        "prevention": "Sprint close: ARCHITECTURE.md + README synced to master",
    },
    {
        "id": "P-08",
        "title": "Stale .cursorrules L1 after milestone close",
        "layer": "L5",
        "status": "ENCODED",
        "rule_ref": "ACP_KARPATHY_REARCHITECTURE_PLAN.md R4",
        "case_study_id": None,
        "prevention": "Sprint-close: review .cursorrules milestone status",
    },
    {
        "id": "P-09",
        "title": "Pilot without branch (L3 gap)",
        "layer": "L3",
        "status": "ENCODED",
        "rule_ref": "CURSOR_RISK_POLICY.md §1",
        "case_study_id": None,
        "prevention": "git branch --show-current ≠ master before commit",
    },
    {
        "id": "P-10",
        "title": "Governance UX static-only",
        "layer": "L4",
        "status": "ENCODED",
        "rule_ref": "GOVERNANCE_UX_RUNTIME.md",
        "case_study_id": None,
        "prevention": "agentctl gov status → case_studies CS-01..06",
    },
    {
        "id": "P-11",
        "title": "HTML artifact context drift",
        "layer": "L5",
        "status": "ACTIVE",
        "rule_ref": "GOVERNANCE_DRIFT_RECONCILIATION.md",
        "case_study_id": None,
        "prevention": "Reconcile HTML at each major governance milestone",
    },
    {
        "id": "P-12",
        "title": "WSL2 multi-host ingress (operator)",
        "layer": "L3",
        "status": "STABLE",
        "rule_ref": "study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md",
        "case_study_id": None,
        "prevention": "Study 06 topology before multi-host drills",
    },
    {
        "id": "P-13",
        "title": "Kill switch HTTP contract (counter-intuitive 200 vs 503)",
        "layer": "L2",
        "status": "ENCODED",
        "rule_ref": "CURSOR_RISK_POLICY.md §10; study-05 RUNBOOK §5g",
        "case_study_id": None,
        "prevention": "Alert on allowed=false + kill_switch_active reason, not HTTP 5xx",
    },
    {
        "id": "P-14",
        "title": "Governance Catalog Static Drift",
        "layer": "L5",
        "status": "ACTIVE",
        "rule_ref": (
            "ACP_STATUS_AUDIT_ANALYSIS_RECONCILIATION.md §deeper-perspectives; "
            "GOVERNANCE_CHANGELOG.md"
        ),
        "case_study_id": None,
        "prevention": (
            "Bump → GOVERNANCE_CHANGELOG; gate PASS cites RESULTS.md; "
            "future ADR-001 evidence predicates"
        ),
    },
    {
        "id": "P-15",
        "title": "Soak Load Realism Gap",
        "layer": "L4",
        "status": "ACTIVE",
        "rule_ref": "LOAD_CHARACTERISTICS.md; PUBLIC_BETA_GO_NO_GO.md §SLO",
        "case_study_id": None,
        "prevention": (
            "State p99 with RPS context; load-test at fleet concurrency; "
            "label soak vs load vs chaos"
        ),
    },
    {
        "id": "P-16",
        "title": "Threat Model Absence in Security-Critical Infrastructure",
        "layer": "L2",
        "status": "ACTIVE",
        "rule_ref": "THREAT_MODEL.md; SECURITY.md; GOVERNANCE_CHANGELOG.md §MINOR definition",
        "case_study_id": None,
        "prevention": (
            "STRIDE-lite before public surface; fail-closed ≠ DoS-safe; "
            "update THREAT_MODEL at MINOR bump"
        ),
    },
]

PRACTICE_EVIDENCE: dict[str, str | int | list[str]] = {
    "studies_completed": 8,
    "last_run": "2026-06-26",
    "overall_verdict": "PASS",
    "open_gaps_count": 1,
    "artifacts_count": 45,
    "hosts": ["MSI WSL", "Mac Mini M2", "ubuntu-vps"],
    "network_topologies": ["localhost", "Docker", "LAN", "Tailscale"],
    "note": "Studies 01–08 PASS; PB-9 calendar soak (G-05) separate from one-shot drills.",
    "index_url": "docs/governance/practice-evidence/README.md",
    "audit_url": "docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md",
    "study_08_url": "docs/governance/practice-evidence/study-08-shipped-remote/RESULTS.md",
}

__all__ = [
    "CASE_STUDIES",
    "DOC_LINKS",
    "GOVERNANCE_FRAMEWORK",
    "GOVERNANCE_VERSION",
    "KNOWN_GAPS",
    "LESSON_PATTERNS",
    "LAYER_SUMMARY",
    "MILESTONE_STATUS",
    "PRACTICE_EVIDENCE",
    "PUBLIC_BETA",
    "VERIFY_GATE_COMMANDS",
]
