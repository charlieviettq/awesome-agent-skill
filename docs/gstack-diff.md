# GStack upstream vs local diff

Comparison between [garrytan/gstack](https://github.com/garrytan/gstack) @ `a6fb317` (v1.48.0.0) and the vendored pack in `.cursor/skills/gstack/`.

## Layout

| Aspect | Upstream | Local (awesome-agent-skill) |
|--------|----------|---------------------------|
| Skill paths | Flat dirs at repo root (`qa/`, `ship/`, …) | Nested under `gstack/<category>/` |
| Pack meta | Root `SKILL.md` | `gstack/SKILL.md` |
| OpenClaw skills | `openclaw/skills/gstack-openclaw-*` | `gstack/remote-agents/openclaw/gstack-openclaw-*` |

## Skill inventory (after refresh)

| Action | Skills |
|--------|--------|
| **Synced (upgrade content)** | All 57 mapped upstream skills including priority `qa`, `qa-only`, `review`, `autoplan`, `office-hours` |
| **Added (were missing locally)** | `document-generate`, `make-pdf`, `spec`, `ios-clean`, `ios-design-review`, `ios-fix`, `ios-qa`, `ios-sync` |
| **Kept (path remap only)** | `browser-qa/*`, `code-quality/*`, `plan-review/*`, `deploy-ship/*`, etc. |
| **Not imported separately** | Upstream root helpers (`bin/`, `lib/`, extension) — out of scope for skill pack |

## Frontmatter evolution

| Pattern | Pre-refresh local | Upstream / post-refresh |
|---------|-------------------|-------------------------|
| `preamble-tier` | No | Yes (1–4, controls bootstrap noise) |
| `version` | No | Yes (e.g. `2.0.0` on `qa`) |
| `triggers` | Embedded in `description` | YAML list |
| `allowed-tools` | No | Yes |
| Voice triggers | In description text | Often in description + speech aliases in body |
| Execution tiers | Mentioned in description | Explicit Quick / Standard / Exhaustive sections (`qa`) |

## MECE with core-workflow

| gstack skill | Local equivalent | Recommendation |
|--------------|------------------|----------------|
| `review` | `core-workflow` PR review patterns | Prefer **core-workflow** for generic repo workflow; **gstack/review** for diff-landing + SQL/LLM boundary checks |
| `investigate` | `core-workflow/test-failure-triage`, gstack investigate | Prefer **gstack/investigate** for runtime RCA with browser evidence |
| `ship` | `reliability-ops/shipping-launch-checklist` | **gstack/ship** for full land workflow; checklist for policy-only |
| `spec` | `core-workflow/spec-driven-development` | **core-workflow** for repo-native specs; **gstack/spec** when using gstack plan pipeline |

## Slash commands covered

Upstream slash skills now represented in the pack:

`/office-hours`, `/plan-*-review`, `/autoplan`, `/devex-review`, `/review`, `/qa`, `/qa-only`, `/ship`, `/land-and-deploy`, `/canary`, `/codex`, `/cso`, `/careful`, `/freeze`, `/guard`, `/unfreeze`, `/gstack-upgrade`, `/learn`, `/scrape`, `/skillify`, `/spec`, `/document-generate`, `/make-pdf`, `/ios-*`, OpenClaw CEO/investigate/office-hours/retro, `/pair-agent`, design + context + gbrain skills.

## Classification legend

- **Upgrade content** — replace local SKILL.md from upstream
- **Add new** — skill did not exist locally
- **Keep** — already present; no upstream change required this cycle
- **Skip** — not vendored (binaries, MCP hosts, native app code)
