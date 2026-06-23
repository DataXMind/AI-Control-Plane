"""Unit tests for core/models.py data contracts (Issue #21)."""

from __future__ import annotations

import pytest
from pydantic import ValidationError

from ai_control_plane.core.models import (
    AgentConfig,
    AgentIdentity,
    PolicyDecision,
    PolicyRule,
    ProjectConfig,
    Task,
    TaskState,
    TaskStatus,
    TelemetryEvent,
)


def test_project_config_is_frozen(sample_project_config: ProjectConfig) -> None:
    with pytest.raises(ValidationError):
        sample_project_config.id = "other"  # type: ignore[misc]


def test_agent_config_fields() -> None:
    agent = AgentConfig(
        id="agent2",
        name="backend-runner",
        roles=["backend"],
        runner="local",
        model_profile="claude-pro-backend",
        capabilities=["git"],
        restrictions=[],
    )
    assert agent.id == "agent2"
    assert "backend" in agent.roles


def test_policy_rule_allow_deny_literals() -> None:
    allow = PolicyRule(
        name="allow-git",
        description="",
        conditions={"role": "backend"},
        effect="allow",
    )
    deny = PolicyRule(
        name="deny-pii",
        description="",
        conditions={"data_category": "PII"},
        effect="deny",
    )
    assert allow.effect == "allow"
    assert deny.effect == "deny"


def test_task_status_progress_bounds() -> None:
    from uuid import uuid4

    task_id = uuid4()
    ok = TaskStatus(task_id=task_id, state=TaskState.RUNNING, progress=50)
    assert ok.progress == 50

    with pytest.raises(ValidationError):
        TaskStatus(task_id=task_id, state=TaskState.RUNNING, progress=101)

    with pytest.raises(ValidationError):
        TaskStatus(task_id=task_id, state=TaskState.RUNNING, progress=-1)


def test_telemetry_event_hash_fields_default() -> None:
    event = TelemetryEvent(
        event_type="tool.call",
        agent_id="agent2",
        project_id="rust-gateway",
        payload={},
    )
    assert event.event_hash == ""
    assert event.previous_hash is None
    assert event.event_id != ""


def test_policy_decision_fail_closed_shape() -> None:
    decision = PolicyDecision(
        allowed=False,
        reason="unknown agent",
        requires_approval=False,
        policy_id=None,
    )
    assert decision.allowed is False
    assert decision.reason != ""


def test_agent_identity_from_fixture(backend_identity: AgentIdentity) -> None:
    assert backend_identity.agent_id == "agent2"
    assert backend_identity.project_id == "rust-gateway"
    assert backend_identity.role == "backend"


def test_task_generates_uuid_and_timestamp() -> None:
    task = Task(
        project_id="rust-gateway",
        agent_id="agent2",
        task_type="git_read",
        payload={"path": "src/"},
    )
    assert task.id is not None
    assert task.created_at.tzinfo is not None
