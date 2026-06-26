# Changelog

All notable changes to this repository are documented here.

## [Unreleased]

### Added

- `marketing/linkedin-growth` - Import leads from LinkedIn or Sales Navigator searches, qualify them against an ideal-customer profile, schedule safe connection invites across accounts, track acceptances, and withdraw stale pending requests.
- `ai-agent-systems/xquik-x-data-workflows` - source-backed Xquik REST API and remote MCP workflow planning for X data tasks
- `scripts/skill_format.py` — shared frontmatter parsing, asset copy, trigger generation
- `scripts/convert-to-cursor.py` — sync Claude flat skills back to Cursor nested paths via `claude-skill-map.json` (preserves `triggers`, `source`, etc.)
- `scripts/prune_claude_skills.py` — remove orphan nested directories under `.claude/skills/`
- `scripts/audit-skill-parity.py` — report map vs on-disk Cursor/Claude gaps
- `convert-to-claude.py --prune-orphans` — optional prune after flat convert

### Changed

- `scripts/convert-to-claude.py`, `scripts/import-plugins.py` — use `skill_format` module
- `scripts/validate-skills.py` — `--parity` checks map coverage; CI runs with `--parity`
- README, CONTRIBUTING, `.claude/commands/sync-skills.md` — document bidirectional sync and dual layout

### Added (continued)

- **Knowledge Work plugins:** import ~79 skills from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) into `.cursor/skills/knowledge-work/` (11 plugin folders)
- `scripts/import-plugins.py` — fetch and adapt upstream `SKILL.md` (triggers, `argument-hint`, `source`)
- `scripts/generate-plugins.py` — publish `plugins/<bundle>/` with `.claude-plugin/plugin.json`, `.mcp.json.template`, `CONNECTORS.md`
- `mcp-templates/` — sanitized MCP stubs (data-warehouse, project-tracker, source-control, monitoring, comms)
- Registry bundles: 11 `knowledge-work-*` plugin bundles, `knowledge-work-all`, and persona bundles (`knowledge-worker`, `data-analyst-professional`, `sales-analyst`, `finance-analyst`, `legal-counsel`)
- `EXTERNAL_SKILLS.md` audit section for anthropics/knowledge-work-plugins

### Changed

- `scripts/convert-to-claude.py` — pass-through `argument-hint` in Claude frontmatter when present
- Persona bundles `data-scientist`, `marketing`, `ceo`, `software-engineer`, `data-engineer` — include selected knowledge-work skills
- Skill catalog graph (`catalog/`) regenerates with **258** skills and expanded bundle/persona nodes

### Added (continued)

- SkillHub web catalog: `scripts/generate-catalog.py`, static `catalog/index.html`
- SkillHub quality: `generate-quality.py`, `skillhub quality`, CI `eval-recommend`
- SkillHub recommend: `recommend`, `eval-recommend` with `registry/recommend-fixtures.json`
- SkillHub CLI: `scripts/skillhub.py` (`list`, `search`, `show`, `bundles`, `install`, `install-bundle`, `validate`, `doctor`)
- SkillHub registry: `registry/skills.json`, `registry/bundles.json`, `scripts/generate-registry.py`
- Bundle resolver: `scripts/resolve-bundle.py`; per-skill install: `scripts/install/install-skill.sh`
- Bundles: `ship-ready`, `agent-builder`, `data-scientist`, `security-reviewer` (plus existing `starter`, `full`)
- Install scripts: `scripts/install/install-domain.sh`, `scripts/install/install-bundle.sh`
- Validation script: `scripts/validate-skills.py` (used in CI)
- Metrics script: `scripts/repo-metrics.py`
- Optional commands: `.claude/commands/`, `.gemini/commands/`
- Contributor docs: `docs/skill-writing-guide.md`, `docs/review-rubric.md`, `docs/good-first-issues.md`
- Distribution tracker: `docs/distribution.md`
- Release cadence: `docs/RELEASE_CADENCE.md`
- Issue template: awesome-list submission tracking
- Superpowers-inspired skills: `systematic-debugging`, `requesting-code-review`, `dispatching-parallel-agents`, `subagent-driven-development`, `writing-skills`
- `EXTERNAL_SKILLS.md` audit section for [obra/superpowers](https://github.com/obra/superpowers)

### Changed

- CI lint workflow uses extended skill validation
- README: compatibility matrix, install scripts, optional commands
- Core workflow skills enriched from Superpowers: idea-refine, interview-me, spec-driven-development, planning-and-task-breakdown, incremental-implementation, test-first-development, verify-before-done, receiving-code-review
- `docs/skill-writing-guide.md`: pressure-test triggers and external adaptation notes

## [2.0.0] - 2026-05-24

### Added

- `EXTERNAL_SKILLS.md` — audit log and provenance for third-party skill sources
- 16 new skills from adapted and clean-room integrations:
  - Core: `interview-me`, `idea-refine`, `api-and-interface-design`, `code-simplification`, `work-access-handoff`
  - Frontend: `frontend-ui-engineering`, `browser-testing-with-devtools`
  - Mobile: `app-store-submission-packager`, `ios-testflight-github-actions`
  - Marketing: `meta-ads-analyzer`
  - Reliability: `serverless-debugging`, `dynamic-config-management`, `cross-platform-error-handling`
  - AI systems: `mcp-ecosystem-optimizer`
  - Product: `product-offer-design`
  - Architecture: `system-mapping`
- New domains: `mobile/`, `marketing/`, `architecture/`
- Context-engineering session setup merged into `context-window-management`

### Changed

- `SKILL_INVENTORY.md` and `.cursor/skills/README.md` updated for new domains
- Claude skill map regenerated (170 skills total)

## [1.0.0] - 2026-05-24

### Added

- Initial public release of `awesome-agent-skill`
- Cursor skill library (`.cursor/skills/`) as source of truth
- Claude Code skill format (`.claude/skills/`) with conversion script
- Domains: core-workflow, ai-agent-systems, gstack, voltagent, security-appsec, reliability-ops, data/ML, writing-docs, visualization
- CI workflow validating `SKILL.md` frontmatter
- README hero and skill-map assets
