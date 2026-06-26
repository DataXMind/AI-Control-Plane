# Practice Studies 01–07 — Audit & progression (Claude analyzer pack)

**Document ID:** ACP-GOV-PRACTICE-AUDIT-01-07  
**Version:** 1.0  
**Audit date:** 2026-06-25  
**Operator:** dmin@MSI (WSL) + dataxmind@DataXMinds-Mac-mini + `ubuntu-vps`  
**Repo baseline:** `master` post PR #86 (governance UX) · evidence PR #87–#88  
**SSOT index:** [`README.md`](README.md)

---

## 1. Mục đích tài liệu

Tài liệu này **không thay thế** từng `RESULTS.md` per study. Nó cung cấp:

1. **Tiến trình có thứ tự** — vì sao Study N phụ thuộc N−1.  
2. **Ma trận coverage** — CS-01..06, invariants, layers, endpoints.  
3. **Gap & partial** — mọi chỗ chưa chặt (để Claude không over-claim).  
4. **Chỉ dẫn phân tích** — cách đọc evidence khi audit Public Beta / onboarding.

**Phạm vi:** Operator-run practice evidence trong `docs/governance/practice-evidence/`.  
**Ngoài phạm vi:** GitHub Actions CI (`pytest -m smoke`), PB-9 calendar soak 14 ngày (đến ~2026-07-06).

---

## 2. Executive summary

| Metric | Value |
|--------|-------|
| Studies executed | **8 / 8** (01–07 audit pack + Study 08) |
| Overall verdict | **PASS** với 3 gap có document |
| Hosts used | MSI WSL · Mac Mini M2 · `ubuntu-vps` (Tailscale tailnet) |
| Config profiles | A (fixture) · B (shipped) · C (Docker fixture) |
| Network paths | localhost → LAN `192.168.1.0/24` → Tailscale `100.x` only |
| CI substitute? | **No** — practice bổ sung, không thay smoke gate |

### Gap registry (không fail tổng thể)

| ID | Study | Gap | Severity | Remediation |
|----|-------|-----|----------|-------------|
| G-01 | 05 | ~~**5g** kill switch SKIPPED~~ **CLOSED G2-1** @ 2026-06-26 | — | `study-05/artifacts/terminal-5g-g2-killswitch.md` |
| G-02 | 05 | ~~**5e** stale image~~ **CLOSED G2-2** @ 2026-06-26 | — | `study-05/artifacts/terminal-5e-r-g2-docker.md` |
| G-03 | 07 | ~~**7-0n** negative LAN ping không paste~~ **CLOSED G2-4** @ 2026-06-26 | — | `study-07/artifacts/terminal-7-0n-negative-lan.md` |
| G-04 | 01–07 | ~~CS-01/03/04 process-layer~~ **CLOSED** @ 2026-06-26 | — | `GOVERNANCE_UX_RUNTIME.md` § process-layer |
| G-05 | PB-9 | Calendar soak 14d ≠ practice one-shot | Info | `PB9_STAGING_SOAK_LOG.md` |
| G-06 | 08 | ~~**Profile B remote**~~ **CLOSED G2-5** @ 2026-06-26 | — | `study-08/artifacts/remote-profile-b-health.json` |
| G-07 | 08 | ~~**apex/trigger** shipped remote~~ **CLOSED G2-5** @ 2026-06-26 | — | `study-08/artifacts/remote-profile-b-soak.md` |

---

## 3. Tiến trình (progression ladder)

```text
┌─────────────────────────────────────────────────────────────────────────────┐
│  PHASE A — Single host (MSI WSL)                                            │
├─────────────────────────────────────────────────────────────────────────────┤
│  Study 01  Profile A (fixture)     health · gov · policy · deny · smoke     │
│     ↓                                                                       │
│  Study 02  Profile B (shipped)     rules 8→10 · assign · CLI→HTTP trace   │
│     ↓                                                                       │
│  Study 03  Profile C (Docker)      container · soak local · healthcheck     │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE B — Ops & failure modes (still 1 host)                               │
├─────────────────────────────────────────────────────────────────────────────┤
│  Study 04  Ops edge                port conflict · URL mismatch · config@boot│
│     ↓                                                                       │
│  Study 05  Advanced surprises      fail-closed · RBAC deny · Docker conflict │
├─────────────────────────────────────────────────────────────────────────────┤
│  PHASE C — Multi endpoint                                                   │
├─────────────────────────────────────────────────────────────────────────────┤
│  Study 06  Multi-host LAN        Laptop↔Mac bidirectional · portproxy WSL   │
│     ↓                                                                       │
│  Study 07  Cross-network TS      ubuntu-vps API · Laptop client · remote soak│
└─────────────────────────────────────────────────────────────────────────────┘
```

