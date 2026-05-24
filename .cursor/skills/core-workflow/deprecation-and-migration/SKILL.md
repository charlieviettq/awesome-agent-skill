---
name: deprecation-and-migration
description: >
  Plan deprecation and migration—replacement first, consumer migration, strangler
  and adapter patterns, zombie code removal. Use when sunsetting APIs, libraries,
  or legacy modules.
  Triggers: "deprecate", "migration plan", "sunset", "remove legacy", "strangler".
---

# Deprecation and migration

## Decision questions

1. Does the old system still provide unique value?
2. How many consumers? Migration cost each?
3. Is replacement production-proven?
4. Cost of NOT deprecating (security, maintenance)?

## Compulsory vs advisory

| Type | When |
|------|------|
| Advisory | Stable legacy, optional migration |
| Compulsory | Security risk, blocks progress — need tooling + deadline |

Default advisory unless risk justifies force.

## Process

1. **Build replacement** first
2. **Announce** — status, replacement, migration guide, timeline
3. **Migrate consumers** incrementally; owner migrates users when possible
4. **Remove** only after zero active usage verified

## Patterns

| Pattern | Use when |
|---------|----------|
| Strangler | Gradual traffic shift |
| Adapter | Old interface, new implementation |
| Feature flag | Per-consumer or cohort cutover |

## Zombie code signals

- No maintainer, active dependents, failing tests ignored, stale deps

## Output

Deprecation notice + migration steps + removal checklist.
