---
name: cross-platform-error-handling
description: Design consistent error handling across web, mobile, and React Native—central handlers, user-facing copy, retry, and logging. Triggers: "error handling", "error boundary", "toast", "React Native errors", "global handler".
---

# Cross-Platform Error Handling

Patterns for centralized error capture, user-appropriate messaging, and observability across web and mobile clients.

## When to use

- Inconsistent error UX across platforms
- Unhandled promise rejections or crash reports
- Adding global error boundary/handler

## When not to use

- Server-side API error design (use `api-and-interface-design`)
- Single-platform app with existing mature pattern (extend, don't rewrite)

## Architecture

```
Error occurs → classify (network/auth/validation/unknown)
            → log (structured, no PII)
            → user message (actionable, localized)
            → optional retry/report
```

## Platform patterns

| Platform | Mechanism |
|----------|-----------|
| React web | Error boundary + window `unhandledrejection` |
| React Native | Global handler + native crash reporting SDK |
| Next.js | `error.tsx` boundaries + server action error mapping |

## User messaging rules

- **Network** — "Check connection" + retry
- **Auth** — redirect to login; no token details
- **Validation** — field-level hints
- **Unknown** — generic message + support/ref ID; log details server-side

## Checklist

- [ ] Central error type taxonomy (shared package if monorepo)
- [ ] No stack traces shown to end users
- [ ] Correlation ID in user-facing error when support needed
- [ ] Regression test for at least one error path per platform
- [ ] Offline mode handled where applicable

## Related skills

- `api-and-interface-design` — API error shapes
- `frontend-ui-engineering` — error UI states
- `observability-slo` — error rate alerting

*Clean-room cross-platform error UX workflow.*
