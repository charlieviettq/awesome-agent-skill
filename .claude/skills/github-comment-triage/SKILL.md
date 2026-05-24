---
name: github-comment-triage
description: "Triage and address GitHub PR review comments systematically—classify, respond, fix or defer with rationale. Use when a PR has review feedback, requested changes, or unresolved threads."
allowed-tools: Read, Glob, Grep
---

# GitHub comment triage

## Workflow

1. **Collect** all open review threads and inline comments (not just summary).
2. **Classify** each item:
   - **Must fix** — correctness, security, contract break, CI
   - **Should fix** — clarity, maintainability, agreed convention
   - **Discuss** — ambiguous or product decision
   - **Defer** — out of scope; needs follow-up issue
3. **Order** must-fix first, then should-fix, then discuss.
4. **Implement** with minimal scoped changes; one logical commit per theme when possible.
5. **Reply** on each thread: what changed, where, or why deferred (link issue if deferred).
6. **Re-verify** tests/lint before requesting re-review.

## Response patterns

```text
Fixed in abc123 — [brief what changed]
```

```text
Deferred: tracked in #NNN — [reason and scope boundary]
```

## Anti-patterns

- Bulk "fixed" without pointing to commits or files.
- Ignoring nitpicks that hide real bugs.
- Expanding scope to unrelated refactors during comment sweep.

## Output

Checklist table: comment | action | status | note.
