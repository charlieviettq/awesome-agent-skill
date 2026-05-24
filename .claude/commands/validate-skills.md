---
description: Run skill validation (frontmatter, naming, triggers, links)
allowed-tools: Bash(python3:*)
---

Run the repository skill validator and report results.

```bash
python3 scripts/validate-skills.py
```

If validation fails, list each error with the file path and suggest the minimal fix. Do not modify unrelated skills.
