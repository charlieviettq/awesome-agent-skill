---
name: api-and-interface-design
description: Design API and module boundaries with clear contracts, error semantics, pagination, and additive compatibility. Use before implementing REST/GraphQL endpoints, SDKs, or public module APIs. Triggers: "API design", "interface contract", "endpoint design", "pagination", "error codes", "backward compatible".
---

# API and Interface Design

Contract-first design for HTTP APIs, GraphQL, CLI surfaces, and library module boundaries. Complements `secure-api-design` (security) and `agent-tool-contracts` (LLM tools) with general interface ergonomics and evolution rules.

## When to use

- New public or cross-team API
- Breaking-change review
- Designing pagination, filtering, idempotency, or error shapes

## When not to use

- Internal refactor with no boundary change
- Security-only audit (use `secure-api-design`)
- Agent tool schema only (use `agent-tool-contracts`)

## Design checklist

### Contract

- Resource naming consistent (nouns, plural collections)
- Versioning strategy documented (URL prefix, header, or additive-only)
- Request/response schemas with examples for happy path + common errors
- Idempotency keys for mutating operations where retries matter

### Errors

- Stable machine-readable codes separate from human messages
- HTTP/status mapping documented; no stack traces in client responses
- Validation errors: field-level detail when safe (no PII leakage)

### Pagination and lists

- Cursor-based preferred for large/live datasets; offset only when bounded
- Default and max page size documented
- Sort/filter params explicit; reject unknown params predictably

### Compatibility

- Additive changes only in minor versions
- Deprecation headers or sunset dates for removals
- Consumer migration notes in changelog

### Observability

- Correlation/request IDs in responses or logs
- Rate-limit headers where applicable

## Workflow

1. Draft resource model and primary use cases
2. Write example requests/responses (including errors)
3. Run `doubt-driven-review` or `secure-api-design` for high-risk surfaces
4. Implement with tests locked to contract examples

## Output

- Short design note or OpenAPI/GraphQL schema sketch
- Compatibility and deprecation table if evolving an existing API

## Related skills

- `secure-api-design` — authn/z, input validation, secrets
- `agent-tool-contracts` — LLM-facing tool schemas
- `deprecation-and-migration` — sunsetting old interfaces

*Adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).*
