---
name: pptx
description: >
  Create and edit PowerPoint presentations (.pptx)—slides, layouts, speaker notes,
  and export. Use when the deliverable is a deck for stakeholders, workshops,
  or model readouts. Complements docx/pdf/xlsx skills.
  Triggers: "PowerPoint", "pptx", "slides", "deck", "presentation".
---

# PowerPoint (pptx)

## When to use

- Stakeholder readouts, training decks, workshop materials.
- Visual narrative where slides beat long documents.

## Workflow

1. **Outline** — audience, timebox, key message per slide (max one idea per slide).
2. **Structure** — title, context, evidence, recommendation, appendix.
3. **Build** — consistent master; limit bullet depth (3 lines max per slide).
4. **Notes** — speaker notes for anything not on slide.
5. **Review** — legibility at projector size; no dense tables on main slides.

## Slide patterns

| Slide type | Content |
|------------|---------|
| Title | Title, subtitle, date, owner |
| Executive summary | 3 bullets max |
| Chart | One chart; source footnote |
| Appendix | Detail tables, methodology |

## Implementation options

- **python-pptx** for programmatic create/edit when scripts exist in repo.
- **Manual edit** guidance when no automation: describe slide-by-slide content for user to paste.
- Prefer editing existing template `.pptx` over blank decks when brand matters.

## Quality checklist

- [ ] Font size readable (body >= 18pt typical)
- [ ] Color contrast sufficient
- [ ] Charts labeled (axes, units, period)
- [ ] No paragraph walls
- [ ] Version/date on title or footer

## Safety

- Do not embed secrets or live customer PII in decks.
- Use aggregated metrics in external-facing decks.

## Boundaries

- Not for PDF-only deliverables (use `pdf` skill).
- Not for spreadsheets as primary output (use `xlsx`).

## Dependencies

If using python-pptx, confirm package available in environment before scripting.
