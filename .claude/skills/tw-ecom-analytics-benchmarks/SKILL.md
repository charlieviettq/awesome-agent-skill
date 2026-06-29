---
name: "\"tw-ecom-analytics-benchmarks\""
description: "\"Taiwan e-commerce benchmark ranges for CVR, ROAS, LTV, AOV, repeat rate, cart-abandon — segmented by vertical (3C, 美妝, 服飾, 母嬰, 生鮮) and channel (DTC, Shopee, momo). Use when a TW merchant asks 'is my CVR / ROAS good?' or when sizing a business case. Source discipline: cite industry report or vendor data; mark undocumented ranges as estimates. STATUS: SKELETON — body pending.\"."
allowed-tools: Read, Glob, Grep
---

# Taiwan E-Commerce Benchmarks

> **STATUS: SKELETON** — body pending.

## When to use this skill

- A merchant asks "is my CVR / ROAS / LTV good?"
- Sizing a business case (revenue / ad-spend projections)
- Comparing performance across verticals or channels
- Investor / banker deck benchmarks

## Do NOT use when

- Instrumentation itself → `tw-ecom-analytics-ga4`
- Unit economics framework → `biz-unit-economics`

## Core concepts

TODO: benchmark tables by vertical × channel, sourced ranges with citations.

## Decision tree

TODO: merchant profile → applicable benchmark row.

## Implementation guidance

TODO: comparison template, outlier-flag criteria, what to do when outside range.

## Gotchas

TODO: 5-6 pitfalls (stale benchmarks, vertical misclassification, channel-mix distortion, attribution-model divergence, peak-period distortion).

## IRON LAW

TODO (candidate: "All benchmark ranges must cite source + year. An uncited number is worse than no number.").

## Output Format

TODO.

## Related

- `ecom-analytics`
- `biz-unit-economics`, `biz-cac-ltv`

_Last verified: 2026-04_
