---
name: test-failure-triage
description: >
  Systematically triage failing tests by grouping errors, fixing root causes in
  priority order, and verifying incrementally. Use when CI fails, test suite is
  broken, or multiple tests fail after a refactor or merge.
  Triggers: "tests failing", "fix tests", "CI red", "make tests pass".
---

# Test failure triage

## Workflow

### 1. Baseline run

Run the project's standard test command and capture full output (counts, error types, files).

### 2. Group failures

Group by:

- **Error type:** ImportError, AttributeError, AssertionError, etc.
- **Root file/module:** Same file causing multiple failures.
- **Likely cause:** Recent change area (use `git diff`, recent commits).

Prioritize groups with highest **downstream impact** (imports/config before assertion tweaks).

### 3. Fix order

1. Infrastructure: imports, deps, config, env
2. API/signature changes: renamed modules, function args
3. Logic: assertion and business-logic failures

### 4. Verify per group

After each group fix, re-run a **focused subset** (file or pattern), then full suite at the end.

```bash
# Example patterns (adapt to project)
pytest path/to/test_file.py -v
pytest -k "pattern" -v
make test
```

## Practices

- Fix one group at a time; do not mix unrelated fixes in one commit if avoidable.
- Prefer minimal changes; match project test style.
- Document external factors (flaky tests, env-only failures).

## Output

Short summary: total failures, groups fixed, remaining risks, final full-suite result.
