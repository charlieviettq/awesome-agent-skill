# Skill Review Rubric

Use this rubric when reviewing new or updated skills.

| Dimension | Pass | Fail |
|-----------|------|------|
| Naming | `name` matches folder; kebab-case; unique | Mismatch, duplicate, or vague name |
| Triggers | Frontmatter has `triggers` list with realistic phrases | Agent cannot tell when to invoke |
| Scope | Single workflow; clear non-goals | Kitchen-sink skill covering unrelated tasks |
| Safety | No secrets/PII/internal URLs | Credential patterns, private tenant names |
| Overlap (MECE) | Distinct from nearby skills; `Related Skills` lists neighbors | Duplicates `core-workflow/*` or gstack/voltagent without reason |
| Contract | `## Contract` states what is guaranteed on success | Only describes topic, not outcome |
| Phases | `## Phases` present with 2–7 clear stages | No sense of progression or order |
| Output | `## Output Format` describes shape of answer/artifact | No done condition or output shape |
| Anti-Patterns | `## Anti-Patterns` lists at least 2–3 failure modes to avoid | Skill silently does risky or out-of-scope work |
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
