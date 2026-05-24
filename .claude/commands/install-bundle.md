---
description: Install starter or full skill bundle into a target project
argument-hint: <starter|full> <target-path>
allowed-tools: Bash(bash:*), Bash(rsync:*)
---

Install a predefined skill bundle.

Bundle argument: $ARGUMENTS

If arguments are missing, ask for bundle (`starter` or `full`) and target project path.

```bash
bash scripts/install/install-bundle.sh <bundle> <target-path> --format both
```

Report which domains were installed.
