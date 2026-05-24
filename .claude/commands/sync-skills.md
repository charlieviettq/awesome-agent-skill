---
description: Regenerate Claude skills from Cursor source and update skill map
allowed-tools: Bash(python3:*)
---

Regenerate Claude-format skills after Cursor source edits.

```bash
python3 scripts/convert-to-claude.py --in-repo --force --write-map
python3 scripts/validate-skills.py
```

Summarize how many skills were converted and whether validation passed.
