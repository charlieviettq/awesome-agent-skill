# SkillHub CLI

Local CLI for browsing and installing skills from this repository.

## Requirements

- Python 3.9+
- Run from repo root (or any cwd; paths resolve from `scripts/skillhub.py`)

## Commands

```bash
# List all skills (optional domain filter)
python3 scripts/skillhub.py list
python3 scripts/skillhub.py list --domain core-workflow

# Search by keyword (id, description, tags, triggers)
python3 scripts/skillhub.py search "code review"
python3 scripts/skillhub.py search mcp -n 5 -v

# Recommend skills for a natural-language task
python3 scripts/skillhub.py recommend "debug flaky CI tests"
python3 scripts/skillhub.py eval-recommend

# Show one skill as JSON
python3 scripts/skillhub.py show core-workflow/verify-before-done

# Bundles
python3 scripts/skillhub.py bundles -v

# Install
python3 scripts/skillhub.py install core-workflow/verify-before-done ~/my-app --format cursor
python3 scripts/skillhub.py install-bundle ship-ready ~/my-app --format both

# Health
python3 scripts/skillhub.py validate
python3 scripts/skillhub.py doctor
```

## Registry

Regenerate after skill changes:

```bash
python3 scripts/generate-registry.py
```

See `registry/README.md` for bundle definitions.
