---
name: planning-and-task-breakdown
description: "Decompose specs into small, ordered tasks with acceptance criteria and verification steps. Use when you have requirements and need an implementable plan or task list."
allowed-tools: Read, Glob, Grep
---

# Planning and task breakdown

## When to use

- Spec or requirements exist but work is too large to start
- Need dependency order, checkpoints, or parallelization notes

## When not to use

- Obvious single-file change with clear acceptance criteria

## Process

1. **Read-only plan mode** — map codebase patterns; no code yet
2. **Dependency graph** — foundations before dependents
3. **Vertical slices** — prefer end-to-end thin slices over horizontal layers
4. **Write tasks** — each with acceptance + verify + files + size
5. **Checkpoints** — every 2-3 tasks, full verify

## Task template

```markdown
## Task N: [Title]
**Acceptance:** ...
**Verify:** test/build/manual check
**Depends on:** ...
**Files:** ...
**Size:** S | M | L (L = split further)
```

## Sizing

| Size | Files | Guidance |
|------|-------|----------|
| S | 1-2 | One endpoint or component |
| M | 3-5 | One feature slice |
| L | 5+ | Split before implementing |

## Parallelization

- Safe parallel: independent slices, docs, tests for stable code
- Sequential: migrations, shared contracts, shared state

## Output

Plan doc with phases, risks, open questions. Human approval before implementation.

## Related

`spec-driven-development`, `incremental-implementation`, `verify-before-done`
