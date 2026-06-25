"""Governance UX catalog — SSOT for GET /governance/status (read-only, no I/O)."""

from __future__ import annotations

from typing import Any

GOVERNANCE_FRAMEWORK = "6-layer-karpathy"
GOVERNANCE_VERSION = "1.0"

VERIFY_GATE_COMMANDS: list[str] = [
    "ruff check src/ tests/",
    "mypy src/ai_control_plane/ --strict",
    "pytest tests/ -v",
    "pytest tests/test_smoke.py -v -m smoke",
    "pytest tests/test_shipped_config_parity.py -v -m shipped_config",
]

DOC_LINKS: dict[str, str] = {
    "architecture": "ARCHITECTURE.md",
    "cursorrules": ".cursorrules",
    "risk_policy": "docs/governance/CURSOR_RISK_POLICY.md",
    "lessons_learned": "docs/governance/LESSONS_LEARNED.md",
    "audit_pass": "docs/governance/GOV_6LAYER_AUDIT_PASS.md",
    "ux_runtime": "docs/governance/GOVERNANCE_UX_RUNTIME.md",
    "public_beta_plan": "docs/governance/PUBLIC_BETA_SPRINT_PLAN.md",
}

LAYER_SUMMARY: dict[str, str] = {
    "L0": "Behavioral — think before coding, simplicity, surgical, goal-driven",
    "L1": "Context — ARCHITECTURE.md, DATA_CLASSIFICATION.md",
    "L2": "Risk — CURSOR_RISK_POLICY.md (LOW/MED/HIGH/CRITICAL)",
    "L3": "Guardrails — branch isolation, file allowlists, invariants",
    "L4": "Evaluation — ruff, mypy, pytest, smoke, parity",
    "L5": "Memory — LESSONS_LEARNED.md, governance HTML archive",
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

__all__ = [
    "CASE_STUDIES",
    "DOC_LINKS",
    "GOVERNANCE_FRAMEWORK",
    "GOVERNANCE_VERSION",
    "LAYER_SUMMARY",
    "MILESTONE_STATUS",
    "PUBLIC_BETA",
    "VERIFY_GATE_COMMANDS",
]