### Dependency graph

| Study | Requires | Unlocks |
|-------|----------|---------|
| 01 | PR #86 merged, `.venv`, uvicorn | 02, 04, 05 |
| 02 | 01 PASS, `unset ACP_CONFIG_DIR` | 03 (delta awareness) |
| 03 | 02 PASS, Docker | PB-9 soak script familiarity |
| 04 | 01–03 | 05 |
| 05 | 04 | 06 (fail-closed confidence) |
| 06 | 05, 2nd physical host | 07 |
| 07 | 06, Tailscale tailnet, VPS | PB-9 remote operator narrative |

---

## 4. Configuration profiles (cross-study)

| Profile | `ACP_CONFIG_DIR` | Runtime | `policy_rules_count` | `agents` | Studies |
|---------|------------------|---------|----------------------|----------|---------|
| **A** | `tests/fixtures/config` | uvicorn local | **8** | 3 | 01, 04, 05, 06, 07 |
| **B** | unset → `config/` | uvicorn local | **10** | 4 | 02, 04c |
| **C** | fixture in compose | Docker `minimal-acp-api` | **8** | 3 | 03, 05d–5e |

**Invariant học được:** `ACP_CONFIG_DIR` trên **client shell không đổi** server đang chạy (Study 04c). Chỉ **restart API** với env mới mới đổi rules (8→10).

---

## 5. Network topology evolution

| Stage | Study | API bind | Client `ACP_API_URL` | Server sees client as |
|-------|-------|----------|----------------------|------------------------|
| Loopback | 01–05 | `127.0.0.1:8000` | `http://localhost:8000` | `127.0.0.1` |
| Docker publish | 03 | `0.0.0.0:8000` (container) | `http://localhost:8000` | `172.27.0.1` (host bridge) |
| LAN remote | 06A | WSL `0.0.0.0` + **portproxy** | `http://192.168.1.59:8000` | `192.168.16.1` (WSL NAT) |
| LAN native API | 06B | Mac `0.0.0.0:8000` | `http://192.168.1.99:8000` | `192.168.1.59` (direct) |
| Tailscale overlay | 07 | VPS `0.0.0.0:8000` | `http://100.94.21.33:8000` | `100.102.105.47` (msi TS) |

**Claude check:** Study 06 chứng minh **cùng subnet**; Study 07 chứng minh **overlay-only** (log VPS không có LAN client IP).

---

## 6. Per-study audit

### Study 01 — Profile A (fixture / CI parity)

| Field | Value |
|-------|--------|
| **Doc ID** | ACP-GOV-PRACTICE-STUDY-01 |
| **Verdict** | **PASS** |
| **Hosts** | 1 (MSI WSL, T1 server + T2 client) |
| **Hypothesis** | Fixture config wires correctly; smoke gate reproducible locally |
| **Evidence path** | [`study-01-profile-a/`](study-01-profile-a/) |

| Test ID | What | Pass criterion | Actual |
|---------|------|----------------|--------|
| A1 | `GET /health` | rules=8, 3 agents | ✅ |
| A2 | `gov status` / `governance/status` | 6-layer, CS-01..06 listed | ✅ |
| A3 | policy allow | `allowed: true` | ✅ |
| A4 | policy deny unknown (CS-06) | `allowed: false` + reason | ✅ |
| A5 | `pytest -m smoke` | 8/8 | ✅ |

**Artifacts:** `health.json`, `policy-allow.json`, `policy-deny-unknown-agent.json`, `smoke-summary.json`  
**Ops note:** Port conflict lần 1 (A0b) — retry OK; không fail study.

