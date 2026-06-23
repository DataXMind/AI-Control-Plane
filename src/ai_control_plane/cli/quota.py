"""agentctl quota — inspect project quotas."""

from __future__ import annotations

import typer

from ai_control_plane.cli._http import format_json, get_project_quota


def quota(
    project: str = typer.Argument(..., help="Project id"),
    json_output: bool = typer.Option(False, "--json", help="Emit JSON output"),
) -> None:
    """Fetch GET /quota/{project_id}."""
    try:
        status = get_project_quota(project)
    except RuntimeError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1) from exc

    output = {
        "project_id": status.project_id,
        "tokens_used": status.tokens_used,
        "tokens_remaining": status.tokens_remaining,
        "requests_today": status.requests_today,
    }
    if json_output:
        typer.echo(format_json(output))
    else:
        typer.echo(
            f"{status.project_id}: "
            f"{status.tokens_remaining:.0f} tokens remaining "
            f"({status.tokens_used:.0f} used, {status.requests_today} requests today)",
        )
