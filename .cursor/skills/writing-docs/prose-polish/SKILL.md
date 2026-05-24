---
name: prose-polish
description: >
  Polish technical and stakeholder prose—clarity, tone, structure, and reducing
  generic AI-writing patterns. Use for blog posts, Confluence, READMEs, exec
  summaries, and user-facing copy before publish.
  Triggers: "edit prose", "polish writing", "sounds like AI", "copy edit", "tone".
---

# Prose polish

## Goals

- Clear, specific, appropriate for audience (engineer vs exec vs end user).
- Active voice where it helps scanning.
- No false certainty; claims tied to evidence when factual.

## Pass order

1. **Structure** — thesis upfront; one idea per paragraph; headings match content.
2. **Clarity** — cut filler; replace vague words (leverage, robust, delve) with specifics.
3. **Accuracy** — numbers, dates, product names; avoid invented citations.
4. **Tone** — match org style; professional without hype.
5. **Final read** — read aloud for rhythm and redundancy.

## AI-writing patterns to remove

| Pattern | Fix |
|---------|-----|
| Empty opener ("In today's world...") | Start with the point |
| Hedging stack | One clear qualification |
| Buzzword salad | Name the mechanism or metric |
| List for everything | Prose when narrative helps |
| Fake symmetry | Keep only real trade-offs |

## Technical docs

- Lead with outcome and constraints.
- Use tables for comparisons; prose for narrative decisions.
- Callouts for warnings; link ADR or ticket for decisions.

## Bilingual (VI/EN) note

When both languages appear: keep terminology consistent; do not mix languages mid-sentence without reason.

## Output

Return edited text or a short change log (structure, clarity, tone) if user prefers diff-style feedback.

## Related

`pptx` for slide decks; `docx` for Word deliverables.
