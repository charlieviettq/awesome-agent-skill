# Agent Skills

Skills live in subfolders with `SKILL.md` (and optional `reference.md` / `examples.md`). Cursor and Claude discover them recursively under `.cursor/skills/`.

## Layout

| Folder | Contents |
|--------|----------|
| `core-workflow/` | Spec/plan/incremental/source/doubt/deprecation + clarify, verify, TDD, ADR, PR review |
| `frontend-engineering/` | UI build + WCAG-oriented accessibility |
| `performance/` | Measure-identify-fix-verify-guard performance workflow |
| `security-appsec/` | Skill supply-chain audit, API security test/design |
| `ai-agent-systems/` | Agent eval, MCP builder, tool contracts, RAG, context budget |
| `reliability-ops/` | CI quality gates, launch checklist, observability/SLO, postmortems |
| `product-growth/` | Product analytics and A/B experiment gates |
| `ml-dl/` | scikit-learn, scikit-survival, transformers, PyTorch Lightning |
| `analysis-stats/` | SHAP, statsmodels, statistical analysis |
| `data-compute/` | Dask, Polars, NetworkX |
| `eda-research/` | EDA, hypothesis generation, UMAP |
| `visualization/` | matplotlib, seaborn, scientific-visualization, infographics, data-viz-storytelling |
| `writing-docs/` | PDF, DOCX, XLSX, PPTX, scientific writing, sympy |
| `meta-tools/` | Autoskill, reflect-yourself (self-learning system) |
| `gstack/` | Converted [gstack](https://github.com/garrytan/gstack) browser/QA/ship workflows |
| `voltagent/` | Converted [VoltAgent awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) role playbooks. See [`voltagent/SKILL.md`](voltagent/SKILL.md). |

## Discovery

- List all skills: `ls .cursor/skills/`
- Search triggers: `rg "^description:" .cursor/skills/**/SKILL.md`
- Browse by domain: see the table above or `../SKILL_INVENTORY.md`

## Adding private skills

You can place team-specific or private skills in `.cursor/skills/private/` (add `private/` to `.gitignore`). They will be discovered by Cursor but excluded from this public repository.

## Regenerating VoltAgent slice

```bash
python3 ../scripts/convert_voltagent_agents.py  # requires clone at /tmp/voltagent-skills
```

## External catalogs

See `../EXTERNAL_SKILLS.md` for curated third-party skills worth cherry-picking (review licenses before installing).
