<div align="center">

<img src=".github/assets/readme-hero.svg" alt="awesome-agent-skill — reusable skills for agentic developer tools" width="100%" />

<br />

[![Stars](https://img.shields.io/github/stars/charlieviettq/awesome-agent-skill?style=for-the-badge&logo=github&color=60a5fa)](https://github.com/charlieviettq/awesome-agent-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/license-MIT-22c55e?style=for-the-badge)](LICENSE)
[![Skills](https://img.shields.io/badge/skills-170-8b5cf6?style=for-the-badge)](.cursor/skills)
[![Formats](https://img.shields.io/badge/formats-Cursor%20%2B%20Claude-0ea5e9?style=for-the-badge)](#quickstart)
[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![Last commit](https://img.shields.io/github/last-commit/charlieviettq/awesome-agent-skill?style=for-the-badge&color=f97316)](https://github.com/charlieviettq/awesome-agent-skill/commits/main)
[![Contributors](https://img.shields.io/github/contributors/charlieviettq/awesome-agent-skill?style=for-the-badge&color=a855f7)](https://github.com/charlieviettq/awesome-agent-skill/graphs/contributors)

**A curated, open-source skill library for agentic developer tools.**

Give your coding agent reusable playbooks for planning, debugging, QA, security, docs, data work, browser automation, and shipping.

</div>

---

## Why This Exists

Most agents start every task from a blank prompt. Skills give them reusable operating procedures: when to ask for clarification, how to run a review, how to triage tests, how to handle PDFs, how to build a quick analysis, how to use browser QA, and how to ship safely.

`awesome-agent-skill` packages those workflows as portable `SKILL.md` files for modern coding agents.

## What You Get

| Area | Includes |
|------|----------|
| Agent workflow | Specs, planning, TDD, incremental implementation, code review, verification |
| Agent systems | MCP, RAG, tool contracts, context-window management, agent evaluation |
| Browser QA | gstack-style browsing, QA, canary checks, benchmarks, screenshots |
| Reliability and security | CI gates, launch checklists, observability, API security, skill supply-chain audit |
| Data and content | Analysis, visualization, documents, spreadsheets, PDFs, presentations |
| Role playbooks | Engineering, research, product, operations, orchestration, language experts |

## Works With

Portable `SKILL.md` folders for agentic coding tools:

| Tool | Install path | Notes |
|------|--------------|-------|
| [Cursor](https://cursor.com) | `.cursor/skills/` | Source of truth in this repo |
| [Claude Code](https://docs.anthropic.com/en/docs/claude-code) | `.claude/skills/` | Generated from Cursor skills |
| [Codex CLI](https://github.com/openai/codex) | `.claude/skills/` or project skills dir | Copy compatible skill folders |
| [OpenCode](https://github.com/opencode-ai/opencode) | `.opencode/skills/` or `.cursor/skills/` | Follow your client’s skill discovery path |
| Gemini CLI / other agents | Project skills directory | Same `SKILL.md` format; verify client docs |

Copy only the domains you need. Reload the agent session after installing skills.

## Quickstart

Clone the pack:

```bash
git clone https://github.com/charlieviettq/awesome-agent-skill.git
cd awesome-agent-skill
```

Install a few Cursor skills into a project:

```bash
mkdir -p /path/to/project/.cursor/skills
rsync -a .cursor/skills/core-workflow/ /path/to/project/.cursor/skills/core-workflow/
rsync -a .cursor/skills/security-appsec/ /path/to/project/.cursor/skills/security-appsec/
rsync -a .cursor/skills/writing-docs/ /path/to/project/.cursor/skills/writing-docs/
```

Install Claude Code skills:

```bash
mkdir -p /path/to/project/.claude/skills
rsync -a .claude/skills/ /path/to/project/.claude/skills/
```

Reload your agent session after copying skills.

## Formats

| Agent surface | Path | Status |
|---------------|------|--------|
| Cursor | `.cursor/skills/**/SKILL.md` | Source of truth |
| Claude Code | `.claude/skills/**/SKILL.md` | Generated and committed |

Regenerate Claude-format skills after editing Cursor-format skills:

```bash
python3 scripts/convert-to-claude.py --in-repo --force --write-map
```

## Skill Map

<img src=".github/assets/skill-map.svg" alt="Skill map for awesome-agent-skill" width="100%" />

Full index: [`SKILL_INVENTORY.md`](SKILL_INVENTORY.md)

## Repository Layout

```text
.
├── .cursor/skills/      # Cursor skill format, source of truth
├── .claude/skills/      # Claude Code skill format, generated from Cursor skills
├── scripts/             # Conversion and maintenance scripts
├── .github/workflows/   # Lightweight validation
└── SKILL_INVENTORY.md   # Human-readable skill index
```

## Highlights

| Folder | Good For |
|--------|----------|
| `core-workflow/` | Spec-first implementation, planning, TDD, verification, reviews |
| `ai-agent-systems/` | MCP servers, RAG systems, agent evals, tool schemas |
| `gstack/` | Browser QA, ship workflows, design review, scrape flows |
| `voltagent/` | Role-based subagent playbooks |
| `security-appsec/` | API security, secure design, skill supply-chain checks |
| `reliability-ops/` | CI gates, SLOs, launch readiness, postmortems |
| `writing-docs/` | PDF, DOCX, XLSX, PPTX, prose polish |
| `visualization/` | Charts, figures, infographics, data storytelling |

## Design Principles

- **Portable:** skills are plain folders with `SKILL.md`.
- **Composable:** copy one domain or the full pack.
- **Public-safe:** no secrets, customer data, or private org assumptions.
- **Agent-first:** written as workflows an agent can follow, not as static articles.
- **Reviewable:** skills stay small; long references belong in `reference.md` or examples.

## Updating Skills

Edit the Cursor source:

```bash
$EDITOR .cursor/skills/core-workflow/spec-driven-development/SKILL.md
```

Regenerate Claude output:

```bash
python3 scripts/convert-to-claude.py --in-repo --force --write-map
```

Run the lightweight check:

```bash
python3 - <<'PY'
from pathlib import Path
skill_files = list(Path(".cursor/skills").rglob("SKILL.md")) + list(Path(".claude/skills").rglob("SKILL.md"))
if not skill_files:
    raise SystemExit("No skills found")
bad = [path for path in skill_files if not path.read_text(encoding="utf-8").startswith("---")]
if bad:
    raise SystemExit("\\n".join(map(str, bad)))
print(f"Validated {len(skill_files)} skill files")
PY
```

## Private Skills

Keep team-specific or sensitive skills in your own repository under paths such as `.cursor/skills/private/` and `.claude/skills/private/`. This public pack is intentionally generic.

## Contributing

Contributions welcome. See [`.github/CONTRIBUTING.md`](.github/CONTRIBUTING.md) for the skill template, PR checklist, and validation steps.

- Propose a skill: [New skill issue](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=new-skill.yml)
- Report outdated content: [Outdated skill issue](https://github.com/charlieviettq/awesome-agent-skill/issues/new?template=outdated-skill.yml)

Recent changes: [`CHANGELOG.md`](CHANGELOG.md)

## Submit to Awesome Lists

If you maintain an awesome-list or agent-tools roundup, consider linking this repo under categories such as **AI agents**, **Cursor**, **Claude Code**, **MCP**, or **developer tools**. Suggested blurb:

> **awesome-agent-skill** — 170+ portable agent skills (planning, QA, security, MCP, browser automation, data/docs) for Cursor and Claude Code.

External catalogs we track: [`EXTERNAL_SKILLS.md`](EXTERNAL_SKILLS.md)

## License

MIT. See [LICENSE](LICENSE). Use it, fork it, and adapt it for your own agents.

