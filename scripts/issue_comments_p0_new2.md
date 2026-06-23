## P0-3 complete (Cursor)

- `ControlPlaneError` hierarchy in `core/exceptions.py`
- Removed duplicate API stubs: `api/app.py`, `api/deps.py`, `api/routes/*`
- `tests/test_exceptions.py` added

## P0-4 complete (Cursor)

- `build_agent_registry()`, `load_project_token_limits()` wired in `build_default_app_state()`
- `GET /health` extended with `HealthResponse` (config wire proof)
- `tests/test_api_server.py` covers health + quota

## NEW-2 complete (Cursor)

- `tests/fixtures/config/policies.yml` unified to production `rbac`/`abac`/`quotas` schema
- `test_policies.py` updated for canonical tool names + `Restrict-PII` policy id
- Loader: `derive_allowed_patterns()`, ABAC `k8s.apply` → `k8s_apply_*` action match
- Verify: `pytest tests/ -v` — 42 passed; `scripts/smoke_acp.sh` — SMK-01..05 passed

**Next:** Phase 2 tab 7 telemetry (#23) — awaiting Claude prompt.
