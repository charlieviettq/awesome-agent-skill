---
name: serverless-debugging
description: Debug serverless and edge functions—limited logs, cold starts, timeouts, env/config mismatches. Use for Lambda, Cloud Functions, Workers, Vercel/Netlify functions. Triggers: "serverless", "Lambda", "edge function", "cold start", "function timeout".
---

# Serverless Debugging

Systematic debugging when traditional server logs and SSH are unavailable. Complements `test-failure-triage` with environment-specific constraints.

## When to use

- Intermittent 5xx from functions
- Timeout or memory limit errors
- Works locally but fails when deployed

## When not to use

- Long-running container services with full shell access
- Client-only bugs (use browser DevTools skills)

## Workflow

1. **Reproduce** — identify trigger (HTTP event, queue, schedule)
2. **Logs** — cloud provider log group/stream; filter by request ID
3. **Config** — compare env vars/secrets: local vs deployed (names only, never log values)
4. **Limits** — timeout, memory, payload size, concurrency
5. **Cold start** — init duration, heavy imports, VPC ENI delay
6. **Dependencies** — outbound network, IAM permissions, region mismatch
7. **Minimal fix** — smallest change; redeploy; verify with structured log line

## Common failure modes

| Symptom | Likely cause |
|---------|----------------|
| Task timed out | Slow downstream, missing async, too much work in handler |
| Cannot find module | Bundle/packaging; wrong runtime |
| Access denied | IAM role, resource policy |
| Connection timeout | VPC/subnet/NAT; wrong security group |
| Works once then fails | State in `/tmp`; connection pool reuse |

## Practices

- Structured JSON logs with `requestId`, `stage`, `durationMs`
- Fail fast on missing required env with clear error message (no secret values)
- Use X-Ray or vendor tracing for cross-service calls
- Keep handlers thin; push heavy work to async queues when needed

## Related skills

- `dynamic-config-management` — env validation
- `observability-slo` — alerts and SLOs for functions
- `gstack/investigate` — general root-cause discipline

*Clean-room workflow for serverless environments.*
