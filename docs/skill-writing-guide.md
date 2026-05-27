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

## Advanced patterns (from gstack pack)

Repo-native skills may adopt these patterns where they add clarity. Imported `gstack/` skills already use them; do not rewrite the pack to match this guide.

### YAML trigger lists

Prefer structured triggers when a skill has more than two phrases:

```yaml
---
name: my-skill
description: Short summary for routing. Triggers: "fallback phrase".
triggers:
  - run the checklist
  - pre-merge review
---
```

`generate-registry.py` indexes YAML `triggers:` as well as `Triggers:` in the description.

### Preamble tier and version

Optional metadata for large bootstrap skills:

```yaml
preamble-tier: 3   # 1=minimal, 4=full bootstrap (routing injection, upgrade checks)
version: 1.0.0
```

Use higher tiers only when the skill must run setup gates (routing injection, vendoring warnings). Most repo-native skills should stay tier 1–2.

### Execution tiers (Quick / Standard / Exhaustive)

For test-and-fix or review workflows, state tiers explicitly:

| Tier | Scope | When to use |
|------|-------|-------------|
| Quick | Critical/high only | CI green, time-boxed |
| Standard | + medium issues | Pre-PR default |
| Exhaustive | + cosmetic/low | Release candidate |

Document default tier in the workflow section, not only in the description.

### Dual role framing

When a skill both **diagnoses** and **fixes**, say so upfront:

```markdown
## Role
You are a QA engineer and bug-fix engineer. Report findings, then fix and re-verify.
```

For report-only variants, split skills (see gstack `qa` vs `qa-only`) instead of one overloaded skill.

### Phased workflows

Number explicit phases for multi-step pipelines:

1. **Investigate** — reproduce, capture evidence
2. **Analyze** — root cause, blast radius
3. **Implement** — minimal fix, atomic commits
4. **Verify** — re-run checks, before/after metrics

Plan-review skills (`autoplan`, `/plan-*-review`) chain phases across *other* skills; keep each skill's phases self-contained.

### Voice triggers

Speech-to-text aliases belong in the description (or a `Voice triggers:` line), separate from primary `triggers:`:

```yaml
description: >
  Systematically QA test a site. Triggers: "qa", "test this site".
  Voice triggers (speech-to-text aliases): "quality check", "test the app".
```

### Skill routing block

gstack pack skills include a **Skill routing** section mapping intents to slash skills. Repo-native skills should use `related` registry metadata and cross-links instead of duplicating a global routing table.

See also: [gstack-version.md](gstack-version.md), [gstack-refresh.md](gstack-refresh.md).
