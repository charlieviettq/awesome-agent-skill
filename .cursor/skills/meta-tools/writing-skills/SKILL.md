---
name: writing-skills
description: >
  Author and pressure-test agent skills—triggers, thin SKILL.md, references, validation.
  Use when creating or revising skills in this repo. Triggers: "write a skill", "new skill",
  "skill authoring", "improve skill triggers".
---

# Writing skills

## When to use

- Adding a skill under `.cursor/skills/<domain>/<name>/`
- Fixing discovery issues (agent never invokes the skill)
- Splitting an oversized skill into SKILL.md + reference.md

## When not to use

- One-off project instructions (use README or rules)
- Copying entire third-party skill trees without audit

## Workflow

1. Read [`docs/skill-writing-guide.md`](../../../../docs/skill-writing-guide.md) and [`docs/review-rubric.md`](../../../../docs/review-rubric.md)
2. Run `skill-supply-chain-audit` if source is external
3. Draft frontmatter: `name` matches folder; description includes **Triggers:**
4. Keep SKILL.md thin; move long examples to `reference.md`
5. Pressure-test: list 3 user phrases that should trigger and 2 that should not
6. Run `python3 scripts/validate-skills.py`
7. Regenerate Claude skills if editing Cursor source

## Description quality

- **Good:** concrete workflow + quoted trigger phrases
- **Bad:** broad "use for everything" or "MUST run before any action"

## Checklist before PR

- [ ] Public-safe (no secrets, no auto-push scripts in skill body)
- [ ] No duplicate of existing skill in `SKILL_INVENTORY.md`
- [ ] Entry in `EXTERNAL_SKILLS.md` if adapted from upstream
- [ ] `CHANGELOG.md` updated under Unreleased

## Related

`skill-supply-chain-audit`, `reflect-yourself`, `core-workflow/planning-and-task-breakdown`

*Authoring practices inspired by [obra/superpowers](https://github.com/obra/superpowers) (MIT).*
