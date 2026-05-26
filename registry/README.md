# SkillHub Registry

Machine-readable metadata for SkillHub CLI, web catalog, and MCP server.

## Files

| File | Purpose |
|------|---------|
| `skills.json` | Generated index of all Cursor skills (do not edit by hand) |
| `bundles.json` | Curated install bundles (edit when adding bundles) |

## Regenerate skills index

```bash
python3 scripts/generate-registry.py
```

Run after adding or changing skills under `.cursor/skills/`. CI should keep `skills.json` in sync.

## Bundle format

Each bundle may define:

- `domains`: install entire top-level folders
- `skills`: explicit skill ids (e.g. `core-workflow/verify-before-done`)
- `install_all_domains`: set true only for `full` bundle
