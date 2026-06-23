"""Tests for ControlPlaneError hierarchy (#3)."""

from __future__ import annotations

from ai_control_plane.core.exceptions import (
    AgentError,
    ApprovalError,
    ConfigError,
    ControlPlaneError,
    PolicyError,
    QuotaError,
)


def test_exception_hierarchy() -> None:
    assert issubclass(ConfigError, ControlPlaneError)
    assert issubclass(PolicyError, ControlPlaneError)
    assert issubclass(QuotaError, ControlPlaneError)
    assert issubclass(AgentError, ControlPlaneError)
    assert issubclass(ApprovalError, ControlPlaneError)


def test_config_error_message() -> None:
    err = ConfigError("policies file not found")
    assert str(err) == "policies file not found"
