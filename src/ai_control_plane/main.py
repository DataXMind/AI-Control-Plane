"""agentctl CLI entrypoint — routing only, no business logic."""

from __future__ import annotations

import typer

from ai_control_plane.cli.apex import app as apex_app
from ai_control_plane.cli.approve import approve as approve_command
from ai_control_plane.cli.assign import assign as assign_command
from ai_control_plane.cli.gov import gov_app
from ai_control_plane.cli.logs import logs as logs_command
from ai_control_plane.cli.quota import quota as quota_command
from ai_control_plane.cli.status import status as status_command

app = typer.Typer(name="agentctl", help="AI Control Plane CLI")

app.command(name="assign", help="Assign tasks to agents")(assign_command)
app.command(name="status", help="Show task status")(status_command)
app.command(name="approve", help="Resolve approval requests")(approve_command)
app.command(name="quota", help="Show project quota")(quota_command)
app.command(name="logs", help="Show telemetry audit events")(logs_command)
app.add_typer(gov_app, name="gov")
app.add_typer(apex_app, name="apex")

__all__ = ["app"]
