# OpenAPI specification

Generated from the FastAPI app (`create_app()`).

## Regenerate

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
python scripts/export_openapi.py
```

Output: [`openapi.json`](openapi.json)

## Interactive docs

When the API is running:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Public Beta (PB-12) publishes a static copy of this spec.

**Runtime verify:**

```bash
export ACP_API_URL=http://localhost:8000
bash scripts/verify_openapi_runtime.sh
```

## Pre-flip gate (PB-6)

| Step | Command | Owner |
|------|---------|-------|
| Regenerate | `ACP_CONFIG_DIR=tests/fixtures/config python scripts/export_openapi.py` | Cursor / maintainer |
| Contract parity | `pytest tests/test_api_contract_snapshot.py -v` | CI |
| Publish | Commit `openapi.json` + link from README on flip | Maintainer |

See [`docs/CONTRACT_TESTS.md`](../CONTRACT_TESTS.md) · [`PB11_LEGAL_AUDIT.md`](../governance/PB11_LEGAL_AUDIT.md).
