# Study 04 — Terminal 2 (client)

**Captured:** 2026-06-25  
**Source:** `TestCase/Study04/terminal2-cs04.md`

## 4a — port conflict + health

```bash
uvicorn ... --port 8000   # → ERROR: [Errno 98] Address already in use
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/health" | python3 -m json.tool
```

**Result:** `policy_rules_count: 8`, agents 1–3, `rust-gateway`.

## 4b — wrong URL (API down between drills) + correct :8002

**While nothing on :8000:**

```bash
export ACP_API_URL=http://localhost:8000
curl -s "$ACP_API_URL/health" | python3 -m json.tool
# → Expecting value: line 1 column 1 (char 0)

agentctl gov status
# → ConnectError → RuntimeError: governance status unavailable
```

**Correct endpoint:**

```bash
export ACP_API_URL=http://localhost:8002
curl -s "$ACP_API_URL/health" | python3 -m json.tool   # rules 8
agentctl gov status                                     # Policy rules: 8
```

## 4c — config without restart vs after restart

**Baseline (T1 fixture running):**

```bash
export ACP_API_URL=http://localhost:8000
curl ... # rules 8 agents 3
```

**Shell-only config change (T1 NOT restarted):**

```bash
unset ACP_CONFIG_DIR
curl ... # rules 8 agents 3  ← unchanged
agentctl gov status | head -5  # Policy rules: 8
```

**After T1 restart with shipped config:**

```bash
curl ... # rules 10 agents 4
```
