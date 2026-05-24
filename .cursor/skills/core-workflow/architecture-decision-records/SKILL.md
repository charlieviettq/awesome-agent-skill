---
name: architecture-decision-records
description: >
  Create and maintain Architecture Decision Records (ADRs) for significant technical
  choices—frameworks, data stores, API shapes, ML platform decisions. Use when
  documenting a decision, onboarding, or superseding a prior approach.
  Triggers: "ADR", "architecture decision", "document decision", "why we chose".
---

# Architecture decision records

## When to write an ADR

| Write ADR | Skip ADR |
|-----------|----------|
| New framework or major dependency | Minor version bump |
| Database or storage choice | Bug fix |
| API or integration pattern | Config-only change |
| Security or auth architecture | Routine maintenance |

## Lifecycle

`Proposed` -> `Accepted` -> `Deprecated` -> `Superseded`

Do not rewrite accepted ADRs; add a new ADR that supersedes the old one.

## Required sections

1. **Context** — problem and constraints
2. **Decision** — what was chosen (one clear statement)
3. **Consequences** — positive, negative, risks and mitigations
4. **Status** and date

## Optional (recommended for significant decisions)

- Decision drivers (numbered)
- Considered options with honest pros/cons
- Related ADRs / links

## Lightweight template

```markdown
# ADR-NNNN: Title

**Status:** Accepted | **Date:** YYYY-MM-DD

## Context
[Why we needed to decide]

## Decision
[What we decided]

## Consequences
**Positive:** ...
**Negative:** ...
**Risks:** ... **Mitigation:** ...
```

## Full MADR-style templates

See [reference.md](reference.md) for extended templates (standard, Y-statement, deprecation).

## Practices

- Write before implementation starts when possible.
- Keep ADRs short (1-2 pages); link deep dives elsewhere.
- Be honest about trade-offs.
