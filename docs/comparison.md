# How This Differs From a Typical Awesome List

Most **awesome-*** repos are curated link lists or markdown indexes. **awesome-agent-skill** is built as a **skill marketplace + installer** for AI coding agents.

| Capability | Typical awesome list | awesome-agent-skill |
|------------|---------------------|---------------------|
| Primary artifact | Links / README tables | Portable `SKILL.md` folders + registry |
| Discovery | Scroll README | [Skill Marketplace](https://charlieviettq.github.io/awesome-agent-skill/) with search, filters, task advisor |
| Task → skills | Manual reading | `skillhub recommend "debug flaky CI"` with bundle + install command |
| Install | Copy-paste paths | `install-bundle.sh`, `skillhub install-bundle`, dry-run / backup flags |
| Metadata | Title + URL | Domain, tier, risk, triggers, quality score, agent format |
| Bundles | None | `starter`, `ship-ready`, `agent-builder`, `data-scientist`, `security-reviewer` |
| Quality gate | Optional | `registry/quality.json`, `validate-skills.py`, CI lint |
| Release | Tags only | Deterministic `skillpack.tar` + SHA256 checksum |
| Resolver | N/A | Compact resolver markdown for agent context budgets |

## When to use this repo

- You want **ready-to-install agent playbooks** (planning, QA, security, MCP, data/docs), not just links.
- You need **Cursor + Claude Code** paths from one source tree.
- You want a **registry** that powers CLI, catalog UI, and recommendation evals from the same data.

## When a plain awesome list is enough

- You only need outbound links to external tools.
- Skills are hosted elsewhere and you do not install locally.

## Related projects

- [Cursor skills docs](https://cursor.com/docs) — client-specific discovery
- [Claude Code skills](https://docs.anthropic.com/en/docs/claude-code) — `.claude/skills/` layout
- Generic awesome lists — great for breadth; this repo optimizes for **install + recommend + trust**
