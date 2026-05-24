---
name: frontend-ui-engineering
description: Build and refine web UI—component structure, responsive layout, design tokens, state, and accessibility. Use for feature UI work beyond WCAG checks alone. Triggers: "build UI", "component", "responsive", "design system", "frontend", "layout".
---

# Frontend UI Engineering

End-to-end UI implementation: structure, styling, responsive behavior, state, and accessibility. Extends `frontend-ui-accessibility` with architecture and design-system discipline.

## When to use

- New page, form, or interactive component
- Refactoring UI for consistency or responsiveness
- Applying or extending a design system

## When not to use

- Backend-only change
- Accessibility audit only (use `frontend-ui-accessibility`)
- Full visual redesign exploration (consider design consultation workflows)

## Workflow

1. **Inventory** — existing components, tokens, patterns to reuse
2. **Structure** — semantic HTML; split presentational vs container components
3. **Layout** — mobile-first breakpoints; avoid fixed widths that break small screens
4. **State** — local vs shared; minimize prop drilling; document async/loading/error UI
5. **Styling** — tokens (color, spacing, type); no magic numbers scattered
6. **A11y** — keyboard, focus, labels, contrast (see `frontend-ui-accessibility`)
7. **Verify** — key viewports; critical user paths; no console errors

## Checklist

| Area | Check |
|------|-------|
| Components | Single responsibility; reusable primitives |
| Responsive | Works at 320px and desktop; touch targets adequate |
| Loading/empty/error | All three states designed |
| Performance | Avoid unnecessary re-renders; lazy-load heavy assets |
| A11y | Focus order, ARIA only when needed, form labels |

## Output

- Implemented components with consistent patterns
- Brief note on new tokens or patterns added to the design system

## Related skills

- `frontend-ui-accessibility` — WCAG-focused review
- `browser-testing-with-devtools` — runtime verification
- `performance-optimization` — bundle and render performance

*Adapted from [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) (MIT).*
