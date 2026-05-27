# GStack pack refresh process

Controlled workflow to re-vendor `.cursor/skills/gstack/` from upstream without touching other domains (`core-workflow/`, `reliability-ops/`, etc.).

## Prerequisites

- Shallow clone of upstream: `git clone --depth 1 https://github.com/garrytan/gstack.git /tmp/gstack-upstream`
- Branch dedicated to refresh (e.g. `plan-gstack-align`)

## Phase 1 — Metadata-first re-vendor

1. Run refresh script:

```bash
python3 scripts/refresh-gstack-pack.py /path/to/gstack-upstream
# dry run first:
python3 scripts/refresh-gstack-pack.py /path/to/gstack-upstream --dry-run
```

2. Regenerate derived artifacts:

```bash
python3 scripts/generate-registry.py
python3 scripts/generate-quality.py
python3 scripts/generate-catalog.py
python3 scripts/convert-to-claude.py --in-repo
```

3. Verify:

```bash
python3 scripts/skillhub.py doctor
python3 scripts/skillhub.py doctor --gstack
python3 scripts/skillhub.py eval-recommend
python3 scripts/validate-skills.py
```

`generate-registry.py` tolerates new frontmatter fields (`preamble-tier`, `version`, YAML `triggers:`). Unknown fields are ignored; triggers are extracted from YAML lists when present.

## Phase 2 — Routing and eval

1. If new skills were added, extend `registry/recommend-fixtures.json` with 1–2 queries each.
2. Confirm MECE: generic workflows stay in `core-workflow/*`; gstack remains **imported specialist** (browser QA, ship pipeline, plan-review gauntlet).
3. Re-run `skillhub eval-recommend` until top-5 hit rate is stable.

## Phase 3 — Optional content merge

Cherry-pick ideas from refreshed gstack skills into repo-native skills **only when**:

- The pattern is generally useful (tiers, phases, role framing)
- Wording is rewritten for this repo (not copy-paste)
- Boundaries stay clear (see [gstack-diff.md](gstack-diff.md) MECE table)

Do **not** edit gstack pack files for one-off customizations; record local patches in `registry/gstack-sync.json` → `local_patches`.

## Version tracking

After refresh, confirm:

- `registry/gstack-sync.json` — commit, version, synced_at, skill counts
- `registry/manifest.json` — `gstack_*` fields (preserved by `pack-skills.py`)
- [gstack-version.md](gstack-version.md) — human summary (update dates/commits)

## Future upgrades

```bash
cd /tmp/gstack-upstream && git pull
python3 scripts/refresh-gstack-pack.py /tmp/gstack-upstream
# … regenerate + doctor + eval as above
git diff --stat .cursor/skills/gstack/
```

Compare diff before merge; pay extra attention to `qa`, `review`, `autoplan`, `office-hours` if upstream changelog mentions them.

## Guardrails

- Do not modify gstack pack content except via `refresh-gstack-pack.py` from a pinned upstream commit.
- Do not reimplement registry/doctor/eval/catalog — use existing SkillHub tooling.
- Open a dedicated PR for each gstack refresh; avoid mixing with unrelated skill additions.
