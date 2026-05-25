---
name: incremental-implementation
description: >
  Implement multi-file changes in thin vertical slices—implement, test, verify,
  commit. Use when a feature touches more than one file or feels too large for one pass.
  Triggers: "incremental", "vertical slice", "one step at a time", "small commits".
---

# Incremental implementation

## Before executing a plan

1. Read the full plan; flag ambiguities or missing verify steps
2. Confirm dependency order and shared-file hotspots
3. Get explicit go-ahead unless user already approved the plan
4. Execute **one task at a time**; stop and report if blocked

## Cycle

Implement -> Test -> Verify -> Commit (if user/repo expects commits) -> next slice

## Slicing strategies

| Strategy | Use when |
|----------|----------|
| Vertical slice | Default — one working path end-to-end |
| Contract-first | Parallel FE/BE — define API/types first |
| Risk-first | Highest uncertainty first |

## Rules

1. **One logical change** per increment
2. **Keep build green** after each slice
3. **Feature flags** for incomplete user-visible work
4. **Safe defaults** — opt-in for risky behavior
5. **Scope discipline** — note adjacent issues, do not fix unless asked
6. **Rollback-friendly** — prefer additive changes; separate delete from replace

## Simplicity check

Before finishing a slice: fewest lines? abstractions earned? staff-engineer "why not just..."?

## Per-slice checklist

- [ ] One clear purpose
- [ ] Existing tests pass
- [ ] New behavior verified
- [ ] Committed with descriptive message

## Stop-on-blocker

- If a task fails verification twice, stop and report hypothesis + options
- Do not skip ahead to later tasks while leaving a broken slice
- Do not auto-merge, auto-delete branches, or auto-create git worktrees

## Worktree hygiene (optional)

- Prefer the current branch unless user requests isolation
- If using a worktree: confirm branch name, run setup/tests once, avoid editing `.gitignore` without approval

## Anti-patterns

- 100+ lines without running tests
- Mixing refactor with feature in one increment
- Re-running same passing command without code changes
- Announcing "done" for the whole plan when only one slice finished

## Related

`test-first-development`, `verify-before-done`, `planning-and-task-breakdown`, `systematic-debugging`

*Execution discipline inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
