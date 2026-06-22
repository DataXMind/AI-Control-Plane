"""agentctl logs — stream or query audit logs (Milestone B)."""

from __future__ import annotations

import typer

app = typer.Typer(help="Audit and telemetry logs", invoke_without_command=True)


@app.callback()
def logs(
    project: str | None = typer.Option(None, "--project", "-p"),
    follow: bool = typer.Option(False, "--follow", "-f"),
) -> None:
    """Placeholder for log streaming."""
    _ = (project, follow)
    typer.echo("logs: not implemented (Milestone B)")
