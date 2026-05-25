---
name: test-first-development
description: "Apply test-first discipline for behavior changes and bugfixes: define expected behavior, add or run a failing test, then implement minimally. Use when fixing bugs, changing logic, or adding features that need regression protection."
allowed-tools: Read, Glob, Grep
---

# Test-first development

## When to use (default)

- Bug fixes with reproducible symptoms.
- Behavior changes in production code.
- Refactors where regression risk is non-trivial.

## When to relax (document why)

- Throwaway prototypes.
- Generated code with separate validation.
- Pure config or documentation-only changes.

## Workflow (RED-GREEN-REFACTOR)

1. **Define** expected behavior in one sentence.
2. **RED:** Add or identify a test that fails for the right reason (missing behavior, not typo). Run it and confirm failure.
3. **GREEN:** Minimal code to pass. Run the same test and confirm pass.
4. **REFACTOR:** Only after green; keep tests passing.
5. **Verify:** Run targeted tests, then broader suite if scope warrants.

For bugfixes: if production code was written before the failing test, treat as process violation—add the test, confirm fail, then fix.

## Good tests

- One behavior per test; name describes behavior.
- Prefer testing real code paths over heavy mocking.
- For bugs: test reproduces the reported symptom.

## Checklist before done

- [ ] New or updated test exists for the change
- [ ] Saw the test fail before the fix (bugfixes)
- [ ] Targeted tests pass
- [ ] No unrelated test failures introduced

## Testing anti-patterns

- Implement first, add tests only at the end for logic changes.
- Tests that pass immediately without proving anything.
- Vague test names (`test1`, `test_fix`).
- Heavy mocking that does not assert real behavior.
- Test-only methods or flags added to production code solely to make tests pass.
- Incomplete mocks that hide integration failures.

## Related

`systematic-debugging`, `test-failure-triage`, `verify-before-done`

*TDD discipline inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
