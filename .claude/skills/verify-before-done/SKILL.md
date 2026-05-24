---
name: verify-before-done
description: "Require fresh verification evidence before claiming tests pass, builds succeed, or work is complete. Use when finishing a task, creating a PR, or reporting status."
allowed-tools: Read, Glob, Grep
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

## Regression discipline

For bugfixes: failing test or repro first, fix, verify pass, optionally revert fix and confirm fail again.

## Output format

```text
Ran: pytest tests/foo.py -q
Result: 12 passed, exit 0
Claim: Tests pass for foo module.
```
