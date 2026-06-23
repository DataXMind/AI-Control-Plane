"""agentctl CLI entrypoint — routing only, no business logic."""

from __future__ import annotations

import typer

from ai_control_plane.cli.apex import app as apex_app
from ai_control_plane.cli.approve import app as approve_app
from ai_control_plane.cli.assign import assign as assign_command
from ai_control_plane.cli.logs import app as logs_app
from ai_control_plane.cli.quota import app as quota_app
from ai_control_plane.cli.status import status as status_command

app = typer.Typer(name="agentctl", help="AI Control Plane CLI")

app.command(name="assign", help="Assign tasks to agents")(assign_command)
app.command(name="status", help="Show task status")(status_command)
app.add_typer(logs_app, name="logs")
app.add_typer(approve_app, name="approve")
app.add_typer(quota_app, name="quota")
app.add_typer(apex_app, name="apex")

__all__ = ["app"]
