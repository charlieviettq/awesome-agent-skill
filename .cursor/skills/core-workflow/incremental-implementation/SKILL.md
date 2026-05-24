---
name: incremental-implementation
description: >
  Implement multi-file changes in thin vertical slices—implement, test, verify,
  commit. Use when a feature touches more than one file or feels too large for one pass.
  Triggers: "incremental", "vertical slice", "one step at a time", "small commits".
---

# Incremental implementation

## Cycle

Implement -> Test -> Verify -> Commit -> next slice

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

## Anti-patterns

- 100+ lines without running tests
- Mixing refactor with feature in one increment
- Re-running same passing command without code changes

## Related

`test-first-development`, `verify-before-done`, `planning-and-task-breakdown`
