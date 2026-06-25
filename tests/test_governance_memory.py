"""L5 / ML5 agent memory pack verification."""

from __future__ import annotations

import subprocess
from pathlib import Path

from fastapi.testclient import TestClient

from ai_control_plane.api.server import create_app
from ai_control_plane.core.governance_catalog import DOC_LINKS

REPO_ROOT = Path(__file__).resolve().parents[1]


def test_verify_governance_memory_script_exits_zero() -> None:
    script = REPO_ROOT / "scripts" / "verify_governance_memory.sh"
    result = subprocess.run(
        ["bash", str(script)],
        cwd=REPO_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0, result.stderr or result.stdout


def test_governance_status_includes_ml5_doc_links() -> None:
    client = TestClient(create_app())
    response = client.get("/governance/status")
    assert response.status_code == 200
    doc_links = response.json()["doc_links"]
    for key in ("agents_md", "session_anchor", "gold_patterns", "l5_maturity", "cursor_rules", "pre_approval_audit"):
        assert key in doc_links
        assert key in DOC_LINKS


def test_agents_md_and_cursor_rules_exist() -> None:
    assert (REPO_ROOT / "AGENTS.md").is_file()
    rules = list((REPO_ROOT / ".cursor" / "rules").glob("*.mdc"))
    assert len(rules) >= 4


def test_gp01_gold_pattern_exists() -> None:
    gp = REPO_ROOT / "docs" / "governance" / "gold-patterns" / "GP-01-agent-session-memory.md"
    assert gp.is_file()
    assert "session_anchor" in gp.read_text(encoding="utf-8")
