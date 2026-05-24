---
name: reflect-yourself
description: Self-learning system that captures corrections, discovers workflow patterns, and syncs learnings to skills and rules. Use when ending a session, after corrections, or when the user wants to formalize learnings (v1.1.3).
---

# reflect-yourself

A self-learning system for Cursor that captures corrections and syncs them to the right place.

## Workflow

When invoked:

1. **Analyze** session (and optionally ask clarifying questions if scope is unclear)
2. **Present** learnings for review (summary-first, then cards; see command file)
3. **Capture action** via the Cursor agent tool **Ask questions** (message-question) when possible — offer Apply all / Apply selected / Skip all / Partial / Other; see Cursor docs → Agent overview → Tools
4. **Apply** only after explicit user approval (via Q&A or typed reply)

## Inputs

| Input | Default | Description |
|-------|---------|-------------|
| Scope | Current conversation | "this session" / "also queue" / "discover skills" |
| Mode | Full review | "quick" (apply high-confidence only) / "full" |

## Commands

When the user invokes these commands, read the corresponding file in `commands/`:

| Command | File |
|---------|------|
| `/reflect-yourself` | `commands/reflect-yourself.md` |
| `/reflect-yourself-skills` | `commands/reflect-yourself-skills.md` |
| `/reflect-yourself-queue` | `commands/reflect-yourself-queue.md` |
| `/reflect-yourself-skip` | `commands/reflect-yourself-skip.md` |

## Quick Start

1. At session end, run `/reflect-yourself`
2. Review captured learnings (summary + cards)
3. Choose action via prompt or reply (apply / edit / skip / redirect)
4. Learnings are applied to skills/rules after approval

## Placement Logic

- **Project Skills** (`.cursor/skills/`) → Codebase-specific
- **Personal Skills** (`~/.cursor/skills/`) → Reusable across projects
- **Project Rules** (`.cursor/rules/`) → Coding standards

## Queue Location

Pending learnings: `~/.cursor/reflect-queue.json` (global location, never pollutes project repos)

## Security

- **Trust model:** Only install skills from sources you trust. Skills are loaded into the agent context and can influence behavior.
- **Import hygiene:** Prefer official or well-known repos; inspect `SKILL.md` and command/rules files before installing. Be wary of skills that instruct the agent to run arbitrary code or exfiltrate data.
- **This skill:** Only instructs the agent to write to `.cursor/skills/`, `.cursor/rules/`, and `~/.cursor/skills/`. The installer copies files only; it does not execute skill content. After install, review `~/.cursor/skills/reflect-yourself/` if you want to verify contents.

## Update check

When main commands are run, the agent may check for a newer npm version. If one exists, the user can be prompted (Yes/No) to run `npx reflect-yourself@latest`. See command files for details.
