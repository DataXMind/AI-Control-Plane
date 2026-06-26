# Local verify — MSI WSL + Docker minimal

**Run date:** 2026-06-26  
**Host:** dmin@MSI (WSL)  
**Repo:** `/mnt/d/Projects/ai-control-plane` @ `8b30ad4`  
**API:** `http://localhost:8000` → `minimal-acp-api-1`

---

## Commands

```bash
git pull origin master
docker compose -f examples/minimal/docker-compose.yml up -d --build
curl -sf http://localhost:8000/governance/status | python3 -c "
import sys,json; d=json.load(sys.stdin)
print(d['governance_version'], len(d['known_gaps']), d['practice_evidence']['overall_verdict'])
"
```

---

## Output

```text
1.2 7 PASS
```

---

## Docker build (excerpt)

```text
[5/7] COPY src ./src
[7/7] RUN pip install --no-cache-dir -e .
✔ Container minimal-acp-api-1 Started
```

---

## Prior failure (documented)

Before rebuild @ same host: `KeyError: 'known_gaps'` — container served pre-#99 image (`governance_version` 1.1).
