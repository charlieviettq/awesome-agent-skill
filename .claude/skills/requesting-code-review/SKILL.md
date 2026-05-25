---
name: requesting-code-review
description: "Request a focused code review with scope, diff context, and severity-ordered findings. Use before merge or between plan tasks when quality gate is needed."
allowed-tools: Read, Glob, Grep
---

# Requesting code review

## When to use

- Before landing a significant PR or slice
- After completing a plan task that touches shared contracts
- When risk is high (auth, money, data migration, agent tools)

## When not to use

- Trivial typo-only changes with no behavior impact
- User explicitly wants speed over review

## Prepare review packet

1. **Scope** — what changed and what was intentionally out of scope
2. **Base** — branch name and commit range or PR link
3. **Risk areas** — files or behaviors reviewers should scrutinize
4. **Verification already run** — commands + outcomes (paste evidence)
5. **Questions** — specific uncertainties for the reviewer

## Review request template

```markdown
## Review request
- **Scope:**
- **Base / range:**
- **Risk areas:**
- **Verification run:**
- **Open questions:**
- **Severity scale:** Critical / High / Medium / Low / Nit
```

## Using a reviewer subagent (optional)

Only when user or parent agent **explicitly allows** subagents:

- Pass the packet above; do not pass unrelated context
- Ask for findings ordered by severity with file:line references
- Parent agent integrates findings; subagent does not merge or push

For deep structural review, `gstack/code-quality/review` may be used as an optional supplement.

## After review

- Triage findings with `receiving-code-review`
- Re-run verification before claiming addressed

## Anti-patterns

- "Please review everything" with no scope
- Starting review before tests pass locally
- Treating nitpicks as blockers without trade-off discussion

## Related

`receiving-code-review`, `verify-before-done`, `doubt-driven-review`, `github-comment-triage`

*Patterns inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
