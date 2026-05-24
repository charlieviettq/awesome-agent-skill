---
name: skill-supply-chain-audit
description: >
  Audit third-party agent skills before install—metadata, triggers, scripts,
  network/exfil patterns, and overlap with existing skills. Use before importing
  skills from external catalogs or vendoring new SKILL.md files.
  Triggers: "audit skill", "import skill", "skill security", "third-party skill".
---

# Skill supply chain audit

## When to run

- Before adding skills from Antigravity, skills.sh, or unknown repos.
- After updating vendored skill packs.
- When a skill requests unusual permissions or runs shell scripts.

## Audit checklist

| Check | Pass criteria |
|-------|----------------|
| Source | Known repo, license noted, pinned version or commit |
| Frontmatter | `name` matches folder; description matches behavior |
| Triggers | No overly broad auto-invoke (e.g. every message) |
| Scripts | No obfuscated code; no blind `curl \| bash` |
| Network | No hidden exfil endpoints; env secrets not required unless justified |
| Overlap | Not duplicate of gstack/voltagent/local skill |
| Risk tier | Document if offensive security or prod-destructive |

## Risk tiers

- **Low:** Markdown-only workflow guidance.
- **Medium:** Runs project test/lint commands; reads repo files.
- **High:** Network calls, credential use, prod mutations, pen-test payloads.

High-risk skills: **opt-in only**; do not add to default `installed_skills` until reviewed.

## Decision

| Outcome | Action |
|---------|--------|
| Adopt | Copy/adapt to local style; register in skill-config |
| Adapt | Extract pattern; shorten; remove unsafe steps |
| Reject | Do not install; note reason |

## Output

Short audit note: source, risk tier, overlap, adopt/adapt/reject, required mitigations.
