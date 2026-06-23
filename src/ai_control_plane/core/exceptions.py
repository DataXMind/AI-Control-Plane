"""Control-plane domain exceptions — inherit from ControlPlaneError (.cursorrules)."""

from __future__ import annotations


class ControlPlaneError(Exception):
    """Base class for recoverable control-plane domain failures."""


class ConfigError(ControlPlaneError):
    """Config file missing, invalid, or failed validation."""


class PolicyError(ControlPlaneError):
    """Policy rule or evaluation configuration failure."""


class QuotaError(ControlPlaneError):
    """Quota limit enforcement failure."""


class AgentError(ControlPlaneError):
    """Agent registry or identity verification failure."""


class ApprovalError(ControlPlaneError):
    """Approval gate workflow failure."""
