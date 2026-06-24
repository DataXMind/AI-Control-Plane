# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- Public Beta prep: LICENSE, SECURITY, CONTRIBUTING, CODE_OF_CONDUCT
- `examples/minimal` Docker Compose quick start
- OpenAPI export (`scripts/export_openapi.py`, `docs/openapi/openapi.json`)
- PB-9 staging soak script (`scripts/soak_staging.sh`)

### Changed

- Governance docs synced post Milestone C+ (audit prompts 1–3 closed)

## [0.1.0-rc.1] — TBD (Public Beta flip PB-12)

Pre-GA public beta release. API may change until `1.0.0`.

### Includes

- Milestones A, B, C (boundary), C+ (ADR depth) — see `ARCHITECTURE.md` §Execution status
- 165 pytest, smoke 8/8, shipped config parity CI

[Unreleased]: https://github.com/DataXMind/AI-Control-Plane/compare/master...HEAD
[0.1.0-rc.1]: https://github.com/DataXMind/AI-Control-Plane/releases/tag/v0.1.0-rc.1
