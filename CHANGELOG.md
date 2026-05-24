# Changelog

All notable changes to this repository are documented here.

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
