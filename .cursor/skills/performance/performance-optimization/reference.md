# Performance checklist

## Before change

- [ ] Baseline metric recorded (tool + environment)
- [ ] Target improvement stated (e.g. p95 -30%)
- [ ] Scope bounded (one page, one endpoint, one job)

## Web frontend

- [ ] Critical path assets minimized
- [ ] Images sized and modern formats where useful
- [ ] Third-party scripts justified
- [ ] Caching headers for static assets

## Backend / API

- [ ] Pagination on large lists
- [ ] No unbounded payloads
- [ ] Connection pooling configured
- [ ] Expensive work async or queued when appropriate

## Data / Python

- [ ] Profiling run on representative sample
- [ ] I/O vs CPU bottleneck identified
- [ ] Memory peak acceptable

## After change

- [ ] Before/after numbers in PR or note
- [ ] No new errors or timeouts
- [ ] Regression guard noted (test, budget, or manual re-check)
