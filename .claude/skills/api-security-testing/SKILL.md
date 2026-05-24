---
name: api-security-testing
description: "Security testing checklist for HTTP APIs—authn/z, input validation, rate limits, sensitive data exposure, and common OWASP API issues. Use when reviewing or testing REST/GraphQL endpoints before release."
allowed-tools: Read, Glob, Grep
---

# API security testing

## Preconditions

- Test in **non-production** unless explicitly authorized.
- Use dedicated test accounts; never real customer PII in payloads.

## Test matrix (prioritized)

### Authentication and session

- [ ] Missing/invalid token rejected (401)
- [ ] Expired or revoked credentials rejected
- [ ] Session fixation / cookie flags (HttpOnly, Secure, SameSite) where applicable

### Authorization

- [ ] Horizontal: user A cannot access user B's resource IDs
- [ ] Vertical: non-admin cannot invoke admin routes
- [ ] IDOR on path/query/body identifiers

### Input and abuse

- [ ] Oversized payloads rejected
- [ ] Injection surfaces parameterized (SQL, command, template)
- [ ] Rate limiting on auth and expensive endpoints

### Data exposure

- [ ] Errors do not leak stack traces or secrets in prod-like config
- [ ] Responses omit internal fields (tokens, hashes, full PAN)
- [ ] Pagination does not bypass auth filters

### Transport and config

- [ ] HTTPS enforced; HSTS where applicable
- [ ] CORS not `*` with credentials
- [ ] Security headers on API gateway if present

### Web-facing surfaces (when API serves or pairs with UI)

- [ ] CSP or explicit script policy documented
- [ ] CSRF protection on cookie-based mutations
- [ ] Clickjacking headers (`X-Frame-Options` or CSP `frame-ancestors`) where relevant
- [ ] File upload: type/size limits, virus scan hook if required by policy

## Reporting

For each finding: endpoint, steps, impact, severity, remediation, retest status.

## Boundaries

- Defensive testing only; no unauthorized production scanning.
- For deep pen-test, engage formal AppSec process.
