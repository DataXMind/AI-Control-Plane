"""agentctl status — show task/agent run status."""

from __future__ import annotations

import time

import typer
from rich.console import Console
from rich.table import Table

from ai_control_plane.cli._http import get_project_status
from ai_control_plane.config.loader import load_projects


def _render_table(rows: list[dict[str, str]], *, clear: bool = False) -> None:
    console = Console()
    if clear:
        console.clear()
    table = Table(title="Task Status")
    table.add_column("Project", style="cyan")
    table.add_column("Task ID", style="green")
    table.add_column("State", style="yellow")
    table.add_column("Progress", justify="right")
    table.add_column("Updated At")

    for row in rows:
        table.add_row(
            row["project"],
            row["task_id"],
            row["state"],
            row["progress"],
            row["updated_at"],
        )

    console.print(table)


def _fetch_status(project_id: str, agent_filter: str | None) -> dict[str, str]:
    status = get_project_status(project_id)
    if agent_filter is not None:
        # Milestone A API is project-scoped; agent filter reserved for Milestone B.
        _ = agent_filter
    return {
        "project": project_id,
        "task_id": str(status.task_id),
        "state": str(status.state),
        "progress": f"{status.progress}%",
        "updated_at": status.updated_at.isoformat(),
    }


def status(
    project: str | None = typer.Option(
        None,
        "--project",
        "-p",
        help="Project id (defaults to all configured projects)",
    ),
    agent: str | None = typer.Option(
        None,
        "--agent",
        "-a",
        help="Filter by agent id (Milestone B)",
    ),
    watch: bool = typer.Option(False, "--watch", "-w", help="Poll status every 2 seconds"),
    interval: float = typer.Option(2.0, "--interval", help="Watch poll interval in seconds"),
) -> None:
    """Fetch GET /status/{project_id} and render a table."""
    try:
        project_ids = [project] if project else sorted(load_projects())
        if not project_ids:
            typer.echo("no projects configured", err=True)
            raise typer.Exit(code=1)
    except (FileNotFoundError, KeyError, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    def poll_once() -> list[dict[str, str]]:
        rows: list[dict[str, str]] = []
        for project_id in project_ids:
            try:
                rows.append(_fetch_status(project_id, agent))
            except RuntimeError as exc:
                typer.echo(f"{project_id}: {exc}", err=True)
        return rows

    if watch:
        try:
            while True:
                rows = poll_once()
                if rows:
                    _render_table(rows, clear=True)
                time.sleep(interval)
        except KeyboardInterrupt:
            raise typer.Exit(code=0) from None

    rows = poll_once()
    if not rows:
        raise typer.Exit(code=1)
    _render_table(rows)
