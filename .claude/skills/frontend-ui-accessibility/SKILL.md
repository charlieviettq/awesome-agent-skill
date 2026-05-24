---
name: frontend-ui-accessibility
description: "Build accessible UI—semantic HTML, keyboard support, ARIA when needed, WCAG-oriented checks. Use when implementing or reviewing web UI, forms, modals, and design systems."
allowed-tools: Read, Glob, Grep
---

# Frontend UI and accessibility

## Defaults

- Semantic HTML first; ARIA only when native semantics insufficient
- Keyboard-operable for every interactive control
- Visible focus states; do not remove outlines without replacement
- Color contrast and non-color-only status cues

## Build checklist

- [ ] Heading hierarchy (`h1` once per view where applicable)
- [ ] Labels tied to inputs (`label`/`for` or `aria-labelledby`)
- [ ] Buttons vs links used correctly
- [ ] Modals: focus trap, `Escape`, return focus on close
- [ ] Images: meaningful `alt` or decorative `alt=""`
- [ ] Dynamic updates: `aria-live` when needed

## Review checklist

- [ ] Tab order logical; no keyboard traps
- [ ] Touch targets adequate on mobile
- [ ] Motion respects `prefers-reduced-motion`
- [ ] Forms: errors associated with fields

## Performance interaction

Avoid layout thrash; lazy-load below fold; measure LCP/CLS when shipping UI.

## Related

- [reference.md](reference.md) — WCAG-oriented checklist
- `performance/performance-optimization` — web vitals
- `gstack/design-review` — visual polish (complementary)