---

### Study 02 — Profile B (shipped config)

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** |
| **Hypothesis** | Shipped `config/` ≠ fixture; assign path works |
| **Evidence path** | [`study-02-profile-b/`](study-02-profile-b/) |

| Test ID | What | Pass criterion | Actual |
|---------|------|----------------|--------|
| B1 | health | rules=**10**, 4 agents, 2 projects | ✅ |
| B2 | gov status | rules 10 | ✅ |
| B3 | `agentctl assign` | task_id, PENDING; T1 logs POST /tasks | ✅ |

**Delta vs 01:** rules 8→10, +agent4, +datax-analytics — **critical for PB-10 production config narrative**.

---

### Study 03 — Profile C (Docker / PB-9)

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** |
| **Hypothesis** | Minimal compose stack + soak script = PB-9 operator slice |
| **Evidence path** | [`study-03-profile-c/`](study-03-profile-c/) |

| Test ID | What | Pass criterion | Actual |
|---------|------|----------------|--------|
| C1 | health via Docker | rules=8 (fixture in compose) | ✅ |
| C2–C4 | `soak_staging.sh` | health=ok, policy=True, apex=ok | ✅ ×2 + log file |
| C5 | container healthcheck | periodic /health 200 | ✅ |
| C6 | teardown | `docker compose down` clean | ✅ |

**CS-05:** Local soak PASS (partial vs 14-day calendar).

---

### Study 04 — Ops edge cases

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** |
| **Hypothesis** | Operator mistakes (port, URL, config) are detectable |
| **Evidence path** | [`study-04-ops-edge/`](study-04-ops-edge/) |

| Drill | Lesson | Evidence |
|-------|--------|----------|
| 4a | Port conflict errno 98 | ✅ |
| 4b | Wrong URL / API down → CLI fail-closed | ✅ Invariant #4 (CLI HTTP-only) |
| 4c | Config only at startup | ✅ 8→8→10 after T1 restart |

**Optional not run:** curl `:8000` while server on `:8002` (stale port) — deferred to 05a overlap.

---

### Study 05 — Advanced surprises

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** (7/7 drills; 5g G2-1) |
| **Hypothesis** | Fail-closed under stress; RBAC deny; Docker vs uvicorn |
| **Evidence path** | [`study-05-advanced-surprises/`](study-05-advanced-surprises/) |

| Drill | Result | Notes |
|-------|--------|-------|
| 5a API down | ✅ | gov + assign unavailable |
| 5b allow/deny | ✅ | reviewer `git_push` denied |
| 5c invalid body | ✅ | **503** not 422 — document drift fixed in notes |
| 5d Docker :8000 | ✅ | rules stable ×3 |
| 5e rebuild version | ✅ G2-2 | `terminal-5e-r-g2-docker.md` |
| 5f bad JWT | ✅ | 503 + `allowed: false` |
| 5g kill switch | ✅ G2-1 | `terminal-5g-g2-killswitch.md` |

**CS-06:** Extended via 5a, 5c, 5f (fail-closed paths).

---

### Study 06 — Multi-host (LAN)

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** (bidirectional, full 6-1..6-4 both rounds) |
| **Hosts** | MSI Laptop (WSL) + Mac Mini M2 |
| **Hypothesis** | Invariant #4 holds across physical hosts on LAN |
| **Evidence path** | [`study-06-multi-host/`](study-06-multi-host/) |
| **Topology** | [`TOPOLOGY_WINDOWS_MAC.md`](study-06-multi-host/TOPOLOGY_WINDOWS_MAC.md) |

| Round | API | Client | Key task_ids | Server client IP in log |
|-------|-----|--------|--------------|-------------------------|
| A | Laptop `192.168.1.59` + portproxy | Mac | `03c332db-...` | `192.168.16.1` (WSL NAT) |
| B | Mac `192.168.1.99` | Laptop | `ae6c13a4-...` | `192.168.1.59` (direct) |

