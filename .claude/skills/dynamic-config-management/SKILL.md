---
name: dynamic-config-management
description: "Manage application configuration—schemas, validation, .env.example, placeholder detection, fail-fast startup. Use when adding env vars or centralizing config."
allowed-tools: Read, Glob, Grep
---

# Dynamic Config Management

Centralize and validate configuration at startup. Reduces "works on my machine" and silent misconfiguration in deployed environments.

## When to use

- New service or deploy target
- Mystery bugs from missing/wrong env vars
- Standardizing config across dev/staging/prod

## When not to use

- Secrets rotation policy (use team secret manager docs)
- Feature flag product logic (may overlap with feature-flag systems)

## Workflow

1. **Inventory** — list all config keys, required vs optional, defaults
2. **Schema** — validate types and allowed values (Zod, pydantic, envconfig, etc.)
3. **`.env.example`** — committed template with placeholders, no real secrets
4. **Fail fast** — app refuses to start if required keys missing or invalid
5. **Document** — README section: key, purpose, example placeholder

## Checklist

- [ ] No secrets in repo or logs
- [ ] Placeholder detection (`changeme`, `TODO`, empty required vars)
- [ ] Different files or prefixes per environment documented
- [ ] CI loads test config explicitly (not developer `.env`)
- [ ] Config dump endpoint disabled in production

## Anti-patterns

- Reading os.environ scattered across codebase
- Defaulting production credentials to dev values
- Silent fallbacks that hide misconfiguration

## Output

- Config schema module
- Updated `.env.example`
- Startup validation with actionable error messages
