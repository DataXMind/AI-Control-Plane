/**
 * ACP policy evaluate load smoke — P-15 skeleton (operator-run, not CI gate).
 *
 * Usage:
 *   export ACP_API_URL=http://127.0.0.1:8000
 *   k6 run benchmarks/k6/policy_evaluate.js
 *
 * Or: bash scripts/run_k6_policy_smoke.sh
 */
import http from "k6/http";
import { check, sleep } from "k6";

const BASE = __ENV.ACP_API_URL || "http://127.0.0.1:8000";
const VUS = Number(__ENV.K6_VUS || 10);
const DURATION = __ENV.K6_DURATION || "30s";

export const options = {
  scenarios: {
    policy_evaluate: {
      executor: "constant-vus",
      vus: VUS,
      duration: DURATION,
    },
  },
  thresholds: {
    http_req_failed: ["rate<0.01"],
    http_req_duration: ["p(99)<500"],
  },
};

const payload = JSON.stringify({
  agent_id: "agent2",
  project_id: "rust-gateway",
  tool_name: "git_read",
  role: "backend",
});

export default function () {
  const res = http.post(`${BASE}/policy/evaluate`, payload, {
    headers: { "Content-Type": "application/json" },
    tags: { name: "policy_evaluate" },
  });
  check(res, {
    "status is 200": (r) => r.status === 200,
    "allowed true": (r) => {
      try {
        return JSON.parse(r.body).allowed === true;
      } catch {
        return false;
      }
    },
  });
  sleep(0.1);
}
