# Skill Inventory (awesome-agent-skill)

High-level index of skill domains. For details, open each folder’s `SKILL.md`.

**Catalog size:** 259 skills (including ~79 from Anthropic knowledge-work-plugins).

## Knowledge Work (Anthropic plugins)

Imported domain: `knowledge-work/` — see hub `knowledge-work/SKILL.md`.

| Plugin folder | Skills |
|---------------|--------|
| `knowledge-work/data` | analyze, build-dashboard, create-viz, data-context-extractor, data-visualization, explore-data, sql-queries, statistical-analysis, validate-data, write-query |
| `knowledge-work/engineering` | architecture, code-review, debug, deploy-checklist, documentation, incident-response, standup, system-design, tech-debt, testing-strategy |
| `knowledge-work/product-management` | competitive-brief, metrics-review, product-brainstorming, roadmap-update, sprint-planning, stakeholder-update, synthesize-research, write-spec |
| `knowledge-work/productivity` | memory-management, start, task-management, update |
| `knowledge-work/marketing` | brand-review, campaign-plan, competitive-brief, content-creation, draft-content, email-sequence, performance-report, seo-audit |
| `knowledge-work/sales` | account-research, call-prep, call-summary, competitive-intelligence, create-an-asset, daily-briefing, draft-outreach, forecast, pipeline-review |
| `knowledge-work/finance` | audit-support, close-management, financial-statements, journal-entry, journal-entry-prep, reconciliation, sox-testing, variance-analysis |
| `knowledge-work/legal` | brief, compliance-check, legal-response, legal-risk-assessment, meeting-briefing, review-contract, signature-request, triage-nda, vendor-check |
| `knowledge-work/customer-support` | customer-escalation, customer-research, draft-response, kb-article, ticket-triage |
| `knowledge-work/bio-research` | instrument-data-to-allotrope, nextflow-development, scientific-problem-selection, scvi-tools, single-cell-rna-qc, start |
| `knowledge-work/cowork-plugin-management` | cowork-plugin-customizer, create-cowork-plugin |

**Bundles:** `knowledge-work-<plugin>`, `knowledge-work-all`, plus personas `knowledge-worker`, `data-analyst-professional`, `sales-analyst`, `finance-analyst`, `legal-counsel`. Graph UI updates via `scripts/generate-catalog.py`.

## Analysis & statistics

- `analysis-stats/shap`
- `analysis-stats/statistical-analysis`
- `analysis-stats/statsmodels`

## Data compute

- `data-compute/dask`
- `data-compute/networkx`
- `data-compute/polars`

## EDA & research

- `eda-research/exploratory-data-analysis`
- `eda-research/hypothesis-generation`
- `eda-research/umap-learn`

## ML & deep learning

- `ml-dl/pytorch-lightning`
- `ml-dl/scikit-learn`
- `ml-dl/scikit-survival`
- `ml-dl/transformers`

## Visualization

- `visualization/matplotlib`
- `visualization/seaborn`
- `visualization/scientific-visualization`
- `visualization/infographics`
- `visualization/data-viz-storytelling-healy`

## Writing & docs

- `writing-docs/docx`
- `writing-docs/pdf`
- `writing-docs/pptx`
- `writing-docs/xlsx`
- `writing-docs/prose-polish`
- `writing-docs/scientific-writing`
- `writing-docs/sympy`

## Core workflow

- `core-workflow/architecture-decision-records`
- `core-workflow/api-and-interface-design`
- `core-workflow/clarify-underspecified`
- `core-workflow/code-simplification`
- `core-workflow/deprecation-and-migration`
- `core-workflow/design-smell-review`
- `core-workflow/doubt-driven-review`
- `core-workflow/github-comment-triage`
- `core-workflow/idea-refine`
- `core-workflow/incremental-implementation`
- `core-workflow/interview-me`
- `core-workflow/planning-and-task-breakdown`
- `core-workflow/requesting-code-review`
- `core-workflow/receiving-code-review`
- `core-workflow/systematic-debugging`
- `core-workflow/source-driven-development`
- `core-workflow/spec-driven-development`
- `core-workflow/test-failure-triage`
- `core-workflow/test-first-development`
- `core-workflow/verify-before-done`
- `core-workflow/work-access-handoff`

## Frontend engineering

- `frontend-engineering/browser-testing-with-devtools`
- `frontend-engineering/frontend-ui-accessibility`
- `frontend-engineering/frontend-ui-engineering`

## Mobile

- `mobile/app-store-submission-packager`
- `mobile/ios-testflight-github-actions`

## Marketing

- `marketing/meta-ads-analyzer`

## Architecture

- `architecture/system-mapping`

## AI agent systems

- `ai-agent-systems/agent-evaluation`
- `ai-agent-systems/dispatching-parallel-agents`
- `ai-agent-systems/subagent-driven-development`
- `ai-agent-systems/agent-tool-contracts`
- `ai-agent-systems/context-window-management`
- `ai-agent-systems/mcp-builder`
- `ai-agent-systems/xquik-x-data-workflows`
- `ai-agent-systems/mcp-ecosystem-optimizer`
- `ai-agent-systems/rag-systems`

## Performance & reliability

- `performance/performance-optimization`
- `reliability-ops/ci-cd-quality-gates`
- `reliability-ops/cross-platform-error-handling`
- `reliability-ops/dynamic-config-management`
- `reliability-ops/observability-slo`
- `reliability-ops/postmortem-writing`
- `reliability-ops/serverless-debugging`
- `reliability-ops/shipping-launch-checklist`

## Security & appsec

- `security-appsec/api-security-testing`
- `security-appsec/secure-api-design`
- `security-appsec/skill-supply-chain-audit`

## Product & growth

- `product-growth/product-analytics-experiments`
- `product-growth/product-offer-design`

## Browser QA & ship (gstack)

- `gstack` (overview)
- `gstack/browser-qa/*`
- `gstack/code-quality/*`
- `gstack/deploy-ship/*`
- `gstack/design/*`
- `gstack/plan-review/*`
- `gstack/context-memory/*`
- `gstack/security-safety/*`
- `gstack/utility/*`

## Role-based subagents (voltagent)

See `voltagent/SKILL.md` and children under `voltagent/**` for DS/ML/product/infra personas converted from VoltAgent’s awesome-claude-code-subagents.

## Meta tools

- `meta-tools/autoskill`
- `meta-tools/writing-skills`
