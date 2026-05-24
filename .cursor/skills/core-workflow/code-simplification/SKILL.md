---
name: code-simplification
description: Simplify working code while preserving behavior—remove dead paths, flatten nesting, clarify names, reduce duplication. Use after features work but code feels over-engineered. Triggers: "simplify", "clean up", "too complex", "YAGNI", "reduce complexity".
---

# Code Simplification

Behavior-preserving simplification pass on code that already works. Distinct from `design-smell-review` (structural critique before change) and `refactor-legacy-python-pr` (scoped legacy cleanup PRs).

## When to use

- Feature is done and tested; complexity exceeds need
- Review feedback says "over-engineered"
- Preparing a focused hygiene PR

## When not to use

- Bug is still open (fix behavior first)
- Large architectural rewrite (use `incremental-implementation`)
- No tests and behavior is unclear (add tests or spike first)

## Workflow

1. **Baseline** — confirm tests pass or define minimal manual checks
2. **Inventory** — list simplification targets (unused code, deep nesting, duplicate logic, premature abstraction)
3. **One change at a time** — small commits; run tests after each
4. **Stop** — when readability improves without expanding scope

## Safe simplifications

- Remove dead code and unused imports
- Inline one-use helpers when they obscure flow
- Replace cleverness with explicit steps
- Consolidate duplicate validation or mapping
- Narrow public API surface if callers allow

## Avoid

- Drive-by renames across unrelated files
- Changing behavior "while you're here"
- Removing abstractions that enable testing or extension without evidence

## Verification

- Same inputs → same outputs
- No new linter/type errors
- Diff stays reviewable (< ~300 lines unless agreed)

## Related skills

- `design-smell-review` — before deciding what to simplify
- `test-first-development` — lock behavior before deleting code
- `verify-before-done` — evidence before claiming complete

*Adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).*
