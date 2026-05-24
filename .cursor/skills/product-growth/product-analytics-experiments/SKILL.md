---
name: product-analytics-experiments
description: >
  Product analytics and experimentation—event design, funnel metrics, tracking
  plans, and A/B test setup with statistical and operational gates. Use when
  defining metrics, launch experiments, or reviewing growth/DS product work.
  Triggers: "A/B test", "experiment", "funnel", "tracking plan", "product analytics".
---

# Product analytics and experiments

## Event and tracking design

- **One event = one user action** with stable name and versioned schema.
- Required context: `user_id` or anonymous id, `timestamp`, `session_id`, product surface.
- Document in a tracking plan: event, properties, trigger, owner, PII classification.

## Core metrics

| Type | Examples |
|------|----------|
| Acquisition | Signups, activation rate |
| Engagement | DAU/WAU, feature adoption |
| Conversion | Funnel step rates |
| Retention | D1/D7/D30 cohort retention |
| Quality | Error rate, task success |

Define **denominator** explicitly (eligible users, not all traffic).

## Funnel analysis

1. Define steps and entry criteria.
2. Check identity stitching and time window.
3. Segment by platform, cohort, campaign (avoid Simpson's paradox surprises).

## A/B test gates (before launch)

- [ ] Hypothesis and primary metric (one primary)
- [ ] Guardrail metrics (latency, errors, revenue risk)
- [ ] Randomization unit correct (user vs session)
- [ ] Sample size / MDE estimated; duration planned
- [ ] No peeking-driven early stop without sequential plan
- [ ] Feature flags and exposure logging verified in staging

## Analysis

- Intent-to-treat as default; document exclusions.
- Report: point estimate, CI, practical significance (not only p-value).
- Slice only with pre-registration or clear exploration label.

## Anti-patterns

- Changing primary metric after results visible.
- Multiple simultaneous experiments on same surface without interaction analysis.
- Tracking PII without legal/product review.

## Output

Experiment brief: hypothesis, design, metrics, ship/kill criteria, results template.
