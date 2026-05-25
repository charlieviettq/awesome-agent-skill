---
name: idea-refine
description: "Shape early ideas through divergent exploration and convergent narrowing before specs or builds. Use when brainstorming product features, model approaches, or architecture directions."
allowed-tools: Read, Glob, Grep
---

# Idea Refine

Early-stage idea shaping: generate options, stress-test assumptions, then narrow to a testable direction. Distinct from `planning-and-task-breakdown` (execution) and `spec-driven-development` (requirements lock).

## When to use

- Idea is directional but not actionable
- User wants alternatives before committing
- Trade-offs between 2–3 approaches need surfacing

## When not to use

- Requirements are already agreed
- User wants immediate implementation
- Pure research with no decision deadline

## Workflow

### Phase 1 — Diverge (2–4 options)

- Restate the problem in one sentence
- Propose distinct approaches (not minor variants)
- For each: upside, downside, effort tier (S/M/L), key assumption

### Phase 2 — Stress test

- What would make each option fail?
- What data or spike would de-risk the choice?
- What is explicitly out of scope?

### Phase 3 — Converge

- Recommend one direction with rationale
- List what to validate in the next 1–2 hours/days
- Present design in **short sections** the user can approve or correct before locking scope
- Hand off to `interview-me`, `spec-driven-development`, or `planning-and-task-breakdown`

### Before code

- Do not start implementation during brainstorming
- Do not auto-save specs or commit without explicit user request

## Output template

```markdown
## Idea refinement
- **Problem:**
- **Options considered:** (name + one-line summary each)
- **Recommendation:**
- **Why not the others:**
- **Next validation steps:**
```
