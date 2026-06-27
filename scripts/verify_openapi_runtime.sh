#!/usr/bin/env bash
# Runtime verify — GET /openapi.json (PB-6 runtime gate)
# Usage: ACP_API_URL=http://127.0.0.1:8000 bash scripts/verify_openapi_runtime.sh
set -euo pipefail
BASE="${ACP_API_URL:-http://127.0.0.1:8000}"
curl -sf "${BASE}/openapi.json" | python3 -c "
import sys, json
d = json.load(sys.stdin)
ver = d.get('openapi', '')
assert ver.startswith('3.'), ver
paths = d.get('paths', {})
assert len(paths) >= 10, len(paths)
for required in (
    '/health',
    '/governance/status',
    '/policy/evaluate',
    '/openapi.json',
):
    assert required in paths, required
print('OK: openapi runtime verify', ver, len(paths), 'paths')
"
