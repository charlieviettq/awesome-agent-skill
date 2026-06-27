# External Skills Audit Log

Curated audit of third-party skill sources reviewed for integration into [awesome-agent-skill](https://github.com/charlieviettq/awesome-agent-skill). Use this file as the provenance ledger before importing or adapting external content.

**Last audit:** 2026-06-27

## Sources reviewed

| Source | URL | License | Stars (audit date) | Verdict |
|--------|-----|---------|-------------------|---------|
| addyosmani/agent-skills | https://github.com/addyosmani/agent-skills | MIT | ~45k | Adapt selected skills with attribution |
| abcnuts/manus-skills | https://github.com/abcnuts/manus-skills | Unverified (README claims MIT; no LICENSE file in repo) | ~24 | Clean-room rewrite only; do not copy text/scripts |
| obra/superpowers | https://github.com/obra/superpowers | MIT | ~206k | Cherry-pick workflows; no plugin/runtime vendoring |
| anthropics/knowledge-work-plugins | https://github.com/anthropics/knowledge-work-plugins | MIT | ~18k | **Adapt all 11 plugins** (~80 skills) into `knowledge-work/` domain |
| Leonxlnx/taste-skill | https://github.com/Leonxlnx/taste-skill | MIT | Unchecked | Import all `skills/` entries plus referenced skill-local files into `frontend-engineering/taste/` |
| charlieviettq/ppt-master | https://github.com/charlieviettq/ppt-master | MIT | Unchecked | Import full `skills/ppt-master` runtime package into `writing-docs/ppt-master` |

## Decision key

| Outcome | Meaning |
|---------|---------|
| **Adapt** | MIT or equivalent; rewrite to repo style; note source here |
| **Rewrite** | Useful ideas but license unclear or content too platform-specific; original wording only |
| **Merge** | Concepts folded into an existing skill instead of a new folder |
| **Hold** | Worth a future checklist skill; not imported in this pass |
| **Reject** | Duplicate, risky, or too thin to ship |

---

## addyosmani/agent-skills

### Adapted (Priority 1)

| External skill | Local skill | Overlap | Risk | Notes |
|----------------|-------------|---------|------|-------|
| interview-me | `core-workflow/interview-me` | Low vs `clarify-underspecified` | Low | One-question intent extraction before spec |
| idea-refine | `core-workflow/idea-refine` | Low | Low | Divergent/convergent idea shaping |
| api-and-interface-design | `core-workflow/api-and-interface-design` | Partial vs `secure-api-design`, `agent-tool-contracts` | Low | Contract-first API/module design |
| code-simplification | `core-workflow/code-simplification` | Partial vs `design-smell-review` | Low | Behavior-preserving simplify pass |
| frontend-ui-engineering | `frontend-engineering/frontend-ui-engineering` | Partial vs `frontend-ui-accessibility` | Low | Full UI engineering beyond a11y |
| browser-testing-with-devtools | `frontend-engineering/browser-testing-with-devtools` | Partial vs `gstack/browser-qa` | Medium | DevTools MCP + untrusted browser boundary |
| context-engineering | (concepts) | Partial vs `context-window-management` | Low | Session setup patterns; not duplicated as skill |

### Documented only (not imported as skills)

| Artifact | Decision | Reason |
|----------|----------|--------|
| `using-agent-skills` meta-skill | Merge concepts | Covered by repo README + skill discovery |
| `agents/code-reviewer`, `security-auditor`, `test-engineer` | Hold | Overlap with gstack/voltagent personas |
| `/ship`, `/spec`, slash commands | Hold | Repo focuses on skills, not command packs |
| `references/orchestration-patterns.md` | Document | Fan-out vs sequential orchestration guidance captured here |

### Overlap — no import

| External skill | Existing local skill |
|----------------|-------------------|
| spec-driven-development | `core-workflow/spec-driven-development` |
| planning-and-task-breakdown | `core-workflow/planning-and-task-breakdown` |
| incremental-implementation | `core-workflow/incremental-implementation` |
| test-driven-development | `core-workflow/test-first-development` |
| source-driven-development | `core-workflow/source-driven-development` |
| doubt-driven-development | `core-workflow/doubt-driven-review` |
| debugging-and-error-recovery | `gstack/code-quality/investigate` |
| code-review-and-quality | `gstack/code-quality/review` |
| security-and-hardening | `security-appsec/*` |
| performance-optimization | `performance/performance-optimization` |
| ci-cd-and-automation | `reliability-ops/ci-cd-quality-gates` |
| deprecation-and-migration | `core-workflow/deprecation-and-migration` |
| documentation-and-adrs | `core-workflow/architecture-decision-records` |
| shipping-and-launch | `reliability-ops/shipping-launch-checklist` |
| git-workflow-and-versioning | `gstack/deploy-ship/ship` patterns |

**Attribution:** Adapted skills follow workflows inspired by [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT). Wording rewritten for this catalog.

---

## abcnuts/manus-skills

### Rewritten (Priority 1)

| External skill | Local skill | Risk | Notes |
|----------------|-------------|------|-------|
| app-store-submission-packager | `mobile/app-store-submission-packager` | Low | Checklist-only; no store credentials in repo |
| ios-testflight-github-actions | `mobile/ios-testflight-github-actions` | Medium | Requires GitHub secrets; no auto-push |
| meta-ads-analyzer | `marketing/meta-ads-analyzer` | Medium | Analytics workflow; not financial advice |
| serverless-debugging | `reliability-ops/serverless-debugging` | Low | Edge/Lambda/Workers debugging |
| dynamic-config-management (workflow) | `reliability-ops/dynamic-config-management` | Low | Config validation, no secrets |
| cross-platform-error-handling (workflow) | `reliability-ops/cross-platform-error-handling` | Low | RN/mobile/web error UX patterns |

### Rewritten (Priority 2)

| External skill | Local skill | Risk | Notes |
|----------------|-------------|------|-------|
| mcp-ecosystem-optimizer | `ai-agent-systems/mcp-ecosystem-optimizer` | Medium | No Manus CLI; registry/inventory only |
| digital-product-inventor | `product-growth/product-offer-design` | Low | Neutral product packaging; no pricing dogma |
| work-access-demo-generator | `core-workflow/work-access-handoff` | Low | Generic Git/cloud handoff guide |
| system-mapper | `architecture/system-mapping` | Low | Causal/system diagram workflow |

### Hold

| External skill | Reason |
|----------------|--------|
| payment-integration | Thin script wrapper; needs secure Stripe checklist pass |
| file-upload-system | Thin; needs presigned URL security review |
| search-implementation | Thin template |
| notification-system | Thin template |
| cron-job-scheduler | Thin template |
| autonomous-github-sync | High risk: Drive intermediary, auto-push |
| autonomous-sync-script | High risk: auto commit/push |
| manus-mcp-configurator | Platform-specific |
| similarweb-analytics, stock-analysis | External API dependency |
| video-generator, music-video-production | Niche creative; low agent-workflow fit |

### Reject

| External skill | Reason |
|----------------|--------|
| docx, pdf, pptx, xlsx (utility) | Already in `writing-docs/*` |
| mcp-builder (duplicate) | Already in `ai-agent-systems/mcp-builder` |
| brainstorming, writing-plans, TDD (workflow) | Overlap with Addy/local core-workflow |
| internet-skill-finder | Overlap with `skill-supply-chain-audit` |

**Attribution:** abcnuts skills used as **inspiration only**. Local files are clean-room rewrites. Do not copy scripts from that repo until license is verified.

---

## obra/superpowers

**Audit date:** 2026-05-25. Upstream is a methodology + multi-harness plugin pack ([superpowers](https://github.com/obra/superpowers)). We adapt **workflow content only** into `.cursor/skills/`; we do **not** vendor `skills/` tree, hooks, `.claude-plugin`, `.cursor-plugin`, OpenCode bootstrap, or local visual server scripts.

### Merged into existing skills

| External skill | Local skill | Risk | Notes |
|----------------|-------------|------|-------|
| brainstorming | `core-workflow/idea-refine`, `interview-me`, `spec-driven-development` | Low | One-question cadence, 2–3 options, chunked design approval; no auto-commit |
| writing-plans | `core-workflow/planning-and-task-breakdown` | Low | Small tasks, exact files, verify commands, no placeholders |
| executing-plans | `core-workflow/incremental-implementation` | Low | Plan review before execute, stop-on-blocker; no auto-finish branch |
| test-driven-development | `core-workflow/test-first-development` | Low | RED-GREEN-REFACTOR + anti-patterns; relax for docs/config/prototypes |
| verification-before-completion | `core-workflow/verify-before-done` | Low | Evidence + requirements checklist |
| receiving-code-review | `core-workflow/receiving-code-review` | Low | Verify claims, clarify vague feedback, evidence-based pushback |
| using-git-worktrees | (notes only) | Medium | Hygiene notes in `incremental-implementation`; no auto worktree/create/cleanup |
| finishing-a-development-branch | (notes only) | Medium | Land/merge via PR + `verify-before-done`; no discard-branch workflow |

### New skills (adapted)

| External skill | Local skill | Risk | Notes |
|----------------|-------------|------|-------|
| systematic-debugging | `core-workflow/systematic-debugging` | Low | Four-phase root cause; no `find-polluter.sh` import |
| requesting-code-review | `core-workflow/requesting-code-review` | Low | Thin review request; optional subagent only when allowed |
| dispatching-parallel-agents | `ai-agent-systems/dispatching-parallel-agents` | Medium | Gated parallel tasks; integration review required |
| subagent-driven-development | `ai-agent-systems/subagent-driven-development` | Medium | Gated; one task per agent; no auto-commit |
| writing-skills | `meta-tools/writing-skills` | Low | Thin skill + `docs/skill-writing-guide.md`; no `render-graphs.js` |

### Skip (this pass)

| External skill | Reason |
|----------------|--------|
| using-superpowers | Meta-bootstrap forcing skill use before every response; conflicts with agent protocol |
| using-git-worktrees (standalone) | Auto worktree, `.gitignore` edits, install deps, destructive cleanup |
| finishing-a-development-branch (standalone) | Discard/merge/cleanup branch flows conflict with Git safety and explicit PR rules |

### Not copied from upstream

- Plugin manifests (`.claude-plugin`, `.cursor-plugin`, `.codex-plugin`, `gemini-extension.json`)
- OpenCode `superpowers.js` bootstrap injection
- `scripts/sync-to-codex-plugin.sh`, hooks, local HTTP visual companion
- `find-polluter.sh`, `render-graphs.js`

**Attribution:** Workflows inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT, Jesse Vincent). Wording rewritten for this catalog.

---

## anthropics/knowledge-work-plugins

**Audit date:** 2026-05-30. Official Anthropic knowledge-worker plugin pack for Claude Cowork/Code. Each plugin ships `.claude-plugin/plugin.json`, optional `.mcp.json` (Snowflake, BigQuery, Linear, etc.), and passive `skills/SKILL.md` files with `argument-hint` in frontmatter.

### Verdict: Adapt all 11 plugins

| Plugin | Skills (upstream) | Local path | MCP hints (reference) |
|--------|-------------------|------------|------------------------|
| data | 10 | `knowledge-work/data/` | snowflake, bigquery, databricks, hex, amplitude |
| engineering | 10 | `knowledge-work/engineering/` | github, linear, datadog |
| product-management | 8 | `knowledge-work/product-management/` | linear, notion |
| productivity | 5 | `knowledge-work/productivity/` | — |
| marketing | 8 | `knowledge-work/marketing/` | — |
| sales | 9 | `knowledge-work/sales/` | salesforce, hubspot |
| finance | 8 | `knowledge-work/finance/` | — |
| legal | 9 | `knowledge-work/legal/` | — |
| customer-support | 5 | `knowledge-work/customer-support/` | zendesk, intercom |
| bio-research | 6 | `knowledge-work/bio-research/` | — |
| cowork-plugin-management | 2 | `knowledge-work/cowork-plugin-management/` | — |

**Import method:** `scripts/import-plugins.py` fetches `SKILL.md` via GitHub API, adds Cursor frontmatter (`version`, `triggers`, `source`), preserves `argument-hint`. Does **not** vendor `.claude-plugin` or live `.mcp.json` credentials — MCP templates live in `mcp-templates/` as optional stubs.

### Not copied verbatim

- Plugin runtime / Cowork installer UI
- User-specific MCP OAuth tokens
- Slash `commands/` trees (passive skills only in this pass)

### Overlap notes

| Upstream skill | Local overlap | Action |
|----------------|---------------|--------|
| statistical-analysis (data) | `analysis-stats/statistical-analysis` | Both kept; kw variant is data-warehouse workflow |
| code-review (engineering) | `gstack/code-quality/review`, voltagent | Both kept; kw variant is standup/tracker oriented |

**Attribution:** Skills adapted from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (MIT). Frontmatter extended for this catalog; body text retained unless path-specific edits required.

---

## Leonxlnx/taste-skill

**Audit date:** 2026-06-27. Upstream commit `06d6028b5c623016c59ce8536f578e5a1127b499`. Taste Skill is a Claude/agent skill pack for frontend design taste, redesign, image-to-code, and image-generation prompt direction.

### Imported

| External skill | Local skill | Risk | Notes |
|----------------|-------------|------|-------|
| brandkit | `frontend-engineering/taste/brandkit` | Low | Image prompt direction for brand-kit boards |
| brutalist-skill | `frontend-engineering/taste/industrial-brutalist-ui` | Medium | Strong frontend aesthetic rules |
| gpt-tasteskill | `frontend-engineering/taste/gpt-taste` | Medium | Code-writing frontend direction |
| image-to-code-skill | `frontend-engineering/taste/image-to-code` | Medium | Image-first website implementation workflow |
| imagegen-frontend-mobile | `frontend-engineering/taste/imagegen-frontend-mobile` | Low | Image prompt direction only |
| imagegen-frontend-web | `frontend-engineering/taste/imagegen-frontend-web` | Low | Image prompt direction only |
| minimalist-skill | `frontend-engineering/taste/minimalist-ui` | Medium | Frontend aesthetic rules |
| output-skill | `frontend-engineering/taste/full-output-enforcement` | Medium | Output completeness enforcement |
| redesign-skill | `frontend-engineering/taste/redesign-existing-projects` | Medium | Existing UI redesign workflow |
| soft-skill | `frontend-engineering/taste/high-end-visual-design` | Medium | Frontend aesthetic rules |
| stitch-skill | `frontend-engineering/taste/stitch-design-taste` | Medium | Includes referenced `DESIGN.md` |
| taste-skill-v1 | `frontend-engineering/taste/design-taste-frontend-v1` | Medium | Preserved v1 behavior |
| taste-skill | `frontend-engineering/taste/design-taste-frontend` | Medium | Current v2 experimental default |

### Not copied from upstream

- `.claude-plugin/` manifests
- README marketing/sponsor assets
- Research notes and examples
- Asset-processing scripts
- Repo-level `llms.txt`

**Attribution:** Skills imported from [Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill) (MIT, Leonxlnx). Body text preserved; frontmatter extended for this catalog with provenance, license, trigger hints, and Claude tool metadata where needed.

---

## charlieviettq/ppt-master

**Audit date:** 2026-06-27. Upstream commit `13a25616e6354fe5abe16f41da18f532e51ac644`. PPT Master is an AI-driven document-to-editable-PPTX skill package with SVG generation, template libraries, image workflows, narration tooling, and PPTX export scripts.

### Imported

| External package | Local skill | Risk | Notes |
|------------------|-------------|------|-------|
| `skills/ppt-master` | `writing-docs/ppt-master` | High | Full runtime package: `SKILL.md`, references, scripts, templates, workflows, `.env.example`, requirements, and embedded assets |

### Runtime files copied

- `references/` including markdown references and image comparison assets
- `scripts/` including Python conversion, SVG, PPTX, image, narration, preview, and quality tooling
- `templates/` including brand, layout, chart, icon, and deck template libraries
- `workflows/` standalone PPT Master workflows
- Upstream root docs referenced by skill-local markdown links, vendored under `references/upstream-docs/`

### Not copied from upstream

- Root `.claude-plugin/` and marketplace metadata
- Root README/site assets and Pages files
- Root examples, exported PPTX decks, screenshots, and generated project outputs
- Repository-level docs that are not referenced by the imported skill runtime

**Attribution:** Skill runtime imported from [charlieviettq/ppt-master](https://github.com/charlieviettq/ppt-master), originally by Hugo He, MIT. Body text and runtime assets preserved; frontmatter and local doc links adapted for this catalog.

---

## Supply-chain checklist (before future imports)

1. Confirm license file exists and matches README claim.
2. Run `skill-supply-chain-audit` on any new external pack.
3. Search for: `curl | bash`, auto-push, credential exfil, broad triggers.
4. Prefer adapt/rewrite over vendoring whole trees.
5. Update this file and `SKILL_INVENTORY.md` in the same PR.

## Orchestration notes (from addyosmani)

- **Direct invocation:** one persona/skill, one artifact.
- **Parallel fan-out:** independent reviews (code + security + tests) then merge in main context.
- **Sequential lifecycle:** user-driven `/spec` → plan → build → test → review → ship.
- **Anti-pattern:** meta-orchestrator personas that only route to other personas.

See upstream [orchestration-patterns.md](https://github.com/addyosmani/agent-skills/blob/main/references/orchestration-patterns.md) for full catalog.
