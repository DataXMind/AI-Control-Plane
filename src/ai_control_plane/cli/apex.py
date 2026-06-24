"""agentctl apex — APEX / SAPAL loop controls (Milestone C)."""

from __future__ import annotations

import json

import typer

from ai_control_plane.cli._http import get_apex_status, post_apex_trigger

app = typer.Typer(help="APEX loop controls")


@app.command("status")
def apex_status() -> None:
    """Fetch GET /apex/status."""
    try:
        body = get_apex_status()
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(body, indent=2, default=str))


@app.command("trigger")
def apex_trigger() -> None:
    """Run POST /apex/trigger to execute one SAPAL cycle."""
    try:
        body = post_apex_trigger()
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc
    typer.echo(json.dumps(body, indent=2, default=str))
