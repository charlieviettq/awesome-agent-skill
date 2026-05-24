# Testing reflect-yourself

There is no automated test suite. Test by running the installer and then trying the commands in Cursor.

## Simplest way to test

1. **Use the branch:** In this repo, switch to the feature branch (e.g. `improve/ux-security-org`). If you use a worktree, the branch is there; in the main clone you can’t check out the same branch while the worktree has it, so run the steps below from the worktree.
2. **Install:** From the repo root (on that branch), run `node bin/install.js`. That overwrites your global `~/.cursor/skills/reflect-yourself/` with this version.
3. **Test in Cursor:** Open any project, run `/reflect-yourself` (and queue/skip/skills as needed). Check summary-first, cards, and Ask Question prompts.
4. **Restore stable:** When done, run `npx reflect-yourself@latest` to reinstall the published version. Your global install is back to stable.

## Optional: test without overwriting global

Use a **test project**: create a folder, then copy the branch’s skill into that project’s `.cursor/skills/reflect-yourself/` (copy `SKILL.md`, `commands/`, `rules/`, `references/` from the repo). Open that folder in Cursor; it will use the project skill and leave `~/.cursor/skills/reflect-yourself/` unchanged. When done, delete `.cursor/skills/reflect-yourself` from the test project.

## 1. Test the installer

From the repo root:

```bash
node bin/install.js
```

**Check:**

- `~/.cursor/skills/reflect-yourself/` exists and contains:
  - `SKILL.md`, `commands/*.md`, `rules/session-reflect.mdc`, `references/ONBOARDING.md`
- `~/.cursor/reflect-queue.json` exists (empty `{ "version": 1, "learnings": [] }` if new)
- Console shows “Installing files…” and “Installed to …”
- If you’re on an older version than npm, you should see: “A newer version (x.y.z) is available…” (optional; depends on registry)

**Optional:** Run `npx reflect-yourself` from another directory (or with a different version in `package.json`) to confirm the version-check message when a newer version is published.

## 2. Test in Cursor (manual)

Open a project in Cursor where the skill is installed (or will be after step 1). Use a session where you can safely create/change `.cursor/skills/` or `.cursor/rules/` (or use a throwaway project).

### `/reflect-yourself`

1. In chat, say something that looks like a correction (e.g. “remember: always run tests before committing” or “no, use X not Y”).
2. Run **`/reflect-yourself`**.
3. **Verify:**
   - A **summary line** appears first (e.g. “X learnings · Y high-confidence · …”).
   - Learnings are in **cards** (numbered, type badge, Confidence | Destination), not one big table.
   - “Why this was captured” is present (in `<details>` or a short line).
   - You get an **Ask Question** with choices like Apply all / Apply selected / Skip all / Partial / Other (or the agent offers them). You can also reply with “1,2” or “skip all” and it still works.
4. Choose **Apply** for one learning and confirm it appears in the right place (e.g. `.cursor/skills/…` or `~/.cursor/skills/…`).
5. Final message is a short **Reflection complete** with Applied / Skipped and optional icons (e.g. ✅ ⏭️), no wide tables.

### `/reflect-yourself-queue`

1. Ensure the queue has at least one item (e.g. run `/reflect-yourself`, choose “queue” or leave one learning unprocessed so it stays in the queue).
2. Run **`/reflect-yourself-queue`**.
3. **Verify:**
   - Output is **card-style** (no wide table), with Total and per-item lines (Date, Confidence, Status).
   - An **Ask Question** appears (e.g. “Process queue now?” with Yes / No / Discard all).

### `/reflect-yourself-skip`

1. With at least one item in the queue, run **`/reflect-yourself-skip`**.
2. **Verify:**
   - Discard list is **card-style** (no wide table).
   - An **Ask Question** for confirmation (e.g. Yes, discard all / No, keep queue).
   - After confirming, queue is cleared and you see a short success message.

### `/reflect-yourself-skills`

1. Run **`/reflect-yourself-skills`** in a session that has some repeat patterns (or after a few corrections).
2. **Verify:**
   - Skill candidates are listed in a clear format.
   - When relevant, the agent uses **Ask Question** for “Which skills to generate?” and/or “Analyze previous conversations?”.

### Update check (optional)

- If a newer version is on npm and the skill description still has the old version, run `/reflect-yourself` or `/reflect-yourself-queue` and see if the agent mentions an update and offers an **Update now / Later** choice (per command instructions). This depends on Cursor and npm being available.

## 3. Sanity checks

- **No horizontal scroll:** All command outputs (learnings, queue, skip, summary) should wrap; no wide tables that force horizontal scroll.
- **Safety:** In a session, mention “from the web” or “from docs” and run `/reflect-yourself`; the agent should not paste raw external instructions into skills without citing source and/or asking.
- **Onboarding:** Open `~/.cursor/skills/reflect-yourself/references/ONBOARDING.md` and confirm it summarizes commands and links to the GitHub README.

## 4. Quick checklist (before release)

- [ ] `node bin/install.js` completes and all files (including `references/ONBOARDING.md`) are present under `~/.cursor/skills/reflect-yourself/`.
- [ ] `/reflect-yourself`: summary-first, cards, Ask Question for actions, reflection complete summary.
- [ ] `/reflect-yourself-queue`: card-style list, Ask Question for “Process queue now?”.
- [ ] `/reflect-yourself-skip`: card-style discard list, Ask Question for confirm before clear.
- [ ] `/reflect-yourself-skills`: Ask Question used for choices when appropriate.
- [ ] No wide tables in any command output; optional icons/emoji are fine.
- [ ] README “Changelog-aligned opportunities” and Safety/trust/import hygiene are present and accurate.
