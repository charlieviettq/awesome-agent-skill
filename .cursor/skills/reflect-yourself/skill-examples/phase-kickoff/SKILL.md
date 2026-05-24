---
name: phase-kickoff
description: Convert the current phase doc into an ordered execution plan and propose work packages (spec-first + tiered tests), including RTL/Hebrew checks.
---
# Phase Kickoff (Spec-first + Israeli-first)

**Workflow:** When invoked, use plan mode first to present the plan for review. Only create files after the user explicitly approves the plan and asks to implement it.

Inputs:
- Phase file (default: `docs/phases/CURRENT.md`)
- Desired parallelism (single vs 2–3 tracks)

Output:
1) Phase summary
2) Ordered plan by epics
3) Proposed work packages with:
   - title, goal, acceptance criteria
   - spec checklist (contracts, invariants, error codes)
   - criticality (CRITICAL vs STANDARD)
   - RTL/Hebrew obligations (if UI)
   - dependencies + risks
4) First work package to execute now

**Todos and project-tracking:** When creating the plan (or when the user approves it), add every deliverable/step as a todo. Always include a todo to update CURRENT.md per the project-tracking skill (set current phase, epic, work package so state stays in sync). Do not leave the todo list empty for a kickoff that has multiple deliverables.
