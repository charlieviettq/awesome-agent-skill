# Good First Issues (templates)

Copy any item below into a GitHub issue and label `good first issue`.

---

## 1. Add triggers to `performance/performance-optimization`

**Acceptance:** frontmatter description includes `Triggers:` with 3+ quoted phrases; `python3 scripts/validate-skills.py` passes.

**Files:** `.cursor/skills/performance/performance-optimization/SKILL.md`

---

## 2. Document install scripts in README examples

**Acceptance:** README shows `install-domain.sh` and `install-bundle.sh` with copy-paste examples.

**Files:** `README.md`

---

## 3. Add mobile bundle to install-bundle.sh

**Acceptance:** new bundle `mobile-release` installs `mobile/` + `reliability-ops/serverless-debugging` docs cross-link.

**Files:** `scripts/install/install-bundle.sh`, `README.md`

---

## 4. Skill: `reliability-ops/feature-flag-rollout`

**Acceptance:** new skill with triggers, workflow, verification; inventory + Claude map updated.

**Files:** `.cursor/skills/reliability-ops/feature-flag-rollout/SKILL.md`

---

## 5. Skill: `core-workflow/pr-description-writer`

**Acceptance:** skill helps draft PR summary + test plan from git diff; public-safe.

---

## 6. Sync hero SVG skill count with map

**Acceptance:** `.github/assets/readme-hero.svg` count matches `scripts/claude-skill-map.json` length.

---

## 7. Add OpenCode install path doc

**Acceptance:** expand compatibility matrix with verified OpenCode path and reload note.

**Files:** `README.md`, `docs/distribution.md`

---

## 8. Skill: `ai-agent-systems/prompt-regression-checklist`

**Acceptance:** checklist skill for comparing prompt versions before deploy.

---

## 9. Fix broken relative links in one domain

**Acceptance:** run `python3 scripts/validate-skills.py` and resolve any broken links in chosen domain.

---

## 10. Add `docs/metrics/` monthly snapshot

**Acceptance:** run `python3 scripts/repo-metrics.py`; commit generated `docs/metrics/YYYY-MM.md`.

---

## 11. Skill: `writing-docs/changelog-writer`

**Acceptance:** skill templates Keep a Changelog entries from git log.

---

## 12. Expand EXTERNAL_SKILLS hold list

**Acceptance:** add 3 candidate repos with adopt/hold/reject notes.

**Files:** `EXTERNAL_SKILLS.md`

---

## 13. Skill: `security-appsec/secrets-scan-checklist`

**Acceptance:** pre-PR secrets hygiene checklist; no tool vendor lock-in.

---

## 14. Add issue template link to CONTRIBUTING

**Acceptance:** `.github/CONTRIBUTING.md` links to this file.

---

## 15. Skill: `product-growth/readme-audit`

**Acceptance:** skill audits README for discoverability (badges, quickstart, works-with table).
