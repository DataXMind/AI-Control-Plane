#!/usr/bin/env bash
# MC-10 — OpenTelemetry collector launcher stub.
# Requires otelcol (https://opentelemetry.io/docs/collector/) on PATH.
set -euo pipefail

CONFIG="${ACP_OTEL_CONFIG:-config/otel-collector.yaml.example}"

if ! command -v otelcol >/dev/null 2>&1; then
  echo "otelcol not found on PATH. Install OpenTelemetry Collector or set ACP_OTEL_CONFIG." >&2
  echo "See: https://opentelemetry.io/docs/collector/installation/" >&2
  exit 1
fi

if [[ ! -f "$CONFIG" ]]; then
  echo "Collector config not found: $CONFIG" >&2
  echo "Copy config/otel-collector.yaml.example to config/otel-collector.yaml or set ACP_OTEL_CONFIG." >&2
  exit 1
fi

exec otelcol --config="$CONFIG"
