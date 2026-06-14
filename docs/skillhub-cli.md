# SkillHub CLI

Browse, recommend, and install skills from the awesome-agent-skill registry.

## Requirements

- Python 3.9+
- Run from a clone of this repo, or `pip install -e .` from repo root

## Quick commands

```bash
# Recommend skills for a task (structured output)
python3 scripts/skillhub.py recommend "debug flaky CI tests"
python3 scripts/skillhub.py recommend "ship a PR safely" --format cursor --json

# After pip install -e .
skillhub recommend "review this architecture" --json

# Install with safety flags
python3 scripts/skillhub.py install-bundle ship-ready ~/my-app --format cursor --dry-run
python3 scripts/skillhub.py install-bundle starter ~/my-app --backup --no-overwrite

# Health
python3 scripts/skillhub.py doctor
python3 scripts/skillhub.py doctor --target ~/my-app
python3 scripts/skillhub.py eval-recommend
python3 scripts/skillhub.py sync
```

## `recommend` output

Human mode prints:

- Suggested **bundle** (if match)
- **Install command** (`install-bundle` or top skills)
- **Full workflow** (clone + install) when useful
- Top skills with **match reasons**
- **Reload note** for Cursor / Claude

`--json` returns the same structure for tooling and the marketplace advisor.

## Packaging

```bash
pip install -e .          # exposes `skillhub` on PATH
uvx --from . skillhub list
python3 scripts/pack-skills.py   # dist/skillpack.tar + sha256
```

Set `SKILLHUB_ROOT` if the CLI package is installed but skills live in another clone path.

## All commands

```bash
python3 scripts/skillhub.py list [--domain DOMAIN]
python3 scripts/skillhub.py search "query" [-n LIMIT] [-v]
python3 scripts/skillhub.py show SKILL_ID
python3 scripts/skillhub.py bundles [-v]
python3 scripts/skillhub.py install SKILL_ID TARGET [--format cursor|claude|both] [--dry-run] [--backup] [--no-overwrite]
python3 scripts/skillhub.py install-bundle BUNDLE TARGET [flags...]
python3 scripts/skillhub.py quality [--regenerate] [--low-only]
python3 scripts/skillhub.py validate
python3 scripts/skillhub.py pack
python3 scripts/skillhub.py resolver-generate
```

See `registry/README.md` for bundle definitions.
