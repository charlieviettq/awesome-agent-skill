# Release Cadence

## Target rhythm

- **Patch** (docs/fixes): anytime, tag optional
- **Minor** (new skills/domains): every **2–4 weeks**
- **Major** (breaking layout or format): rare, with migration notes

## Release checklist

1. Ensure `main` is green (CI lint passes)
2. Run `python3 scripts/validate-skills.py`
3. Update [`CHANGELOG.md`](../CHANGELOG.md) with version + date
4. Tag: `git tag vX.Y.Z && git push origin vX.Y.Z`
5. Create GitHub Release from tag (notes from CHANGELOG section)
6. Run `python3 scripts/repo-metrics.py` and commit metrics snapshot if material
7. Pin latest release on GitHub Releases page

## Release notes template

```markdown
## What's new
- bullet list of new skills or domains

## Changed
- updates to existing skills or docs

## Contributors
- thanks + links
```

## Versioning

Follow [Keep a Changelog](https://keepachangelog.com/) semantics:

- **Added** for new skills
- **Changed** for meaningful updates
- **Deprecated** when superseded
- **Removed** only with migration path

## GitHub Topics (maintainers)

Set under repo About:

`awesome-list, cursor, claude-code, ai-agents, llm, developer-tools, mcp, agent-skills, cursor-ai, copilot, opencode, codex`
