# Contributing to AI Control Plane

Thank you for contributing. This project is a **governance control plane** — changes that weaken fail-closed behavior or bypass invariants will be rejected.

## Before you start

1. Read [ARCHITECTURE.md](ARCHITECTURE.md) — **8 hard invariants** are non-negotiable.
2. Read [docs/DEVELOPMENT_PROTOCOL.md](docs/DEVELOPMENT_PROTOCOL.md) — PACE workflow, 9-step executor path, smoke gate.
3. Open or link a GitHub issue (`bug`, `spec-gap`, `debt`, `quality`).

## Development setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
export ACP_CONFIG_DIR=tests/fixtures/config
```

## Required gates (every PR)

```bash
ruff check src/ tests/
mypy src/ai_control_plane/ --strict
pytest tests/ -q
pytest -m smoke -q
```

CI must pass **Smoke gate** and **Full suite**.

## Invariants (summary)

1. Custom `PolicyEngine` in `core/policies.py` — no OSS replacement.
2. `core/models.py` owns all data contracts.
3. `mcp/git_server.py` is the only Git facade — no Git logic in Python.
4. `cli/` calls HTTP/API only — no direct policy imports.
5. `apex/` owns the SAPAL loop.
6. `api/` is the TypeScript bridge.
7. `QuotaStore` is swappable via ABC.
8. Shipped `config/` + runtime `ACP_CONFIG_DIR`.

## PR rules

- Target `master` via pull request only (no direct pushes).
- Conventional Commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`.
- Link the issue in the PR description.
- Update `ARCHITECTURE.md` when HTTP contracts or config loading change.

## Code of conduct

See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
