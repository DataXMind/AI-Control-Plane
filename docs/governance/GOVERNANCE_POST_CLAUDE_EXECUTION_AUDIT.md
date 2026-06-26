# Post-Claude review — Execution audit (Phương án A–F)

**Document ID:** ACP-GOV-POST-CLAUDE-AUDIT-001  
**Audit date:** 2026-06-26  
**Baseline:** `master` @ `dd16769` (PR #98–#100 merged)  
**Source:** Claude `practice_studies_architecture_review.html` + operator approve sequence §5

---

## 1. Executive matrix

| ID | Phương án | Scope | Status | PR / evidence |
|----|-----------|-------|--------|---------------|
| **NOW** | Merge PR #98 Gate B + PB9 + systemd | Docs + evidence | ✅ **DONE** | #98 → `6065e63` |
| **D** | PB-9 calendar soak (local SSOT) | Operator daily | 🔄 **IN PROGRESS** | `PB9_STAGING_SOAK_LOG.md` — tick 2026-06-26 |
| **B** | G-04 docs, profiles, WSL portproxy | Docs | ✅ **DONE** | #99 |
| **F** | Archive Claude HTML + banner | Docs | ✅ **DONE** | #99 |
| **A** | `known_gaps` + `practice_evidence` API v1.2 | Code + docs | ✅ **DONE** | #99 · verify [`governance-status-v12-verify/`](practice-evidence/governance-status-v12-verify/) |
| **—** | v1.2 dual-host verify evidence | Docs | ✅ **DONE** | #100 |
| **C1** | Study 05e-r (G-02 stale image) | Code bump + operator drill | 🔄 **THIS PR** | `study-05` artifact + catalog `1.2.1` |
| **C2** | Study 08 Profile B remote (G-06/G-07) | Operator on VPS | ⏸ **SCAFFOLD** | `study-08-shipped-remote/` — **needs Gate B approve + operator** |
| **C3** | Study 07b Mac witness (G2-3) | Optional operator | ⏸ **NOT STARTED** | Optional per audit |
| **E** | PB-11 legal completeness audit | Docs | 🔄 **THIS PR** | `PB11_LEGAL_AUDIT.md` |
| **G3/G4** | PB-7 verify, PB-8 rc, PB-12 flip | Human gates | ⏸ **BLOCKED** | PB-9 + PB-12 approve |

---

## 2. Gap registry sync

| Gap | Was (Claude HTML) | Now @ master |
|-----|-------------------|--------------|
| G-01 | SKIPPED | ✅ CLOSED G2-1 |
| G-02 | 5e partial | 🔄 05e-r in progress |
| G-03 | 7-0n soft | ✅ CLOSED G2-4 |
| G-04 | CS process-layer | ✅ CLOSED docs (#99 + UX runtime) |
| G-05 | PB-9 calendar | 🔄 OPEN (expected) |
| G-06 | Profile B remote | ⏸ Study 08 scaffold |
| G-07 | apex shipped remote | ⏸ Study 08 scaffold |

Runtime: `curl /governance/status` → `known_gaps[]` (catalog v1.2+).

---

## 3. Karpathy / PACE compliance

| Layer | This wave |
|-------|-----------|
| **L2** | LOW (docs + catalog patch version) |
| **L4** | SMK 8/8 + pytest after `governance_catalog` bump |
| **L5** | practice-evidence + LESSONS (G-02 stale image) |
| **Gate** | C2/C3 require **Gate B** operator approval before execution |

---

## 4. Blocked on human approve

| Item | Maintainer action |
|------|-------------------|
| **Study 08 execute** | Run `study-08-shipped-remote/RUNBOOK.md` on VPS (shipped `config/`) |
| **PB-9 daily tick** | *"đã tick ngày YYYY-MM-DD"* when soak log PASS |
| **PB-12 / public flip** | Gate **E** after PB-9 Day 14 (~2026-07-06) |
| **G2-3 Study 07b** | Optional Mac witness — approve if wanted |

---

**Last updated:** 2026-06-26
