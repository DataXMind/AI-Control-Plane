# Study 06 — Direction B — Mac server (native API)

**Captured:** 2026-06-25  
**Role:** API host (round 2)  
**Path:** `~/AI-Control-Plane`

## Setup

```bash
export ACP_CONFIG_DIR=tests/fixtures/config
uvicorn ai_control_plane.api.server:app --reload --host 0.0.0.0 --port 8000
```

- Reloader PID **56711**, worker **56713**
- Bind: `http://0.0.0.0:8000` (macOS native — **không** cần portproxy)

## Remote request (Laptop client)

| Time (local) | Remote IP | Method | Path | Status |
|--------------|-----------|--------|------|--------|
| 17:03:54 | **192.168.1.59:59566** | GET | /governance/status | 200 |

Latency 2.17 ms — IP Laptop hiện **trực tiếp** trên Mac (khác WSL round A).
