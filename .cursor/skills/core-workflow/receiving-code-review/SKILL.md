---
name: receiving-code-review
description: >
  Receive code review feedback constructively—verify claims, prioritize fixes,
  push back with evidence when needed. Use when acting on reviewer comments or
  preparing a second review round.
  Triggers: "code review", "reviewer said", "address review", "feedback on PR".
---

# Receiving code review

## Mindset

- Reviewers surface risk you may have missed; treat feedback as input, not orders.
- Verify technical claims before changing code (read code, run tests).

## Workflow

1. **Read fully** — understand intent, not only the literal suggestion.
2. **Clarify** — if feedback is vague, ask one focused question before partial implementation.
3. **Verify** — reproduce issue or confirm the concern in code; do not assume the reviewer is correct.
4. **Prioritize** — correctness and security before style.
5. **Respond** — agree + fix, or disagree with evidence (snippet, test, spec).
6. **Batch** related fixes; avoid drive-by changes outside review scope.
7. **Confirm** — run verification before marking threads resolved.

## When to push back

- Suggestion breaks API contract without migration plan.
- Fix is out of PR scope (offer follow-up issue).
- Reviewer assumption is wrong (show counter-evidence).

## When to accept quickly

- Naming/clarity that matches project conventions.
- Missing tests for changed behavior.
- Security or data-handling gaps.

## Anti-patterns

- Defensive replies without technical substance.
- Blindly applying every suggestion without understanding.
- Scope creep disguised as "while we're here".
- Implementing every comment without verifying technical accuracy.

## Related

`requesting-code-review`, `github-comment-triage`, `verify-before-done`

*Review handling patterns inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
