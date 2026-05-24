---
name: context-restore
description: Restore working context saved earlier by /context-save. Loads the most
  recent saved state (across all branches by default) so you can pick up where you
  left off — even across Conductor workspace handoffs. Use when asked to "resume",
  "restore context", "where was I", or "pick up where I left off". Pair with /context-save.
  Formerly /checkpoint resume — renamed because Claude Code treats /checkpoint as
  a native rewind alias in current environments. (gstack)
---

## Skill routing

When the user's request matches an available skill, invoke it via the Skill tool. When in doubt, invoke the skill.

Key routing rules:
- Product ideas/brainstorming → invoke /office-hours
- Strategy/scope → invoke /plan-ceo-review
- Architecture → invoke /plan-eng-review
- Design system/plan review → invoke /design-consultation or /plan-design-review
- Full review pipeline → invoke /autoplan
- Bugs/errors → invoke /investigate
- QA/testing site behavior → invoke /qa or /qa-only
- Code review/diff check → invoke /review
- Visual polish → invoke /design-review
- Ship/deploy/PR → invoke /ship or /land-and-deploy
- Save progress → invoke /context-save
- Resume context → invoke /context-restore
```

Then commit the change: `git add CLAUDE.md && git commit -m "chore: add gstack skill routing rules to CLAUDE.md"`

If B: run `~/.claude/skills/gstack/bin/gstack-config set routing_declined true` and say they can re-enable with `gstack-config set routing_declined false`.

This only happens once per project. Skip if `HAS_ROUTING` is `yes` or `ROUTING_DECLINED` is `true`.

If `VENDORED_GSTACK` is `yes`, warn once via AskUserQuestion unless `~/.gstack/.vendoring-warned-$SLUG` exists:

> This project has gstack vendored in `.claude/skills/gstack/`. Vendoring is deprecated.
> Migrate to team mode?

Options:
- A) Yes, migrate to team mode now
- B) No, I'll handle it myself

If A:
1. Run `git rm -r .claude/skills/gstack/`
2. Run `echo '.claude/skills/gstack/' >> .gitignore`
3. Run `~/.claude/skills/gstack/bin/gstack-team-init required` (or `optional`)
4. Run `git add .claude/ .gitignore CLAUDE.md && git commit -m "chore: migrate gstack from vendored to team mode"`
5. Tell the user: "Done. Each developer now runs: `cd ~/.claude/skills/gstack && ./setup --team`"

If B: say "OK, you're on your own to keep the vendored copy up to date."

Always run (regardless of choice):
```bash
eval "$(~/.claude/skills/gstack/bin/gstack-slug 2>/dev/null)" 2>/dev/null || true
touch ~/.gstack/.vendoring-warned-${SLUG:-unknown}
```

If marker exists, skip.

If `SPAWNED_SESSION` is `"true"`, you are running inside a session spawned by an
AI orchestrator (e.g., OpenClaw). In spawned sessions:
- Do NOT use AskUserQuestion for interactive prompts. Auto-choose the recommended option.
- Do NOT run upgrade checks, telemetry prompts, routing injection, or lake intro.
- Focus on completing the task and reporting results via prose output.
- End with a completion report: what shipped, decisions made, anything uncertain.

## Detect command

Parse the user's input:

- `/context-restore` → load the most recent saved context (any branch)
- `/context-restore <title-fragment-or-number>` → load a specific saved context
- `/context-restore list` → tell the user "Use `/context-save list` — listing
  lives on the save side" and exit. No mode detection here.

---

## Restore flow

### Step 1: Find saved contexts

```bash
eval "$(~/.claude/skills/gstack/bin/gstack-slug 2>/dev/null)" && mkdir -p ~/.gstack/projects/$SLUG
eval "$(~/.claude/skills/gstack/bin/gstack-paths)"
CHECKPOINT_DIR="$GSTACK_STATE_ROOT/projects/$SLUG/checkpoints"
if [ ! -d "$CHECKPOINT_DIR" ]; then
  echo "NO_CHECKPOINTS"
else
  # Use find + sort instead of ls -1t. Two reasons:
  # 1. Canonical order is the filename YYYYMMDD-HHMMSS prefix (stable across
  #    copies/rsync). Filesystem mtime drifts and is not authoritative.
  # 2. On macOS, `find ... | xargs ls -1t` with zero results falls back to
  #    listing cwd. `sort -r` on empty input cleanly returns nothing.
  # Cap at 20 most recent: a user with 10k saved files shouldn't blow the
  # context window just listing them. /context-save list handles pagination.
  FILES=$(find "$CHECKPOINT_DIR" -maxdepth 1 -name "*.md" -type f 2>/dev/null | sort -r | head -20)
  if [ -z "$FILES" ]; then
    echo "NO_CHECKPOINTS"
  else
    echo "$FILES"
  fi
fi
```

**Candidates include every `.md` file in the directory, regardless of branch**
(the branch is recorded in frontmatter, not used for filtering here). This
enables Conductor workspace handoff.

### Step 2: Load the right file

- If the user specified a title fragment or number: find the matching file among
  the candidates.
- Otherwise: load the **first file returned by the `sort -r` above** — that is
  the newest `YYYYMMDD-HHMMSS` prefix, which is the canonical "most recent."

Read the chosen file and present a summary:

```
RESUMING CONTEXT
════════════════════════════════════════
Title:       {title}
Branch:      {branch from frontmatter}
Saved:       {timestamp, human-readable}
Duration:    Last session was {formatted duration} (if available)
Status:      {status}
════════════════════════════════════════

### Summary
{summary from saved file}

### Remaining Work
{remaining work items}

### Notes
{notes}
```

If the current branch differs from the saved context's branch, note this:
"This context was saved on branch `{branch}`. You are currently on
`{current branch}`. You may want to switch branches before continuing."

### Step 3: Offer next steps

After presenting, ask via AskUserQuestion:

- A) Continue working on the remaining items
- B) Show the full saved file
- C) Just needed the context, thanks

If A, summarize the first remaining work item and suggest starting there.

---

## If no saved contexts exist

If Step 1 printed `NO_CHECKPOINTS`, tell the user:

"No saved contexts yet. Run `/context-save` first to save your current working
state, then `/context-restore` will find it."

---

## Important Rules

- **Never modify code.** This skill only reads saved files and presents them.
- **Always search across all branches by default.** Cross-branch resume is the
  whole point. Only filter by branch if the user explicitly asks via a
  title-fragment match that happens to be branch-specific.
- **"Most recent" means the filename `YYYYMMDD-HHMMSS` prefix**, not
  `ls -1t` (filesystem mtime). Filenames are stable across file-system
  operations; mtime is not.
- **This is a gstack skill, not a Claude Code built-in.** When the user types
  `/context-restore`, invoke this skill via the Skill tool.
