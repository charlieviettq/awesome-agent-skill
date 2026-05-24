---
name: interview-me
description: "Extract user intent through structured one-question-at-a-time interviews before specs or implementation. Use when requirements are fuzzy, the user says \"help me think through\", or you need success criteria before planning."
allowed-tools: Read, Glob, Grep
---

# Interview Me

Structured intent extraction before specs, plans, or code. Complements `clarify-underspecified` with a stricter one-question cadence and explicit stop conditions.

## When to use

- User has a goal but not a spec
- Multiple interpretations exist and batch questions would overwhelm
- Before `spec-driven-development` or `planning-and-task-breakdown`

## When not to use

- User already provided a complete spec or ticket
- Single factual question suffices
- Emergency fix with clear repro steps

## Workflow

1. **State purpose** — one sentence on what you are extracting (goal, constraints, success criteria).
2. **Ask one question** — highest-leverage unknown only; offer 2–4 concrete options when helpful.
3. **Listen and summarize** — after each answer, one-line recap of what you learned.
4. **Stop when** — you can write: objective, non-goals, constraints, acceptance criteria, and open risks.
5. **Hand off** — produce a short intent brief or propose `spec-driven-development`.

## Rules

- Never ask more than one question per turn unless user explicitly requests a batch.
- Prefer multiple-choice or examples over open-ended vagueness.
- Do not start implementation until stop condition is met or user waives interview.
- Flag assumptions explicitly; do not silently fill gaps.

## Output template

```markdown
## Intent brief
- **Objective:**
- **Non-goals:**
- **Constraints:**
- **Success criteria:**
- **Open risks:**
- **Next step:** spec / plan / spike / implement
```
