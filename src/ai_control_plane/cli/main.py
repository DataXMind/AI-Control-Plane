"""Backward-compatible CLI entry re-export."""

from ai_control_plane.main import app

__all__ = ["app"]


def main() -> None:
    app()
