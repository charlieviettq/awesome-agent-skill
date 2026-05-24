---
name: meta-ads-analyzer
description: "Analyze Meta (Facebook/Instagram) ad performance—campaign structure, breakdowns, marginal vs average CPA, and scaling decisions. Analytical workflow only, not financial or legal advice."
allowed-tools: Read, Glob, Grep
---

# Meta Ads Analyzer

Structured analysis of Meta advertising accounts. Helps interpret metrics and structure experiments; does not replace professional media buying or compliance review.

## When to use

- Reviewing campaign performance or budget allocation
- Explaining CPA/ROAS changes across ad sets
- Planning scale/pause/hold decisions with data

## When not to use

- Creating ad creative (out of scope)
- Legal/compliance sign-off on claims or targeting
- Non-Meta platforms (adapt patterns manually)

## Core concepts

### Breakdown Effect

As spend increases, **average** CPA often rises even when incremental (marginal) ROI is still acceptable. Compare:

- **Average CPA** — total spend / total conversions (blends history)
- **Marginal CPA** — cost of the next incremental conversion (recent window or cohort)

Do not pause winning ad sets solely because average CPA crossed a target if marginal performance remains profitable.

### Analysis workflow

1. **Scope** — date range, attribution window, conversion event
2. **Structure** — campaign → ad set → ad; note learning phase status
3. **Breakdowns** — placement, age, gender, device, region (one at a time)
4. **Trends** — 7d vs prior 7d; flag sudden frequency or CPM spikes
5. **Recommendations** — scale, hold, refresh creative, consolidate, or test

## Metrics table

| Metric | Use |
|--------|-----|
| CPA / CPL | Efficiency vs target |
| ROAS | Revenue campaigns |
| Frequency | Creative fatigue signal |
| CTR / CPM | Top-of-funnel health |
| Conversion rate | Landing/offer fit |

## Output template

```markdown
## Meta ads readout
- **Period:**
- **Spend / conversions / CPA:**
- **Top performers:**
- **Underperformers:**
- **Breakdown insights:**
- **Recommended actions:** (with rationale)
- **Experiments to run:**
```

## Disclaimer

Analytical guidance only. Verify against Meta Business Help Center and your organization's policies. Past performance does not guarantee future results.

*Clean-room analytical workflow; not copied from external ad tooling.*
