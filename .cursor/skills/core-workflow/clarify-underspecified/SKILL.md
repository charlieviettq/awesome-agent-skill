---
name: clarify-underspecified
description: >
  Ask the minimum clarifying questions before implementing when scope, constraints,
  or success criteria are unclear. Use when a request has multiple plausible
  interpretations, missing acceptance criteria, or ambiguous environment constraints.
  Triggers: "unclear", "ambiguous", "not sure what you want", "multiple options".
---

# Clarify underspecified requests

## When to use

- Multiple plausible interpretations exist.
- Objective, scope, constraints, or "done" criteria are missing.
- Quick read-only discovery cannot resolve the ambiguity.

## When not to use

- Request is already specific enough to proceed.
- A short repo/config read answers the open questions.

## Workflow

1. Decide if the request is underspecified (objective, scope, constraints, environment, safety).
2. Ask **1-5** questions max; prefer multiple-choice with a `defaults` fast path.
3. Separate **need to know** vs **nice to know**.
4. Do not run mutating commands or commit to a detailed plan until must-have answers arrive.
5. If the user asks to proceed without answers, state assumptions explicitly and get confirmation.

## Question format

```text
1) Scope?
a) Minimal change (default)
b) Broader refactor in the same area
c) Not sure - use default

Reply: defaults (or 1a 2b)
```

## Anti-patterns

- Do not ask what a quick read of repo/docs already answers.
- Do not ask open-ended questions when a yes/no or A/B choice is faster.

## Output

Restate requirements in 1-3 sentences (constraints + success criteria), then start work.
