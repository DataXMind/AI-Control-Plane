# Dependency Security Audit — ACP 0.x

## CI Gate Status

pip-audit **NOT** automated in CI as of 0.x. Operator must run manually before each release. Planned: add pip-audit job to CI in v0.2.x.

Audit performed 2026-06-29: `grep -r 'pip.audit\|pip_audit' .github/workflows/` — **NOT FOUND** (no matching job in `ci.yml` or other workflow files).

## Suppression Policy

If a vulnerability has no available fix:

1. Add to `.pip-audit-suppression.json` with: CVE ID, reason, expiry date (max 90 days from discovery)
2. Create GitHub Issue tracking resolution
3. Update SECURITY.md §Known Issues

## Dependency Categories

| Category | Examples | Audit Priority |
|---|---|---|
| Runtime core | fastapi, redis, pydantic, uvicorn | CRITICAL — audit on every bump |
| Dev/test only | pytest, ruff, mypy | HIGH — audit weekly |
| Optional extras | opentelemetry-sdk | MEDIUM — audit on install |

## SBOM (Software Bill of Materials)

**0.x:** No formal SBOM published.

**Planned v0.2.x:** Generate SBOM via pip-licenses + cyclonedx on each release tag.

Enterprise users requiring SBOM before v0.2.x: contact maintainer@dataxmind.com.

## Local Verification Commands

```bash
pip install pip-audit
pip-audit
# or against requirements file:
pip-audit --requirement requirements.txt
```

## Supply Chain Note

ACP is a security enforcement control plane. A compromised ACP dependency could affect the entire governed agent fleet. pip-audit should be considered a CRITICAL gate, not optional. See THREAT_MODEL.md §T-2 (governance_catalog.py supply chain).
