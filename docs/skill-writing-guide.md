# Skill Writing Guide

Guidance for authoring skills that agents can discover and follow reliably.

## Good skill traits

- **Narrow scope:** one workflow, one decision boundary
- **Explicit triggers:** phrases users or agents actually say
- **Actionable steps:** numbered workflow, not essay prose
- **Verification:** how to know the task is done
- **Public-safe:** no secrets, private URLs, or org-only assumptions

## Frontmatter

```yaml
---
name: my-skill-name
version: 1
description: One sentence summary. Triggers: "phrase one", "phrase two".
argument-hint: "<optional parameter hint>"   # optional; Claude plugin style
triggers:
  - "phrase one"
  - "phrase two"
tools: []        # optional, list of MCP or CLI tools this skill calls
mutating: false  # does this skill write files / change external systems?
priority: normal # optional: normal | high | low
source: "anthropics/knowledge-work-plugins/data"  # optional provenance
---
```

- `name` must match the folder name (kebab-case)
- `version` should be bumped when behavior or contract changes
- `triggers` should be an explicit list of phrases users or agents actually say
- `argument-hint` is optional; preserved when converting to `.claude/skills/` (Anthropic plugin compatibility)
- `tools` and `mutating` help agent routers decide when extra care is needed
- `source` documents upstream pack when skills are adapted (see `EXTERNAL_SKILLS.md`)

## Structure template (Content Conformance V2)

Every non-legacy skill should follow this structure:

1. **Contract** — what this skill guarantees when it succeeds
2. **When To Use**
3. **When Not To Use**
4. **Phases** — high-level stages of the workflow
5. **Output Format** — shape of the final answer or artifact
6. **Anti-Patterns** — what the skill must explicitly avoid
7. **Related Skills** — pointers to adjacent skills or alternatives

At minimum, include the following headings:

```markdown
## Contract
## When To Use
## When Not To Use
## Phases
## Output Format
## Anti-Patterns
## Related Skills
```

## Examples

### Good (Content Conformance V2)

```markdown
## Contract
Help the user produce a concrete API design proposal that is safe, reviewable, and ready for implementation.

## When To Use
- New or significantly changed HTTP/JSON API
- Team needs alignment on request/response shapes and error handling

## When Not To Use
- Simple internal helper functions or private methods

## Phases
1. Clarify consumers and non-goals
2. Sketch endpoints, request/response, and errors
3. Run secure-api-design checklist
4. Produce review-ready proposal

## Output Format
- Markdown section with:
  - Table of endpoints
  - Detailed request/response examples
  - Auth and validation notes

## Anti-Patterns
- Do not invent undocumented auth schemes
- Do not approve designs without error handling

## Related Skills
- `secure-api-design`
- `deprecation-and-migration`
```

Clear contract, explicit phases, defined output, and concrete anti-patterns.

### Bad

```markdown
## Overview
APIs are important. Consider many factors when designing APIs including security,
performance, versioning, and team preferences. Think holistically.
```

Too vague; no triggers, no steps, no done condition.

## Legacy packs

Skills under `gstack/` and `voltagent/` are imported packs. New contributions should prefer top-level domains (`core-workflow/`, `reliability-ops/`, etc.) unless extending those packs intentionally.

## Pressure-test triggers

Before merging a new skill, write:

1. Three phrases that **should** invoke it
2. Two phrases that **should not** (too broad or wrong domain)
3. One edge case (e.g. user asks for speed over process)

If the skill would fire on almost every message, narrow the description or move content to a reference file.

## External adaptation

When adapting from catalogs such as [obra/superpowers](https://github.com/obra/superpowers):

- Record the decision in `EXTERNAL_SKILLS.md`
- Rewrite wording; do not copy plugin hooks or bootstrap meta-skills
- Prefer **merge** into an existing skill when overlap is high

## Skill vs code

- Deterministic operations (file layout, install plans, concrete commands) usually belong in **scripts/CLI**.
- Judgment calls, routing between workflows, and failure-mode handling belong in **skills**.
- When in doubt, keep the harness thin and the skill explicit about decisions and trade-offs.

## Before opening a PR

- Read [`review-rubric.md`](review-rubric.md)
- Run `python3 scripts/validate-skills.py`
- If editing Cursor skills, regenerate Claude output
