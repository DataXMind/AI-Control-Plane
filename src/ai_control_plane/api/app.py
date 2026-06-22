"""FastAPI application factory for the HTTP API bridge.

TypeScript PolicyClient calls this service for policy evaluation,
approval gates, and telemetry ingest. No business logic here — wiring only.
"""


def create_app():
    """Build and return the FastAPI application instance."""
