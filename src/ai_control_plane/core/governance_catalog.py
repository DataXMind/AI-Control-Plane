"""Governance UX catalog — SSOT for GET /governance/status (read-only, no I/O)."""

from __future__ import annotations

from typing import Any

GOVERNANCE_FRAMEWORK = "6-layer-karpathy"
GOVERNANCE_VERSION = "1.2.1"

VERIFY_GATE_COMMANDS: list[str] = [
    "ruff check src/ tests/",
    "mypy src/ai_control_plane/ --strict",
    "pytest tests/ -v",
    "pytest tests/test_smoke.py -v -m smoke",
    "pytest tests/test_shipped_config_parity.py -v -m shipped_config",
]

DOC_LINKS: dict[str, str] = {
    "architecture": "ARCHITECTURE.md",
    "agents_md": "AGENTS.md",
    "cursorrules": ".cursorrules",
    "cursor_rules": ".cursor/rules/",
    "risk_policy": "docs/governance/CURSOR_RISK_POLICY.md",
    "lessons_learned": "docs/governance/LESSONS_LEARNED.md",
    "session_anchor": "docs/prompts/SESSION_ANCHOR_TEMPLATE.md",
    "l5_maturity": "docs/governance/L5_MATURITY_MODEL.md",
    "pre_approval_audit": "docs/governance/GOVERNANCE_NEXT_PHASE_PRE_APPROVAL_AUDIT.md",
    "gold_patterns": "docs/governance/gold-patterns/README.md",
    "audit_pass": "docs/governance/GOV_6LAYER_AUDIT_PASS.md",
    "claude_md": "CLAUDE.md",
    "practice_audit": "docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md",
    "ux_runtime": "docs/governance/GOVERNANCE_UX_RUNTIME.md",
    "public_beta_plan": "docs/governance/PUBLIC_BETA_SPRINT_PLAN.md",
}

LAYER_SUMMARY: dict[str, str] = {
    "L0": "Behavioral — think before coding, simplicity, surgical, goal-driven",
    "L1": "Context — ARCHITECTURE.md, DATA_CLASSIFICATION.md",
    "L2": "Risk — CURSOR_RISK_POLICY.md (LOW/MED/HIGH/CRITICAL)",
    "L3": "Guardrails — branch isolation, file allowlists, invariants",
    "L4": "Evaluation — ruff, mypy, pytest, smoke, parity",
    "L5": "Memory — LESSONS_LEARNED.md, AGENTS.md, .cursor/rules/, GP-01 gold pattern",
}

MILESTONE_STATUS: dict[str, str] = {
    "milestone_a": "CLOSED",
    "milestone_b": "CLOSED",
    "milestone_c": "CLOSED",
    "milestone_c_plus": "CLOSED",
    "public_beta": "IN_PROGRESS",
}

PUBLIC_BETA: dict[str, str] = {
    "phase": "PB-9 staging soak",
    "open_issues": "#77-#80",
    "soak_started": "2026-06-22",
    "soak_review_target": "2026-07-06",
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
        "status": "OPEN",
        "remediation": "Study 08: rules=10 on remote endpoint (ubuntu-vps)",
    },
    {
        "id": "G-07",
        "study": "08",
        "title": "apex/trigger with shipped config remote",
        "severity": "low",
        "status": "OPEN",
        "remediation": "Study 08 soak with unset ACP_CONFIG_DIR",
    },
]

PRACTICE_EVIDENCE: dict[str, str | int] = {
    "studies_completed": 7,
    "last_run": "2026-06-25",
    "overall_verdict": "PASS",
    "index_url": "docs/governance/practice-evidence/README.md",
    "audit_url": "docs/governance/practice-evidence/PRACTICE_STUDIES_AUDIT_01-07.md",
}

__all__ = [
    "CASE_STUDIES",
    "DOC_LINKS",
    "GOVERNANCE_FRAMEWORK",
    "GOVERNANCE_VERSION",
    "KNOWN_GAPS",
    "LAYER_SUMMARY",
    "MILESTONE_STATUS",
    "PRACTICE_EVIDENCE",
    "PUBLIC_BETA",
    "VERIFY_GATE_COMMANDS",
]
