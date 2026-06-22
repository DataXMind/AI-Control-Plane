"""agentctl approve — human-in-the-loop approval workflows (Milestone B)."""

from __future__ import annotations

import typer

app = typer.Typer(help="Approval workflows", invoke_without_command=True)


@app.callback()
def approve(
    approval_id: str | None = typer.Argument(None, help="Approval request id"),
) -> None:
    """Placeholder for approval resolution via api/server.py."""
    _ = approval_id
    typer.echo("approve: not implemented (Milestone B)")
