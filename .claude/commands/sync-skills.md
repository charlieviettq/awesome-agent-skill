---
description: Sync skills between Cursor (source) and Claude (generated flat) formats
allowed-tools: Bash(python3:*)
---

## Default: Cursor → Claude

After editing `.cursor/skills/`:

```bash
python3 scripts/convert-to-claude.py --in-repo --force --write-map --prune-orphans
python3 scripts/validate-skills.py --parity
```

`--prune-orphans` removes stale nested trees under `.claude/skills/` (e.g. duplicate `knowledge-work/`, `voltagent-subagents/`) so only flat mapped skills remain.

## Recovery: Claude → Cursor

If you changed `.claude/skills/<flat-name>/` and need Cursor nested paths updated:

```bash
python3 scripts/convert-to-cursor.py --in-repo --only-newer
python3 scripts/convert-to-claude.py --in-repo --force --write-map --prune-orphans
python3 scripts/validate-skills.py --parity
```

Use `--force` on `convert-to-cursor` to overwrite Cursor even when newer on disk.

## Audit

```bash
python3 scripts/audit-skill-parity.py
```

Summarize convert counts, parity gaps, and whether validation passed.
