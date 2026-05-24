# Skill Review Rubric

Use this rubric when reviewing new or updated skills.

| Dimension | Pass | Fail |
|-----------|------|------|
| Naming | `name` matches folder; kebab-case; unique | Mismatch, duplicate, or vague name |
| Triggers | Description includes `Triggers:` or clear `Use when` | Agent cannot tell when to invoke |
| Scope | Single workflow; clear non-goals | Kitchen-sink skill covering unrelated tasks |
| Safety | No secrets/PII/internal URLs | Credential patterns, private tenant names |
| Overlap | Distinct from nearby skills | Duplicates `core-workflow/*` or gstack/voltagent without reason |
| Verification | Defines output or checks | No done condition |
| Size | Focused SKILL.md; refs in `reference.md` | Very long inline reference dumps |

## Scoring

- **Approve:** all Pass
- **Request changes:** any Fail in Safety or Naming
- **Suggest merge with existing skill:** high overlap with one current skill

## Maintainer checklist

1. Run `python3 scripts/validate-skills.py`
2. Confirm `SKILL_INVENTORY.md` updated if path is new
3. Confirm `CHANGELOG.md` entry under `[Unreleased]` or next version
4. For external inspiration, log provenance in `EXTERNAL_SKILLS.md`
