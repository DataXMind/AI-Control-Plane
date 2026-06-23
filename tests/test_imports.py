"""Smoke test — package and subpackages are importable."""


def test_import_ai_control_plane():
    import ai_control_plane  # noqa: F401


def test_import_subpackages():
    import ai_control_plane.apex  # noqa: F401
    import ai_control_plane.api  # noqa: F401
    import ai_control_plane.cli  # noqa: F401
    import ai_control_plane.config  # noqa: F401
    import ai_control_plane.core  # noqa: F401
    import ai_control_plane.mcp  # noqa: F401
