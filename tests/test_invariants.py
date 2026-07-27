"""A7 — machine-enforce the subset of ARCHITECTURE invariants that can be
checked structurally without false positives.

Most of the 8 invariants are convention-level (facade shape, "data contracts
live here") and would need fuzzy heuristics to test — those stay review-gated.
The two below are unambiguous grep-level truths, so CI can hold the line:

  Invariant #1 — `core/` never imports an OSS policy runtime.
  Invariant #4 — `cli/` never imports `core.policies` directly (HTTP only).
"""

from __future__ import annotations

from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src" / "ai_control_plane"

# OSS policy engines the custom PolicyEngine must never be replaced by (Inv #1).
_FORBIDDEN_POLICY_IMPORTS = (
    "cedarpolicy",
    "casbin",
    "oso",
    "py_abac",
    "open_policy_agent",
    "opa_client",
    "openfga",
)


def _python_files(subdir: str) -> list[Path]:
    return sorted((SRC / subdir).rglob("*.py"))


@pytest.mark.parametrize("path", _python_files("core"))
def test_invariant1_core_has_no_oss_policy_engine(path: Path) -> None:
    """Inv #1 — the custom engine is never swapped for an OSS policy runtime."""
    text = path.read_text(encoding="utf-8")
    for pkg in _FORBIDDEN_POLICY_IMPORTS:
        assert f"import {pkg}" not in text, f"{path.name} imports OSS policy engine '{pkg}'"
        assert f"from {pkg}" not in text, f"{path.name} imports OSS policy engine '{pkg}'"


@pytest.mark.parametrize("path", _python_files("cli"))
def test_invariant4_cli_does_not_import_policy_engine(path: Path) -> None:
    """Inv #4 — cli/ speaks to the control plane over HTTP, never in-process policy."""
    text = path.read_text(encoding="utf-8")
    assert "core.policies" not in text, f"{path.name} imports core.policies (Inv #4: HTTP only)"
    assert "from ai_control_plane.core.policies" not in text, (
        f"{path.name} imports core.policies (Inv #4: HTTP only)"
    )
