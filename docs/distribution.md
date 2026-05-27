# Distribution & Launch Checklist

Track submissions to awesome lists, releases, and social launch.

## Marketplace (primary demo)

- Public URL: enable **GitHub Pages** from `catalog/` (workflow: `.github/workflows/pages.yml`)
- Regenerate: `python3 scripts/generate-catalog.py`
- Share link in README, social posts, awesome-list submissions

## Install paths

| Path | Command |
|------|---------|
| Clone + script | `bash scripts/install/install-bundle.sh starter . --format cursor` |
| SkillHub CLI (dev) | `python3 scripts/skillhub.py install-bundle starter . --format cursor` |
| Editable package | `pip install -e .` then `skillhub install-bundle starter . --format cursor` |
| uvx (from clone) | `uvx --from . skillhub recommend "debug flaky CI"` |
| Release tarball | `python3 scripts/pack-skills.py` → `dist/skillpack.tar` + `.sha256` |

## Release checklist

- [ ] `python3 scripts/skillhub.py sync` (registry, quality, catalog, validate)
- [ ] `python3 scripts/skillhub.py eval-recommend` passes
- [ ] `python3 scripts/skillhub.py doctor` green
- [ ] `python3 scripts/pack-skills.py` → commit or attach `dist/skillpack.tar` to GitHub Release
- [ ] Tag version (e.g. `v0.2.0`) with release notes
- [ ] Regenerate catalog and verify Pages deploy

## GitHub repo settings

Topics (suggested):

`cursor`, `claude-code`, `ai-agents`, `agent-skills`, `mcp`, `developer-tools`, `skillhub`

Social preview: `.github/assets/social-preview.svg` (set as Open Graph image or use in README hero)

## Submission tracker

| List / channel | Category | Status | Link | Notes |
|----------------|----------|--------|------|-------|
| sindresorhus/awesome | TBD | Planned | https://github.com/sindresorhus/awesome | Use `docs/comparison.md` angle |
| Cursor community lists | cursor | Planned | | Marketplace + install scripts |
| Claude Code resources | claude-code | Planned | | Bundles + `.claude/skills/` sync |
| MCP awesome lists | mcp | Planned | | Highlight `mcp-builder` |
| Reddit / HN launch | social | Planned | | After Pages live + release tagged |

## Suggested blurb (short)

> **awesome-agent-skill** — 178+ portable agent skills with a searchable marketplace, task-to-skills advisor, quality-scored registry, and one-command bundle install for Cursor and Claude Code.

## Suggested blurb (HN / Reddit)

> I open-sourced a skill marketplace for AI coding agents: browse 178 playbooks on GitHub Pages, type what you want to do, get matching skills + an install command. Registry-driven CLI (`skillhub recommend`, bundle install, dry-run/backup). Not just an awesome list — installable skills with metadata (tier, risk, quality).

## Comparison page

See [comparison.md](./comparison.md) for positioning vs typical awesome lists.

## Contributor funnel

- `skillhub quality --low-only` surfaces skills needing cleanup
- Good first issues: thin descriptions, missing triggers, low quality score

Update the submission table when a channel is contacted or accepted.
