---
name: shipping-launch-checklist
description: >
  Pre-launch and rollout checklist—feature flags, thresholds, rollback, monitoring,
  and comms. Use before production releases or risky deploys.
  Triggers: "launch", "ship to prod", "rollout", "release checklist", "go live".
---

# Shipping and launch checklist

## Pre-launch

- [ ] Success criteria and rollback trigger defined
- [ ] Feature behind flag or dark launch when possible
- [ ] Migrations backward-compatible or reversible plan
- [ ] Dashboards/alerts for new paths (`observability-slo`)
- [ ] Runbook: who to page, how to revert

## Rollout

| Strategy | When |
|----------|------|
| Big bang | Low risk, small blast radius |
| Percentage | Gradual exposure with metrics watch |
| Cohort/region | Geo or tenant isolation first |

## During rollout

- Watch error rate, latency, business KPIs vs baseline
- Stop or roll back if thresholds breached (define before launch)

## Post-launch

- [ ] Remove temporary flags after stable period
- [ ] Document known issues and follow-ups
- [ ] Postmortem if incident (`postmortem-writing`)

## Related

`gstack/ship`, `gstack/land-and-deploy`, `gstack/canary`, `observability-slo`