| Test | Round A | Round B |
|------|---------|---------|
| 6-1 health | ✅ | ✅ (via gov/policy) |
| 6-2 gov | ✅ | ✅ |
| 6-3 policy | ✅ | ✅ @ 17:34 |
| 6-4 assign | ✅ | ✅ @ 17:34 |
| 6-5 soak remote LAN | ⏭️ | → Study 07 |

**Infra lesson:** WSL2 API requires **Admin portproxy** + firewall for LAN ingress.

---

### Study 07 — Cross-network (Tailscale)

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** |
| **Hosts** | `ubuntu-vps` (API) + MSI Laptop (client) |
| **Mac Mini** | **Not used** — see §8 |
| **Hypothesis** | Remote operator reaches staging-like API via overlay only |
| **Evidence path** | [`study-07-cross-network/`](study-07-cross-network/) |

| Test ID | Result | Key value |
|---------|--------|-----------|
| 7-0 tailnet | ✅ | Client TS `100.102.105.47` only in VPS logs |
| 7-1 health | ✅ | rules 8 |
| 7-2 gov | ✅ | rules 8 |
| 7-3 policy | ✅ | allow in assign + soak |
| 7-4 assign | ✅ | `6206697f-eab5-49c8-83e0-0dcf887d4999` |
| 7-5 soak remote | ✅ | CS-05 one iteration |

**API host:** Cloud VPS (runbook option B) — valid; inherently off-home-LAN.

---

## 7. Case study coverage matrix (CS-01..06)

Catalog SSOT: `src/ai_control_plane/core/governance_catalog.py` · narrative: [`GOVERNANCE_UX_RUNTIME.md`](../GOVERNANCE_UX_RUNTIME.md)

| CS | Layer | Runtime check (catalog) | Hands-on evidence | Studies | Strength |
|----|-------|-------------------------|-------------------|---------|----------|
| **CS-01** | L3 | PR LOC + risk before merge | Listed in `gov status` only | 01–07 (A2/B2/…) | **Weak** — process, not drilled |
| **CS-02** | L3 | Doc-only PR allowlist | `doc_links` in gov response | 01 A2 | **Weak** — path listed |
| **CS-03** | L5 | Individual `Closes #N` | Listed in `gov status` only | 01–07 | **Weak** — process |
| **CS-04** | L0 | ABAC key pre-flight | Listed in `gov status` only | 01–07 | **Weak** — process |
| **CS-05** | L4 | `/health` + `soak_staging.sh` | Local soak ×2; **remote soak ×1** | 03, **07** | **Strong** (slice; not 14d) |
| **CS-06** | L4 | `POST /policy/evaluate` fail-closed | deny unknown; 503 paths; allow remote | 01, 05, 06, 07 | **Strong** |

**Claude rule:** Do **not** claim CS-01/03/04 are operator-validated beyond catalog visibility. Claim CS-05/06 with study citations.

---

## 8. Invariants & architecture checks

| Invariant / rule | Source | Validated by |
|------------------|--------|--------------|
| CLI → HTTP only (no direct `core/policies` in CLI) | `.cursorrules` L0 #4 | 02 B3b logs, 04 4b, 06–07 remote assign |
| Fail-closed policy (no default-allow on error) | `.cursorrules` NEVER | 01 A4, 05 5a/5c/5f, 04 4b |
| `ACP_CONFIG_DIR` at startup | config invariant #8 | 04 4c |
| `ACP_API_URL` must match live API | practice invariant #4 | 04 4b, 06, 07 |
| core/policies: no OSS engine imports | `.cursorrules` #1 | CI / code review (not practice drill) |
| Smoke SMK-01..06c | CI + Study 01 A5 | 01 only (pytest) |

---

## 9. Endpoint & tool coverage

