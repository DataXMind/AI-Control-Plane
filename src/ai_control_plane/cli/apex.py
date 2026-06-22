"""agentctl apex — APEX / SAPAL loop controls (Milestone C)."""

from __future__ import annotations

import typer

app = typer.Typer(help="APEX loop controls", invoke_without_command=True)


@app.callback()
def apex() -> None:
    """Placeholder for APEX pipeline controls."""
    typer.echo("apex: not implemented (Milestone C)")
