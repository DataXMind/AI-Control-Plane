"""agentctl gov — governance UX runtime (HTTP-only, Invariant #4)."""

from __future__ import annotations

import json

import typer

from ai_control_plane.cli._http import get_governance_status

gov_app = typer.Typer(help="Governance UX — 6-layer status and case studies")


@gov_app.command("status")
def status(*, json_output: bool = typer.Option(False, "--json", help="Emit raw JSON")) -> None:
    """Show 6-layer governance status from GET /governance/status."""
    payload = get_governance_status()
    if json_output:
        typer.echo(json.dumps(payload, indent=2))
        return

    typer.echo(f"Framework: {payload['framework']} (v{payload['governance_version']})")
    rules = payload["policy_rules_count"]
    typer.echo(f"Config loaded: {payload['config_loaded']} | Policy rules: {rules}")
    typer.echo("\nMilestones:")
    for key, value in payload["milestones"].items():
        typer.echo(f"  {key}: {value}")
    pb = payload["public_beta"]
    typer.echo(f"\nPublic Beta: {pb.get('phase')} ({pb.get('open_issues')})")
    typer.echo("\nCase studies (runtime checks):")
    for cs in payload["case_studies"]:
        typer.echo(f"  [{cs['id']}] {cs['title']} ({cs['layer']}) — {cs['runtime_check']}")
    typer.echo("\nDocs: docs/governance/GOVERNANCE_UX_RUNTIME.md")
