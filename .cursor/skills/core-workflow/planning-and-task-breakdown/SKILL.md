---
name: planning-and-task-breakdown
description: >
  Decompose specs into small, ordered tasks with acceptance criteria and verification
  steps. Use when you have requirements and need an implementable plan or task list.
  Triggers: "break down tasks", "implementation plan", "task breakdown", "plan mode".
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

## High-quality plan checklist

- Each task is small enough to complete in one focused session (roughly 2–15 minutes of agent work)
- **Files:** lists exact paths to create or edit (no "update relevant files")
- **Verify:** includes full command and expected outcome (exit code, key output line)
- No placeholders like "add tests here" or "implement logic"
- For behavior changes, note which test should fail first (TDD) when applicable

## Task template

```markdown
## Task N: [Title]
**Acceptance:** ...
**Verify:** `command` -> expected result
**Depends on:** ...
**Files:** path/to/file.ext, path/to/test.ext
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

*Plan quality patterns inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
