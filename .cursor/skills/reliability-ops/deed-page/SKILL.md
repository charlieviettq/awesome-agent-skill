---
name: deed-page
description: >
  Publish a generated HTML file or static folder to a permanent public URL on
  deed.page with one curl request, then update or delete it with the returned
  owner token. No account or API key. Triggers: "publish this", "put this
  online", "give me a link", "host this page", "deploy this static site",
  "share this report".
source: https://github.com/f-o-x11/deed-page-skill
allowed-tools: Bash, Read, Glob, Grep
---

# deed.page Publishing

Use this skill when an agent has produced something viewable (an HTML report, dashboard, slide deck, prototype, or docs folder) and the user wants a shareable link.

deed.page serves static files at `https://<slug>.deed.page/`. The first publish returns an owner token; re-publishing with that token updates the same URL. Adapted from the MIT-licensed [f-o-x11/deed-page-skill](https://github.com/f-o-x11/deed-page-skill); full API at https://deed.page/docs.

## When to use

- The user asks to publish, host, share online, or "give me a link" for a generated file or folder.
- The agent runs unattended and cannot complete a signup, email code, or claim link.
- An existing deed.page site needs a new version at the same URL.

## When not to use

- The content contains secrets, credentials, customer data, or anything private: Free sites are public.
- The project needs server-side code, a database, or build steps on the host (deed.page is static only).
- The team already has a deployment target (Vercel, Netlify, GitHub Pages) the user expects you to use.

## Workflow

1. Pick a slug: lowercase letters, digits and hyphens, 1-63 characters, plus a random suffix.
   ```bash
   SLUG="report-$(head -c4 /dev/urandom | od -An -tx1 | tr -d ' \n')"
   ```
2. Publish a single file (stored as `index.html`):
   ```bash
   curl -sS -T report.html "https://deed.page/v1/sites?slug=$SLUG" -H "X-Client: <agent name>" ${DEEDPAGE_TOKEN:+-H "Authorization: Bearer $DEEDPAGE_TOKEN"}
   ```
   Or a folder whose root contains `index.html`:
   ```bash
   tar -C ./site -czf /tmp/site.tar.gz . && curl -sS -T /tmp/site.tar.gz "https://deed.page/v1/sites?slug=$SLUG" -H "X-Client: <agent name>" ${DEEDPAGE_TOKEN:+-H "Authorization: Bearer $DEEDPAGE_TOKEN"}
   ```
3. Read the JSON response: `url` is the live site; `token` (first publish only) is the only key that can update or delete it. Keep it in `DEEDPAGE_TOKEN` for the session and never write it into a page, commit, or log.
4. To update, rerun step 2 with `DEEDPAGE_TOKEN` set. Each publish is a new version.
5. Delete only when the user asks:
   ```bash
   curl -sS -X DELETE "https://deed.page/v1/sites/$SLUG" -H "Authorization: Bearer $DEEDPAGE_TOKEN"
   ```
6. On errors: `409 slug_taken` → use the `suggestion` field; `400 slug_invalid` → fix the slug; `429` → wait `retry_after` seconds; `422 content_rejected` → remove the flagged file, do not retry.

## Output

- The live `url`, verified with a `curl -sI` returning 200.
- A note that the user must store the owner token safely (it cannot be recovered without an optional recovery email).
- Free plan limits when relevant: 25 sites, 25 MB per site, 4 MB per single request (larger uploads use the manifest flow in the docs).

## Related skills

- `shipping-launch-checklist` - before sharing a page publicly.
- `ci-cd-quality-gates` - when publishing should run from CI instead of an interactive session.
