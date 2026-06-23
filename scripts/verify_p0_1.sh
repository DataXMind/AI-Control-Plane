#!/usr/bin/env bash
set -euo pipefail
cd /mnt/d/Projects/ai-control-plane
.venv/bin/python -c "
from ai_control_plane.core import registry, telemetry
from ai_control_plane.core.models import TelemetryEvent, TaskStatus
from ai_control_plane.core.telemetry import InMemoryTelemetryStore
s = InMemoryTelemetryStore()
e = s.append(TelemetryEvent(event_type='tool.call', agent_id='a', project_id='p', payload={}))
assert e.event_hash
assert TaskStatus.model_fields['progress'].default == 0
print('P0-1 OK')
"
.venv/bin/pytest tests/ -v --tb=short
