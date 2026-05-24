# awesome-agent-skill

Curated skill pack for LLM agents in data science and machine learning, ready for Cursor and Claude.

This repository collects reusable agent workflows for EDA, statistics, visualization, ML/DL, reporting, QA, security, reliability, and agent orchestration. Each skill is packaged as a `SKILL.md` so your coding agent can load domain-specific playbooks instead of starting from a blank prompt.

## What you get

- **Agent-ready skills** organized by domain (stats, viz, ML, docs, QA, security, reliability, workflows).
- **Cursor & Claude support** via `.cursor/skills/**` and generated `.claude/skills/**`.
- **Batteries-included workflows** instead of one-off prompts.

## Quickstart (project-local)

Clone this repo next to your project and copy the skills you want:

```bash
git clone https://github.com/charlieviettq/awesome-agent-skill.git

# Example: copy analysis & visualization skills into your project
rsync -a awesome-agent-skill/.cursor/skills/analysis-stats/  .cursor/skills/analysis-stats/
rsync -a awesome-agent-skill/.cursor/skills/visualization/   .cursor/skills/visualization/
```

Reload Cursor/Claude in your project so the agent can see the new skills.

## Skill layout

All Cursor-format skills live under `.cursor/skills/`:

- `analysis-stats/` — SHAP, statistical tests, statsmodels, and related analysis helpers.
- `data-compute/` — dask, polars, networkx.
- `eda-research/` — exploratory data analysis helpers and hypothesis tooling.
- `frontend-engineering/` — UI accessibility and frontend-focused helpers.
- `ml-dl/` — scikit-learn, PyTorch Lightning, transformers.
- `performance/` — performance measurement and optimization patterns.
- `product-growth/` — experiment design and product analytics.
- `reliability-ops/` — CI quality gates, SLO/observability, launch checklists, postmortems.
- `security-appsec/` — secure API design, API security testing, skill supply-chain audit.
- `visualization/` — matplotlib, seaborn, scientific-visualization, infographics, chart selection.
- `writing-docs/` — docx/pdf/pptx/xlsx, scientific writing, prose polish.
- `core-workflow/` — planning, task breakdown, TDD, spec-driven development, code review, etc.
- `gstack/` — browser QA, deployment, ship workflows for web apps.
- `voltagent/` — role-based DS/ML/product subagents (converted from VoltAgent).
- `meta-tools/` — higher-level tooling like autoskill.

Generated Claude-format skills live under `.claude/skills/` and are produced by:

```bash
python3 scripts/convert-to-claude.py --in-repo --force
```

## Using with Cursor

1. Ensure this repo is cloned somewhere accessible.
2. Copy or sync the desired skill folders into your project’s `.cursor/skills/`.
3. Reload Cursor (\"Reload Window\") so the agent picks up the new skills.

Skills are automatically discovered by Cursor under `.cursor/skills/**` and can be triggered based on their descriptions and triggers.

## Using with Claude Code

If your project uses `.claude/skills/`, either:

- Generate `.claude/skills/` in your project with `convert-to-claude.py`, or
- Copy from this repo’s `.claude/skills/**` into your project.

Restart your Claude Code session to load the new skills.

## Contributing

Contributions are welcome. Good contributions include:

- New skills that follow the existing structure (`SKILL.md` + optional references/examples).
- Improvements to existing skills (better triggers, clearer descriptions, safer defaults).
- CI improvements and docs that make these skills easier to adopt.

Please open an issue or PR with a short description, and keep skills generic and safe for public use (no secrets, internal-only details, or partner data).

## License

MIT license (proposed) — pick a permissive license so teams can adopt these skills in their own agents.

