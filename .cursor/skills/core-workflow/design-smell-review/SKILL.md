---
name: design-smell-review
description: >
  Lightweight design smell review for modules and APIs—coupling, cohesion,
  naming, boundaries, and unnecessary complexity. Use before large refactors or
  when code feels hard to change. Complements gstack/review (diff-focused).
  Triggers: "design review", "code smell", "too complex", "refactor structure".
---

# Design smell review

## Scope

Review **structure and boundaries**, not line-by-line style. Pair with PR diff review for changes; use this for module-level health.

## Smell checklist

| Smell | Signal | Direction |
|-------|--------|-----------|
| God module | Many unrelated responsibilities | Split by domain |
| Shotgun surgery | One change touches many files | Consolidate logic |
| Feature envy | Module A mostly uses B's data | Move behavior |
| Leaky abstraction | Impl details escape API | Narrow public surface |
| Config soup | Magic strings everywhere | Named constants / schema |
| Boolean flags | `if is_x` branches everywhere | Polymorphism or strategy |

## Workflow

1. Map **entry points** and **dependencies** (imports, public API).
2. List **responsibilities** per module; flag >1 unrelated core job.
3. Check **testability** — can core logic run without I/O?
4. Propose **smallest** structural improvement (not full rewrite).
5. Record decision in ADR if trade-off is significant.

## Output format

```text
## Summary
[1-2 sentences]

## Smells (priority order)
1. [Smell] — evidence — suggested fix (effort: S/M/L)

## Recommended next step
[One concrete change to try first]
```

## Simplification (Chesterton's Fence)

Before deleting or collapsing code, ask **why it exists**:

- Comment, test, or git history explaining constraint?
- If unknown, prefer small experiment or question over bulk delete.
- Remove duplication only when behavior is proven identical.
- "Fewer lines" is not success if edge cases or observability regress.

## Boundaries

- Do not block small fixes on perfect architecture.
- Prefer incremental extraction over big-bang rewrites.
