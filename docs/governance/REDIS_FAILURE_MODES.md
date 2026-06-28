# Redis Failure Modes — ACP 0.x

## Behavior When Redis Unreachable

**ACP behavior:** FAIL-CLOSED — all policy evaluations return DENY with reason "redis_unavailable".
This is intentional (same as API-down behavior per SMK-04/CS-06).

**Operator action:** Restart Redis → ACP auto-reconnects. No ACP restart needed.
Check: `docker compose -f examples/minimal/docker-compose.yml ps`

## Redis Data Classification

| Key pattern | Content | Sensitivity | TTL |
|---|---|---|---|
| policy:cache:{hash} | Evaluated policy result | LOW (no PII) | Configurable |
| quota:{agent_id} | Request count | LOW | Rolling window |
| session:{token} | Agent session state | MEDIUM (identity) | Per-config |
| apex:proposals | SAPAL proposal queue | LOW (0.x stub) | N/A |

## Recommended Redis Configuration (Production)

```bash
# redis.conf minimum for ACP
requirepass <strong-password>
tls-port 6380
tls-cert-file /etc/ssl/redis/redis.crt
tls-key-file /etc/ssl/redis/redis.key
maxmemory-policy allkeys-lru   # prevent OOM; LRU eviction
maxmemory 512mb                 # tune per deployment
```

## Eviction Risk
If Redis evicts quota:{agent_id} keys under memory pressure, 
agents can bypass quota limits until key is re-populated.
Mitigation: Set maxmemory high enough; monitor Redis memory via /health endpoint.

## Single-Node Limitation (0.x)
examples/minimal uses single-node Redis. No HA in 0.x.
For production, use Redis Sentinel or Redis Cluster.
This is a known 0.x limitation — see PUBLIC_BETA_GO_NO_GO.md.

---

**Last updated:** 2026-06-28 · Catalog v1.3.3 · `master` @ `9bf5655`
