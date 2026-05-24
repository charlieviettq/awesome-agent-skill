---
name: performance-optimization
description: >
  Measure, identify bottlenecks, fix, verify, and guard performance regressions.
  Use for web vitals, slow APIs, heavy notebooks/pipelines, or video/render workloads.
  Triggers: "performance", "optimize", "slow", "latency", "bundle size", "profiling".
---

# Performance optimization

## Workflow

```
MEASURE -> IDENTIFY -> FIX -> VERIFY -> GUARD
```

Never optimize without a baseline.

## Measure first

| Domain | Signals |
|--------|---------|
| Web | LCP, INP, CLS, bundle size, waterfall |
| API/DB | p50/p95 latency, query plans, N+1 |
| Data/ML | wall time, memory peak, I/O wait |
| Media | frame time, encode throughput |

## Identify

- Profile before guessing (browser Performance, py-spy, query EXPLAIN)
- One bottleneck at a time; document hypothesis

## Fix patterns (common)

| Issue | Direction |
|-------|-----------|
| Large JS bundle | Code split, lazy routes, tree-shake |
| Render churn | Memoization only when measured; virtualize lists |
| Slow queries | Indexes, fewer round trips, pagination |
| Pandas hot path | Vectorize, polars, smaller dtypes |

## Verify

- Compare before/after with same workload
- Check regressions on adjacent metrics (memory, error rate)

## Guard

- Budget thresholds in CI or release checklist
- `gstack/benchmark` for web regressions when applicable

## Related

`gstack/benchmark`, `frontend-engineering/frontend-ui-accessibility`, `observability-slo`

See [reference.md](reference.md) for a performance review checklist.
