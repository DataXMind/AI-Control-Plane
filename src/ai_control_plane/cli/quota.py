"""agentctl quota — inspect project and agent quotas."""

from __future__ import annotations

import typer

app = typer.Typer(help="Quota inspection", invoke_without_command=True)


@app.callback()
def quota(
    project: str | None = typer.Option(None, "--project", "-p"),
) -> None:
    """Placeholder for GET /quota/{project_id}."""
    _ = project
    typer.echo("quota: not implemented (Milestone B)")
