---
name: systematic-debugging
description: "Four-phase root-cause debugging—reproduce, compare patterns, hypothesize, fix with tests. Use when errors are unclear, fixes failed twice, or symptoms keep returning."
allowed-tools: Read, Glob, Grep
---

# Systematic debugging

## Iron law

No fixes without a **reproduced** failure and a **testable hypothesis**. After three failed fix attempts, question architecture or assumptions.

## When to use

- Intermittent or unclear failures
- Prior "quick fixes" did not hold
- Multiple subsystems involved (API, DB, cache, agent tools)

## When not to use

- Typo or one-line obvious fix with clear error message
- User only wants a stack trace explained, not a fix

## Four phases

### 1. Reproduce

- Capture exact steps, inputs, environment, and error output
- Minimize repro (one test, one script, one URL)
- Confirm you can trigger the failure on demand

### 2. Compare

- What changed recently (code, config, deps, data)?
- Find a **known-good** comparison (last green commit, sibling module, docs example)
- Diff behavior, not only code

### 3. Hypothesize

- List 2–3 plausible causes ranked by likelihood
- For each: one experiment that would confirm or rule it out
- Prefer experiments that take minutes, not hours

### 4. Fix with test

- Add or extend a test that fails for the current bug
- Apply minimal fix; re-run repro and test
- Run `verify-before-done` before claiming fixed

## Escalation

| Signal | Action |
|--------|--------|
| 3+ failed fix attempts | Stop; write findings; propose design/architecture review |
| Cannot reproduce | Gather more data; do not patch blindly |
| Fix works locally only | Check env parity, feature flags, cached state |

## Anti-patterns

- Random changes until something "seems" fixed
- Fixing symptoms (broad try/catch, silent rescue) without root cause
- Skipping repro because "it's obvious"

## Related

`test-first-development`, `test-failure-triage`, `verify-before-done`, `gstack/code-quality/investigate`

*Workflow inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
