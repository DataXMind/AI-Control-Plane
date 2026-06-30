#!/usr/bin/env bash
# Runtime verify — GET /governance/status (catalog v1.3.0+)
# Usage: ACP_API_URL=http://127.0.0.1:8000 bash scripts/verify_governance_status_runtime.sh
set -euo pipefail
BASE="${ACP_API_URL:-http://127.0.0.1:8000}"
curl -sf "${BASE}/governance/status" | python3 -c "
import sys, json
d = json.load(sys.stdin)
assert d['governance_version'] == '1.5.0', d.get('governance_version')
assert len(d['known_gaps']) == 7
assert sum(1 for g in d['known_gaps'] if g['status'] == 'OPEN') == 1
assert len(d['lessons_patterns']) >= 17
assert len(d['public_beta']['gates_remaining']) >= 5
assert d['public_beta']['gates_blocking_pb12'] == ['PB-9', 'PB-12']
assert len(d['public_beta']['gate_details']) == 7
assert len(d['public_beta']['gates_closed']) >= 3
assert d['doc_links']['risk_policy'].endswith('CURSOR_RISK_POLICY.md')
assert d['practice_evidence']['studies_completed'] == 8
print('OK: governance/status runtime verify', d['governance_version'], len(d['lessons_patterns']), 'patterns')
"
