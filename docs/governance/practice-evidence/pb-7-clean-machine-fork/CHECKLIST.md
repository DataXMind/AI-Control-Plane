# PB-7 — Checklist

- [ ] Machine profile recorded (CLEAN or WARM)
- [ ] `git clone` + SHA noted
- [ ] Path A or B selected
- [ ] Timer started at T0 (clone)
- [ ] `GET /health` → `status: ok`, `config_loaded: true`
- [ ] `POST /policy/evaluate` allow → `allowed: true`
- [ ] (Recommended) deny unknown agent → `allowed: false`
- [ ] Total elapsed ≤ 15 minutes
- [ ] Artifacts saved under `artifacts/`
- [ ] `RESULTS.md` updated PASS/FAIL
