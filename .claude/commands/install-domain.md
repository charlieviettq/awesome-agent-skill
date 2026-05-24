---
description: Install a skill domain into a target project
argument-hint: <domain> <target-path> [cursor|claude|both]
allowed-tools: Bash(bash:*), Bash(rsync:*)
---

Install skills from this repository into a target project using install scripts.

Domain argument: $ARGUMENTS

If arguments are missing, ask for:
1. Domain folder (e.g. `core-workflow`, `security-appsec`)
2. Target project absolute path
3. Format: `cursor`, `claude`, or `both` (default `both`)

Then run:

```bash
bash scripts/install/install-domain.sh <domain> <target-path> --format <format>
```

Confirm installed paths and remind user to reload the agent session.
