#!/usr/bin/env python3
"""Export OpenAPI 3 schema from FastAPI app (Public Beta PB-6)."""

from __future__ import annotations

import json
import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = REPO_ROOT / "docs" / "openapi"
OUT_FILE = OUT_DIR / "openapi.json"


def main() -> int:
    os.environ.setdefault("ACP_CONFIG_DIR", str(REPO_ROOT / "tests" / "fixtures" / "config"))
    sys.path.insert(0, str(REPO_ROOT / "src"))

    from ai_control_plane.api.server import create_app

    app = create_app()
    schema = app.openapi()
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    OUT_FILE.write_text(json.dumps(schema, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote {OUT_FILE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
