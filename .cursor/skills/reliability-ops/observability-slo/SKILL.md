---
name: observability-slo
description: >
  Lightweight observability and SLO practice—SLIs, SLO targets, error budgets,
  logs, metrics, traces, and alerting for apps and data pipelines.
  Use when defining monitoring, on-call alerts, or reliability targets.
  Triggers: "SLO", "SLI", "observability", "alerting", "error budget", "monitoring".
---

# Observability and SLO (lite)

## Three pillars (minimum viable)

| Pillar | Start here |
|--------|------------|
| Logs | Structured JSON; request/job ID; severity |
| Metrics | RED/USE for services; duration, errors, throughput |
| Traces | One trace per request/job across critical hops |

## SLI -> SLO flow

1. **Pick SLI** — measurable user- or business-visible signal.
2. **Set SLO** — target over window (e.g. 99.9% availability / 30d).
3. **Error budget** — 100% - SLO; spend triggers policy (slow features, freeze risky deploys).
4. **Alert on budget burn** — fast burn (pages) vs slow burn (ticket).

## Example SLIs

| Service type | SLI examples |
|--------------|--------------|
| API | Success rate, p95 latency |
| Batch job | Completion within SLA window |
| Model scoring | Scoring latency, feature freshness |

## Alert rules

- Page humans only for SLO-threatening or user-visible outages.
- Warning for degradation trending toward budget burn.
- Every alert links to a **runbook** (symptom, checks, mitigation, escalation).

## Runbook skeleton

```markdown
## Symptom
## Impact
## Checks (ordered)
## Mitigation
## Escalation
```

## Pipeline note

For data/ML jobs: monitor row counts, null spikes, partition lag, and scoring drift alongside infra metrics.

## Anti-patterns

- Alert on every log error without SLO linkage.
- SLOs without measurement (aspirational only).
- Dashboards nobody owns.
