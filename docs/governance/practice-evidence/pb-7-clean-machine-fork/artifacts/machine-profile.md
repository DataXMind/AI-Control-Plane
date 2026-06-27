# PB-7 machine profile — CLEAN run

| Field | Value |
|-------|-------|
| **Label** | **CLEAN** (Ubuntu OS user; no prior ACP on this user/path) |
| **Caveat** | Same physical host **MSI** — not a separate laptop; distinct from WARM `dmin@MSI` WSL dev path |
| **Host** | `ubuntu@MSI` |
| **Repo path** | `/mnt/d/DataXMind/Projects/AI-Control-Plane` |
| **OS** | Ubuntu (Linux on `/mnt/d` mount) |
| **Path** | **A — Docker Compose** (`examples/minimal/docker-compose.yml`) |
| **`master` SHA** | `082c5f9` (expected @ clone; verify with `git log -1`) |
| **Docker** | Compose v2, build `minimal-acp-api` |
| **Host `pip` / `agentctl`** | Not installed — CLI via `docker exec` only |

**WARM reference (does not count):** [`warm-fork-user-msi-2026-06-27.md`](warm-fork-user-msi-2026-06-27.md)
