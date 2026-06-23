"""agentctl approve — human-in-the-loop approval workflows (Milestone B)."""

from __future__ import annotations

import typer

from ai_control_plane.api.schemas import ApprovalResolveRequest
from ai_control_plane.cli._http import format_json, post_policy_approve


def approve(
    approval_id: str = typer.Argument(..., help="Approval request id"),
    approver: str = typer.Option(..., "--approver", "-u", help="Approver identity"),
    deny: bool = typer.Option(False, "--deny", help="Deny instead of approve"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    """Resolve a pending approval via POST /policy/approve."""
    body = ApprovalResolveRequest(
        approval_id=approval_id,
        approved=not deny,
        approver=approver,
    )
    try:
        decision = post_policy_approve(body)
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    output = {
        "request_id": str(decision.request_id),
        "approved": decision.approved,
        "approver": decision.approver,
    }
    if json_output:
        typer.echo(format_json(output))
    else:
        status = "approved" if decision.approved else "denied"
        typer.echo(f"Approval {status}: {decision.request_id} by {decision.approver}")
