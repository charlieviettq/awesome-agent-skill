# Accessibility reference (WCAG-oriented)

## Perceivable

| Check | Target |
|-------|--------|
| Text contrast | 4.5:1 normal text; 3:1 large text |
| Non-text contrast | UI components 3:1 |
| Alt text | Informative images described; decorative empty |
| Captions | Video/audio alternatives when media present |

## Operable

| Check | Notes |
|-------|-------|
| Keyboard | All functionality without mouse |
| Focus visible | Custom focus ring if outline removed |
| Skip link | Long pages: skip to main content |
| Time limits | User can extend or disable where possible |

## Understandable

| Check | Notes |
|-------|-------|
| Labels | Every input has visible or programmatic label |
| Errors | Clear message + how to fix |
| Language | `lang` on `html` |

## Robust

| Check | Notes |
|-------|-------|
| Valid HTML | Prefer semantic elements over div soup |
| ARIA | Correct role/state; no redundant roles |
| Name/role/value | Custom widgets expose accessible name |

## Quick manual test

1. Tab through entire flow without mouse
2. Zoom 200% — content still usable
3. Screen reader spot-check on primary path (VoiceOver/NVDA)

## Tools (optional)

axe DevTools, Lighthouse accessibility audit, eslint-plugin-jsx-a11y
