---
name: verify-before-done
description: >
  Require fresh verification evidence before claiming tests pass, builds succeed,
  or work is complete. Use when finishing a task, creating a PR, or reporting status.
  Triggers: "done", "fixed", "passes", "ready to merge", "all tests green".
---

# Verify before done

## Iron rule

No completion claims without **fresh verification evidence** in the current turn.

## Gate (before claiming success)

1. **Identify** what command proves the claim (test, lint, build, repro).
2. **Run** the full command (not a partial check from memory).
3. **Read** exit code and full relevant output.
4. **Verify** output matches the claim.
5. **Then** state the claim with evidence.

## Common claims vs proof

| Claim | Requires | Not sufficient |
|-------|----------|----------------|
| Tests pass | Test command, 0 failures | Previous run, "should pass" |
| Linter clean | Linter output, 0 errors | Build passed |
| Bug fixed | Repro test passes | Code changed only |
| Requirements met | Checklist vs plan | Tests pass alone |

## Red flags (stop and verify)

- "Should", "probably", "seems to"
- Satisfaction before running checks
- Trusting subagent or prior message without re-running
- Partial verification only

## Requirements met (not tests alone)

- Map plan/spec acceptance criteria to evidence (test output, screenshot, API response, manual step)
- A green test suite does not prove every requirement if scope included non-testable items

## Regression discipline

For bugfixes: failing test or repro first, fix, verify pass, optionally revert fix and confirm fail again.

## Branch completion (lightweight)

- Before claiming PR-ready: tests/lint/build per project norms, no known blockers, user informed of scope
- Do not discard branches, force-merge, or cleanup worktrees without explicit user approval

*Verification gate inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*

## Output format

```text
Ran: pytest tests/foo.py -q
Result: 12 passed, exit 0
Claim: Tests pass for foo module.
```
