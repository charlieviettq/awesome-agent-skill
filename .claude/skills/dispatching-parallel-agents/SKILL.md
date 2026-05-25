---
name: dispatching-parallel-agents
description: "Split independent work across parallel agents with explicit boundaries and a parent integration review. Use only when user allows subagents and tasks do not share mutable files."
allowed-tools: Read, Glob, Grep
---

# Dispatching parallel agents

## Gate (required)

Use this skill **only if**:

- User or parent explicitly allows parallel subagents, **and**
- Tasks are independent (no shared files, no ordering dependency on partial output)

If either condition fails, use sequential `incremental-implementation` instead.

## When to use

- Independent reviews (security + tests + API contract) on the same commit
- Parallel research spikes with separate output files
- Large plan with disjoint file ownership per task

## When not to use

- Single shared module being edited by multiple agents
- Database migrations or sequential deploy steps
- User did not approve multi-agent execution

## Workflow

1. **Partition** — list tasks with disjoint `Files:` sets
2. **Brief** — each agent gets scope, constraints, verify command, output format
3. **Dispatch** — run parallel agents; cap concurrency to what the harness supports
4. **Collect** — gather outputs without assuming correctness
5. **Integrate** — parent reconciles conflicts, runs full verification, single commit strategy per user rules

## Integration checklist

- [ ] No conflicting edits to the same paths
- [ ] Combined diff reviewed by parent (or `requesting-code-review`)
- [ ] Full test/lint suite on integrated result
- [ ] User informed of what each agent did

## Anti-patterns

- Parallel implementers on the same feature branch without file boundaries
- Merging subagent output without reading diffs
- Spawning agents to avoid reading the codebase

## Related

`subagent-driven-development`, `incremental-implementation`, `requesting-code-review`, `verify-before-done`

*Orchestration patterns inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
