---
name: spec-driven-development
description: >
  Write a structured spec before significant implementation—objective, commands,
  boundaries, testing, and success criteria. Use when starting a feature, project,
  or multi-file change without a written spec.
  Triggers: "write spec", "PRD", "requirements", "spec before code", "what are we building".
---

# Spec-driven development

## When to use

- New feature, project, or significant change
- Requirements ambiguous or multi-file scope
- Architectural decision needed before code

## When not to use

- Single-line fixes, typos, obvious one-file changes

## Gated workflow

```
SPECIFY -> PLAN -> TASKS -> IMPLEMENT
```

Do not implement until spec (or explicit assumptions) is agreed.

## Chunked approval

- Present spec sections in digestible chunks (objective, boundaries, testing) when scope is large
- Ask for explicit approval or corrections per chunk before moving to plan/tasks
- Do not treat silence as sign-off

## Spec sections (minimum)

1. **Objective** — user, problem, success criteria
2. **Commands** — build, test, lint, dev (full commands)
3. **Structure** — where code, tests, docs live
4. **Code style** — one example snippet beats paragraphs
5. **Testing** — framework, levels, coverage expectations
6. **Boundaries** — Always / Ask first / Never

## Assumptions block

Before writing the spec, list assumptions and ask for correction:

```text
ASSUMPTIONS:
1. ...
2. ...
-> Correct me or I proceed with these.
```

## Success criteria

Reframe vague asks into testable conditions (metrics, dates, thresholds).

## Living document

Update spec when scope or decisions change; link spec sections in PRs.

## Related

- `clarify-underspecified` — when spec inputs are missing
- `planning-and-task-breakdown` — after spec is approved
- `incremental-implementation` — during build

See [reference.md](reference.md) for a lightweight template.

*Workflow patterns inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
