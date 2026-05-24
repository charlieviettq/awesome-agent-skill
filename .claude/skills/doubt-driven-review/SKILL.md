---
name: doubt-driven-review
description: "Adversarial fresh-context review for non-trivial decisions before they stand. Use for production-impacting logic, security-sensitive changes, unfamiliar code, or high-blast-radius architecture choices."
allowed-tools: Read, Glob, Grep
---

# Doubt-driven review

## Non-trivial when

- Branching logic or cross-module boundary changes
- Properties types/compiler cannot verify
- Irreversible deploy, migration, or public API change

## When not to use

- Renames, formatting, obvious one-liners

## Cycle

1. **CLAIM** — decision + why it matters (2-3 lines)
2. **EXTRACT** — artifact + contract only (no reasoning journey)
3. **DOUBT** — fresh review with adversarial prompt ("find issues, do not validate")
4. **RECONCILE** — classify: contract misread / actionable / trade-off / noise
5. **STOP** — trivial findings only, 3 cycles max, or user says ship

## Reviewer input

Pass **ARTIFACT + CONTRACT** only—not your CLAIM (avoids agreement bias).

## Reconcile precedence

1. Contract misread — fix contract, re-run
2. Valid actionable — change artifact
3. Valid trade-off — document explicitly
4. Noise — note and move on

## Optional second opinion

Offer cross-model or `codex review` for high stakes; user decides. Never silent skip.

## Related

`verify-before-done`, `test-first-development` (RED step as behavioral doubt), `gstack/review` (post-hoc PR)
