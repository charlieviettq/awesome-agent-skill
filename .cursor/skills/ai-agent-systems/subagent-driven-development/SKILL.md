---
name: subagent-driven-development
description: >
  Execute an approved plan via one subagent per task with spec and quality checks.
  Use only when user allows subagents and a written plan exists. Triggers: "subagent
  per task", "dispatch implementer", "agent per plan step".
---

# Subagent-driven development

## Gate (required)

Use **only if**:

- A written plan exists (`planning-and-task-breakdown` output) and user approved execution
- User or parent **explicitly allows** subagents for implementation
- Each task has clear files, acceptance, and verify steps

Otherwise use `incremental-implementation` in the main agent.

## Workflow

```
For each plan task:
  1. Implementer subagent -> minimal change for task only
  2. Spec check -> matches acceptance criteria
  3. Quality check -> tests, style, scope (parent or review subagent)
  4. Parent integrates -> run verify-before-done for slice
```

## Implementer brief (per task)

```markdown
## Task
- **Title:**
- **Files (only these):**
- **Acceptance:**
- **Verify:**
- **Do not:** edit other files, refactor drive-by, commit unless instructed
```

## Parent responsibilities

- Own git strategy (commit per slice only if user/repo expects it)
- Resolve conflicts between tasks
- Stop plan if two tasks need the same file
- Never claim full plan done until all tasks verified

## Two-stage review

| Stage | Question |
|-------|----------|
| Spec compliance | Does the change meet acceptance and stay in scope? |
| Code quality | Tests, clarity, security, maintainability |

Critical spec failures block the next task.

## Anti-patterns

- Subagents rewriting the plan mid-flight
- Parallel implementers without `dispatching-parallel-agents` guards
- Auto-commit/push from subagents without parent approval

## Related

`dispatching-parallel-agents`, `incremental-implementation`, `requesting-code-review`, `receiving-code-review`, `verify-before-done`

*Workflow inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
