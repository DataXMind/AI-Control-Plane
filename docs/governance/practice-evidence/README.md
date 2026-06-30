# Practice evidence — Profile A/B/C hands-on runs

**Document ID:** ACP-GOV-PRACTICE-EVIDENCE-001  
**Purpose:** Bằng chứng thực hành local (operator-run), tách theo terminal, dùng cho audit Public Beta và onboarding sau PB-12.

**Không thay thế CI.** Smoke gate chính thức vẫn là `pytest tests/test_smoke.py -m smoke` trên GitHub Actions.

**Audit toàn chuỗi (Claude analyzer pack):** [`PRACTICE_STUDIES_AUDIT_01-07.md`](PRACTICE_STUDIES_AUDIT_01-07.md)

**Drift reconciliation (HTML artifacts ↔ master):** [`../GOVERNANCE_DRIFT_RECONCILIATION.md`](../GOVERNANCE_DRIFT_RECONCILIATION.md) · **Next tasks:** [`../GOVERNANCE_NEXT_PHASE_PLAN.md`](../GOVERNANCE_NEXT_PHASE_PLAN.md)

---

## Index

| Study | Profile | Verdict | Date | Evidence |
|-------|---------|---------|------|----------|
| Study 01 | A — fixture / CI | **PASS** | 2026-06-25 | [`study-01-profile-a/`](study-01-profile-a/) |
| Study 02 | B — shipped `config/` | **PASS** | 2026-06-25 | [`study-02-profile-b/`](study-02-profile-b/) |
| Study 03 | C — Docker / PB-9 soak | **PASS** | 2026-06-25 | [`study-03-profile-c/`](study-03-profile-c/) |
| Study 04 | Ops edge cases | **PASS** | 2026-06-25 | [`study-04-ops-edge/`](study-04-ops-edge/) |
| Study 05 | Advanced surprises | **PASS**† | 2026-06-25 | [`study-05-advanced-surprises/`](study-05-advanced-surprises/) |
| Study 06 | Multi-host (2+ machines) | **PASS** | 2026-06-25 | [`study-06-multi-host/`](study-06-multi-host/) |
| Study 07 | Cross-network (Tailscale) | **PASS** | 2026-06-25 | [`study-07-cross-network/`](study-07-cross-network/) |
| Study 08 | B — shipped remote VPS | **PASS** | 2026-06-26 | [`study-08-shipped-remote/`](study-08-shipped-remote/) |
| Gov status v1.2 | Docker dual-host (PR #99) | **PASS** | 2026-06-26 | [`governance-status-v12-verify/`](governance-status-v12-verify/) |
| Gov status v1.3 | Runtime `lessons_patterns` (PR #104) | **PASS** | 2026-06-26 | [`governance-status-v13-verify/`](governance-status-v13-verify/) — latest **v1.3.2** · 13 patterns @ `68ae48e` |
| ECC 48H post-verify | Deep audit v1.5.0 + integrate live | **PASS**‡ | 2026-06-30 | [`ecc-48h-post-verify/`](ecc-48h-post-verify/) — GHCR gap G-ECC-01 |
| k6 policy smoke | P-15 load smoke @ 10 VUs | **PASS** | 2026-06-30 | [`k6-policy-smoke/`](k6-policy-smoke/) |
| PB-7 | Clean-machine fork ≤15 min (G3-1) | **PAUSED** | — | Operator: other laptop — [`pb-7-clean-machine-fork/`](pb-7-clean-machine-fork/) |

‡ ECC post-verify: compose local **1.5.0** PASS; GHCR republish coupled to catalog push (G-ECC-01 closed @ PR #157).

† Study 05: 5g G2-1 + 5e G2-2 closed @ 2026-06-26.

---

## Lộ trình đề xuất

| Bước | Study | Máy |
|------|-------|-----|
| 1 | 01 Profile A (fixture) | 1 |
| 2 | 02 Profile B (shipped) | 1 |
| 3 | 03 Profile C (Docker soak) | 1 |
| 4 | 04 Ops edge (4a–4c) | 1 |
| 5 | 05 Advanced (5a–5g) | 1 |
| 6 | 06 Multi-host | **2+** (cùng LAN) |
| 7 | 07 Cross-network | **2+** (khác LAN, Tailscale) |

---

## Cấu trúc mỗi study

```text
study-NN-profile-x/
  RESULTS.md          # Ma trận PASS/FAIL + giá trị kỳ vọng
  terminal-1-server.md   # API / uvicorn / docker
  terminal-2-client.md   # curl / agentctl / pytest
  artifacts/          # JSON trích xuất (machine-readable)
```

**Ghi chú:** Log gốc operator có thể lưu ngoài repo; bản trong repo là bản đã sanitize (không secret).
