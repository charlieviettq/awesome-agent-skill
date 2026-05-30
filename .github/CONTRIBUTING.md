# Contributing to awesome-agent-skill

Thank you for helping improve this skill library. This repo is optimized for **portable, public-safe agent workflows** that work in Cursor, Claude Code, and similar tools.

## Before you start

1. Search existing skills: `rg "Triggers:" .cursor/skills/**/SKILL.md` or read [`SKILL_INVENTORY.md`](../SKILL_INVENTORY.md).
2. Prefer extending an existing skill over duplicating one.
3. For third-party inspiration, read [`EXTERNAL_SKILLS.md`](../EXTERNAL_SKILLS.md) and follow license/provenance rules.

## Skill template

Create a folder under `.cursor/skills/<domain>/<skill-name>/SKILL.md`:

```markdown
---
name: your-skill-name
description: One sentence on what it does. Include precise triggers. Triggers: "keyword one", "keyword two".
---

# Your Skill Name

Short intro (1-2 sentences).

## When to use

- Bullet list

## When not to use

- Bullet list

## Workflow

1. Step one
2. Step two

## Output

What the agent should produce when done.

## Related skills

- `other-skill` — when to pair
```

Rules:

- `name` must match the folder name (kebab-case).
- `description` must include **Triggers:** with quoted phrases agents/users might say.
- Keep the body focused; move long references to `reference.md` in the same folder.
- No secrets, private URLs, customer data, or org-specific assumptions.

## PR checklist

Before opening a pull request:

- [ ] `name` in frontmatter matches folder name
- [ ] Description includes clear triggers
- [ ] Skill is public-safe (no credentials or internal-only naming)
- [ ] Ran Claude converter if you edited `.cursor/skills/`:
  ```bash
  python3 scripts/convert-to-claude.py --in-repo --force --write-map --prune-orphans
  ```
- [ ] If you edited only `.claude/skills/` (flat), sync back to Cursor then forward:
  ```bash
  python3 scripts/convert-to-cursor.py --in-repo --only-newer
  python3 scripts/convert-to-claude.py --in-repo --force --write-map --prune-orphans
  ```
- [ ] Ran validation:
  ```bash
  python3 scripts/validate-skills.py --parity
  ```
- [ ] Updated [`SKILL_INVENTORY.md`](../SKILL_INVENTORY.md) if adding a new top-level skill path
- [ ] Added a line to [`CHANGELOG.md`](../CHANGELOG.md) under `[Unreleased]` or the next version

## Domain placement

| Domain | Use for |
|--------|---------|
| `core-workflow/` | Spec, planning, reviews, implementation discipline |
| `ai-agent-systems/` | MCP, RAG, agents, context, tool contracts |
| `frontend-engineering/` | UI, a11y, browser DevTools |
| `reliability-ops/` | CI, launch, observability, serverless, config |
| `security-appsec/` | API security, supply-chain audit |
| `mobile/`, `marketing/`, `architecture/` | Domain-specific workflows |
| `gstack/`, `voltagent/` | Large converted packs; prefer new generic skills in top-level domains |

## GitHub Topics (maintainers)

Topics improve discovery in GitHub Search. Set on the repo **About** section (not in git):

```
awesome-list, cursor, claude-code, ai-agents, llm, developer-tools, mcp, agent-skills, cursor-ai, copilot, opencode, codex
```

## Issues

- **New skill:** use the [New skill proposal](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=new-skill.yml) template
- **Outdated skill:** use the [Outdated skill report](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=outdated-skill.yml) template
- **Awesome-list submission:** use the [Distribution tracker](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=awesome-list-submission.yml) template

## Further reading

- [`docs/skill-writing-guide.md`](../docs/skill-writing-guide.md)
- [`docs/review-rubric.md`](../docs/review-rubric.md)
- [`docs/good-first-issues.md`](../docs/good-first-issues.md)
- [`docs/RELEASE_CADENCE.md`](../docs/RELEASE_CADENCE.md)

## License

By contributing, you agree that your contributions are licensed under the [MIT License](../LICENSE).
