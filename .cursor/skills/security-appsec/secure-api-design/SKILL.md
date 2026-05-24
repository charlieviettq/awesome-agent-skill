---
name: secure-api-design
description: >
  Design and implement secure APIs—authentication patterns, authorization models,
  input validation, secrets handling, and safe defaults. Use when designing new
  endpoints, auth flows, or reviewing API contracts.
  Triggers: "secure API", "auth design", "JWT", "OAuth", "API best practices".
---

# Secure API design

## Defaults

- Deny by default; explicit allow per route and role.
- Validate at boundary; typed schemas (OpenAPI/JSON Schema/protobuf).
- Least privilege for service accounts and API keys.

## Authentication patterns

| Pattern | Use when | Notes |
|---------|----------|-------|
| Session cookie | Browser-first apps | CSRF protection, secure cookies |
| Bearer JWT | SPA/mobile, stateless | Short TTL, rotation, no sensitive claims in payload |
| API key | Machine-to-machine | Scoped keys, audit log, rate limits |
| OAuth2/OIDC | Third-party identity | Standard libraries; validate issuer/audience |

## Authorization

- Resource-level checks close to data access (not only route middleware).
- Avoid exposing sequential IDs without ownership check.
- Document policy matrix: role x action x resource.

## Contract-first (public APIs)

- Define OpenAPI/JSON Schema **before** implementation when the API is shared.
- Version breaking changes; additive fields preferred.
- **Hyrum's Law:** undocumented behavior becomes dependency—document or forbid.
- Stable error shape: machine-readable `code`, human `message`, optional `details[]`.
- Pagination: cursor preferred for large sets; cap `limit`; document sort order.

## Input and output

- Reject unknown fields on write endpoints when schema allows.
- Normalize encoding; limit string/array sizes.
- Redact secrets in logs; structured logging without raw tokens.

## Secrets

- Never commit secrets; use env/secret manager.
- Separate dev/stage/prod credentials.
- Rotate on leak suspicion.

## Implementation checklist

- [ ] Schema validation on all inputs
- [ ] Authn required except explicit public routes
- [ ] Authz enforced per resource
- [ ] Rate limits on login and expensive operations
- [ ] Security headers and TLS termination documented

## Related

Use `api-security-testing` before release for verification.