| Endpoint / tool | 01 | 02 | 03 | 04 | 05 | 06 | 07 |
|-----------------|:--:|:--:|:--:|:--:|:--:|:--:|:--:|
| `GET /health` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ remote | ✅ remote TS |
| `GET /governance/status` | ✅ | ✅ | ✅ | ✅ | — | ✅ remote | ✅ remote |
| `POST /policy/evaluate` allow | ✅ | — | ✅ soak | ✅ | ✅ | ✅ both dirs | ✅ |
| `POST /policy/evaluate` deny | ✅ | — | — | — | ✅ | — | — |
| `POST /policy/evaluate` invalid | — | — | — | — | ✅ 503 | — | — |
| `POST /identity/verify` bad JWT | — | — | — | — | ✅ | — | — |
| `POST /tasks` (assign) | — | ✅ | — | — | — | ✅ both dirs | ✅ |
| `GET /quota/{project}` | — | — | ✅ soak | — | — | — | ✅ soak |
| `POST /apex/trigger` | — | — | ✅ soak | — | — | — | ✅ soak |
| `agentctl gov status` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `agentctl assign` | — | ✅ | — | — | ✅ down | ✅ | ✅ |
| `pytest -m smoke` | ✅ | — | — | — | — | — | — |
| `soak_staging.sh` | — | — | ✅ local | — | — | ⏭️ | ✅ remote |
| Docker compose | — | — | ✅ | — | ✅ | — | — |

---

## 10. Host & operator inventory

| Host | OS | Tailscale | Roles in studies | LAN IP (when relevant) |
|------|-----|-----------|------------------|------------------------|
| MSI Laptop | Windows + WSL Ubuntu | `100.102.105.47` | 01–05 client/server; 06 API+client; 07 client | `192.168.1.59` |
| Mac Mini M2 | macOS | `100.72.15.27` | **06 only** (LAN peer) | `192.168.1.99` |
| ubuntu-vps | Linux (cloud) | `100.94.21.33` | **07 API** | N/A (not home LAN) |

### Vì sao Mac Mini không trong Study 07?

| Reason | Detail |
|--------|--------|
| Role saturation | Study 06 already used Mac as LAN client **and** API |
| Client persona | Study 07 = **mobile laptop** as remote operator |
| API stability | VPS always-on vs Mac sleep |
| Witness optional | Mac could join Study 07b (LAN vs TS compare) — not required for PASS |

---

## 11. Evidence artifact index (machine-readable)

```text
study-01-profile-a/artifacts/     health, policy-allow, policy-deny-unknown-agent, smoke-summary
study-02-profile-b/artifacts/     health, gov-status-summary, cli-assign
study-03-profile-c/artifacts/     health, gov-status-summary, soak-log-excerpt
study-04-ops-edge/artifacts/      drill-4a, 4b, 4c
study-05-advanced-surprises/      drill-5a..5f (no 5g)
study-06-multi-host/artifacts/    topology-lan, direction-a-*, direction-b-*
study-07-cross-network/artifacts/ topology-tailscale, remote-health, remote-policy-assign, remote-soak
```

**Operator raw logs (ngoài repo):** `TestCase/Study01` … `Study05` (Windows path operator).

---

## 12. PB-9 Public Beta relationship

| Gate | Practice evidence | Calendar / CI |
|------|-------------------|---------------|
| Smoke pytest | Study 01 A5 | GitHub Actions every PR |
| Docker minimal stack | Study 03 | — |
| `soak_staging.sh` local | Study 03 C2–C4 | — |
| `soak_staging.sh` remote | Study 07 7-5 | — |
| 14-day soak log | **Not closed** by studies | `PB9_STAGING_SOAK_LOG.md` ~2026-07-06 |
| Multi-host staging | Studies 06–07 | — |

**Claude rule:** Studies 01–07 **do not** close PB-9. They provide **operator confidence** and **audit trail**.

---

## 13. Chronology (2026-06-25)

| Time (local approx) | Event |
|---------------------|-------|
| AM | Studies 01–03 Profile A/B/C |
| 14:00–14:32 | Studies 04–05 continuous |
| 15:14–16:59 | Study 06 round A (portproxy + Mac client) |
| 17:03–17:34 | Study 06 round B (Mac API + Laptop full suite) |
| 11:09–11:18 UTC | Study 07 ubuntu-vps + Laptop Tailscale |

---

## 14. Hướng dẫn cho Claude khi phân tích

### 14.1 Câu hỏi thường gặp

