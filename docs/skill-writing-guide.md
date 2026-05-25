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
description: One sentence summary. Triggers: "phrase one", "phrase two".
---
```

- `name` must match the folder name (kebab-case)
- Include `Triggers:` with quoted phrases for non-legacy domains

## Structure template

1. When to use
2. When not to use
3. Workflow (numbered)
4. Output / acceptance criteria
5. Related skills

## Examples

### Good

```markdown
## Workflow
1. Confirm target API surface and consumers
2. Draft request/response examples including errors
3. Run secure-api-design checklist for auth and validation
```

Clear, ordered, verifiable.

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

## Before opening a PR

- Read [`review-rubric.md`](review-rubric.md)
- Run `python3 scripts/validate-skills.py`
- If editing Cursor skills, regenerate Claude output
