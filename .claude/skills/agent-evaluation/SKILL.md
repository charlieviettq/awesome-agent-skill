---
name: agent-evaluation
description: "Evaluate LLM agents and tool-using workflows—task success, tool accuracy, latency/cost, safety, and regression suites. Use when shipping agent features, comparing prompts/models, or debugging agent failures."
allowed-tools: Read, Glob, Grep
---

# Agent evaluation

## What to measure

| Dimension | Examples |
|-----------|----------|
| Task success | End state matches spec (binary or rubric) |
| Tool use | Correct tool, valid args, no spurious calls |
| Safety | No policy violations, no secret leakage |
| Efficiency | Tokens, latency, tool call count |
| Stability | Same input -> consistent outcome across runs |

## Workflow

1. **Define tasks** — realistic user intents with clear pass/fail or scored rubric.
2. **Build dataset** — golden set + edge cases (errors, ambiguous input, empty context).
3. **Run baseline** — fixed model/settings; log traces (inputs, tools, outputs).
4. **Score** — automated checks first; human review for ambiguous cases.
5. **Compare** — A/B prompts, models, or tool schemas; report deltas with confidence notes.
6. **Gate** — block release on regression in must-pass tasks.

## Automated checks

- Schema validation on tool arguments.
- Assert final answer contains required fields or avoids forbidden content.
- Snapshot tests for deterministic sub-steps where possible.

## Human rubric (when needed)

Score 1-5 on: correctness, completeness, tone, safety. Document disagreements.

## Anti-patterns

- Eval only on cherry-picked happy paths.
- Changing task and model simultaneously without isolation.
- No trace logs when debugging tool failures.

## Output

Summary table: variant | success rate | avg tools | avg latency | notes.
