"""CLI main entry re-export (coverage Tier 2)."""

from __future__ import annotations

from unittest.mock import patch

from ai_control_plane.cli import main as cli_main


def test_cli_main_invokes_app() -> None:
    with patch("ai_control_plane.cli.main.app") as mock_app:
        cli_main.main()
        mock_app.assert_called_once()
