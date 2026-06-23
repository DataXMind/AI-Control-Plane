"""agentctl assign — assign a task to an agent for a project."""

from __future__ import annotations

import json
from typing import Any

import typer

from ai_control_plane.api.schemas import PolicyEvalRequest, TaskRegisterRequest
from ai_control_plane.cli._http import format_json, post_policy_evaluate, post_register_task
from ai_control_plane.config.loader import validate_agent_in_project
from ai_control_plane.core.models import Task


def assign(
    project_id: str = typer.Argument(..., help="Target project id"),
    agent_id: str = typer.Argument(..., help="Assigned agent id"),
    task_type: str = typer.Argument(..., help="Task type / tool name for policy check"),
    payload: str = typer.Option("{}", "--payload", help="JSON task payload"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    """Assign a task after policy evaluation via api/server.py."""
    try:
        task_payload = json.loads(payload)
        if not isinstance(task_payload, dict):
            raise TypeError("payload must be a JSON object")
    except (json.JSONDecodeError, TypeError) as exc:
        typer.echo(f"invalid --payload JSON: {exc}", err=True)
        raise typer.Exit(code=1) from exc

    try:
        agent = validate_agent_in_project(agent_id, project_id)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    role = agent.roles[0] if agent.roles else "backend"

    eval_request = PolicyEvalRequest(
        agent_id=agent_id,
        project_id=project_id,
        tool_name=task_type,
        args={"task_type": task_type, "task_payload": task_payload},
        role=role,
    )

    try:
        decision = post_policy_evaluate(eval_request)
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    if not decision.allowed:
        if json_output:
            typer.echo(
                format_json(
                    {
                        "allowed": False,
                        "reason": decision.reason,
                        "policy_id": decision.policy_id,
                    },
                ),
            )
        else:
            typer.echo(decision.reason, err=True)
        raise typer.Exit(code=1)

    if decision.requires_approval:
        approval_id = decision.policy_id or "pending"
        message = f"Pending approval: {approval_id}"
        if json_output:
            typer.echo(
                format_json(
                    {
                        "status": "pending_approval",
                        "approval_id": approval_id,
                        "reason": decision.reason,
                    },
                ),
            )
        else:
            typer.echo(message)
        raise typer.Exit(code=0)

    task = Task(
        project_id=project_id,
        agent_id=agent_id,
        task_type=task_type,
        payload=task_payload,
    )

    try:
        post_register_task(
            TaskRegisterRequest(
                task_id=task.id,
                project_id=project_id,
                agent_id=agent_id,
                task_type=task_type,
                payload=task_payload,
            ),
        )
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    output: dict[str, Any] = {
        "task_id": str(task.id),
        "project_id": project_id,
        "agent_id": agent_id,
        "task_type": task_type,
        "state": "PENDING",
    }
    if json_output:
        typer.echo(format_json(output))
    else:
        typer.echo(f"Task created: {task.id}")