| Question | Answer source |
|----------|---------------|
| Fixture vs shipped rules count? | §4 — 8 vs 10; Docker back to 8 |
| Remote CLI proven? | Study 06–07 + 02 B3b server logs |
| Fail-closed proven? | Study 01 A4, 04 4b, 05 5a/5c/5f |
| Tailscale vs LAN? | Study 06 = LAN; Study 07 = TS only in VPS logs |
| Mac role? | Study 06 only; §10 |
| What's still open? | §2 Gap registry G-05, G-06, G-07 |

### 14.2 Không được suy diễn

- CS-01, CS-02, CS-03, CS-04 **hands-on PASS** — chỉ **catalog visibility**.  
- PB-9 **closed** — chỉ slice soak PASS.  
- Study 07 **overlay-only path** — G2-4 closed via `terminal-7-0n-negative-lan.md` (VPS B). Hotspot strict paste optional for on-prem API.  
- Kill switch active — **5g PASS** (G2-1 @ 2026-06-26).

### 14.3 Citation format

Khi trích dẫn evidence trong PR/issue:

```text
Practice evidence Study NN — docs/governance/practice-evidence/study-NN-*/RESULTS.md
Artifact: study-NN-*/artifacts/<file>.json
Governance UX v1.2 verify — practice-evidence/governance-status-v12-verify/RESULTS.md
```

### 14.3b Supplemental — governance status v1.2 (PR #99)

| Field | Value |
|-------|--------|
| **Verdict** | **PASS** dual-host |
| **Date** | 2026-06-26 |
| **Path** | [`governance-status-v12-verify/`](governance-status-v12-verify/) |
| **Assert** | `governance_version` 1.2 · 7 `known_gaps` · `practice_evidence` PASS |
| **Hosts** | MSI Docker + `ubuntu-vps` systemd/Docker |

Documents stale-image lesson (rebuild required after `src/` merge).

### 14.4 Đề xuất follow-up studies (optional)

| ID | Name | Purpose |
|----|------|---------|
| 07b | Mac witness | LAN fail vs TS ok side-by-side (optional) |
| ~~05g-r~~ | ~~Kill switch~~ | **Done** — G2-1 |
| ~~05e-r~~ | ~~Stale image~~ | **Done** — G2-2 @ 2026-06-26 |
| 08 | Shipped config remote | **Scaffold** — [`study-08-shipped-remote/`](study-08-shipped-remote/) — operator Gate B |

---

## 15. Sign-off matrix

| Study | Verdict | Blocker for next | Evidence complete |
|-------|---------|------------------|-------------------|
| 01 | PASS | No | Yes |
| 02 | PASS | No | Yes |
| 03 | PASS | No | Yes |
| 04 | PASS | No | Yes |
| 05 | PASS | No | Yes (5g G2-1) |
| 06 | PASS | No | Yes |
| 07 | PASS | No | Yes (7-0n G2-4) |

**Series verdict:** **PASS** — sufficient for Public Beta operator onboarding narrative and Claude governance analysis, with documented gaps in §2.

---

## 16. Related documents

| Document | Role |
|----------|------|
| [`practice-evidence/README.md`](README.md) | Index Studies 01–07 |
| [`GOVERNANCE_UX_RUNTIME.md`](../GOVERNANCE_UX_RUNTIME.md) | CS-01..06 catalog |
| [`ACP_ARTIFACT_PUZZLE_MAP.md`](../ACP_ARTIFACT_PUZZLE_MAP.md) | Doc map |
| [`GOVERNANCE_DRIFT_RECONCILIATION.md`](../GOVERNANCE_DRIFT_RECONCILIATION.md) | HTML artifacts ↔ master |
| [`GOVERNANCE_NEXT_PHASE_PLAN.md`](../GOVERNANCE_NEXT_PHASE_PLAN.md) | G0–G4 tasks |
| [`CLAUDE.md`](../../../CLAUDE.md) | L0 behavioral SSOT |
| `.cursorrules` L0–L5 | Invariants & verify gate |
| `scripts/soak_staging.sh` | PB-9 soak script |

**Drift:** HTML `karpathy_acp_artifacts_fixed.html` deploy packet (pytest 156) is stale — use this audit + reconciliation doc.

**Last updated:** 2026-06-25
