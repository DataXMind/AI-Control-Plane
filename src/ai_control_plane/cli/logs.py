"""agentctl logs — query audit telemetry via api/server.py (Milestone B)."""

from __future__ import annotations

import time

import typer

from ai_control_plane.cli._http import format_json, get_telemetry_events


def logs(
    project: str | None = typer.Option(None, "--project", "-p", help="Filter by project id"),
    follow: bool = typer.Option(False, "--follow", "-f", help="Poll telemetry every 2 seconds"),
    interval: float = typer.Option(2.0, "--interval", help="Follow poll interval in seconds"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON array"),
    limit: int = typer.Option(20, "--limit", "-n", help="Max events to show"),
) -> None:
    """Fetch GET /telemetry/events (optionally filtered by project)."""

    def fetch() -> list[dict[str, object]]:
        try:
            events = get_telemetry_events(project)
        except RuntimeError as exc:
            typer.echo(str(exc), err=True)
            raise typer.Exit(code=1) from exc
        sliced = events[-limit:] if limit > 0 else events
        return [
            {
                "event_id": event.event_id,
                "event_type": event.event_type,
                "agent_id": event.agent_id,
                "project_id": event.project_id,
                "timestamp": event.timestamp.isoformat(),
            }
            for event in sliced
        ]

    if follow:
        seen: set[str] = set()
        try:
            while True:
                rows = fetch()
                new_rows = [row for row in rows if row["event_id"] not in seen]
                for row in new_rows:
                    seen.add(str(row["event_id"]))
                    if json_output:
                        typer.echo(format_json(row))
                    else:
                        typer.echo(
                            f"{row['timestamp']} [{row['project_id']}] "
                            f"{row['event_type']} agent={row['agent_id']}",
                        )
                time.sleep(interval)
        except KeyboardInterrupt:
            raise typer.Exit(code=0) from None

    rows = fetch()
    if json_output:
        typer.echo(format_json({"events": rows}))
    elif not rows:
        typer.echo("no telemetry events")
    else:
        for row in rows:
            typer.echo(
                f"{row['timestamp']} [{row['project_id']}] "
                f"{row['event_type']} agent={row['agent_id']}",
            )
