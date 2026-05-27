# GStack version tracking

This repo vendors the [garrytan/gstack](https://github.com/garrytan/gstack) skill pack under `.cursor/skills/gstack/`. Upstream is the source of truth for pack content; this document records what we have synced.

## Current sync

| Field | Value |
|-------|-------|
| Upstream repo | https://github.com/garrytan/gstack |
| Upstream version | 1.48.0.0 |
| Upstream commit | `a6fb31726cece1d1bba401fde593db7cb96bc738` |
| Synced at | 2026-05-27 |
| Local pack path | `.cursor/skills/gstack/` |
| Local skill count | 58 (`SKILL.md` files incl. pack meta) |

Machine-readable copies:

- `registry/gstack-sync.json` — full sync metadata and staleness policy
- `registry/manifest.json` — includes `gstack_version`, `gstack_commit`, `gstack_synced_at`

## Prior snapshot (pre-refresh)

| Field | Value |
|-------|-------|
| Commit | unknown (not tracked before this refresh) |
| Version | unknown |
| Skill count | 49 (+ nested layout, old frontmatter) |
| Notes | Single-line `description` frontmatter; missing ios/spec/document-generate/make-pdf skills |

## Local patches

None. The pack is imported as-is from upstream with path remapping only (flat upstream dirs → nested `gstack/<category>/`).

## What we did **not** reimplement

Registry v2, doctor/sync, eval-recommend, catalog, safe-install, resolver, and pack tooling in this repo already cover the infra layer. This refresh updates **pack content and version tracking** only.

## Check freshness

```bash
python3 scripts/skillhub.py doctor --gstack
python3 scripts/skillhub.py doctor --gstack-only
```

Doctor flags:

- Missing `registry/gstack-sync.json` or manifest gstack fields
- Skill count drift vs recorded count
- Sync older than 90 days (configurable in `gstack-sync.json`)

## Upgrade procedure

See [gstack-refresh.md](gstack-refresh.md).
