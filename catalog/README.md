# SkillHub Marketplace (static)

Modern browser UI for the skill registry — search, filters, bundle cards, and a **Describe your task** advisor.

## Generate

```bash
python3 scripts/generate-catalog.py
```

Copies `registry/*.json` into `catalog/data/`, renders `index.html` from `index.template.html`, and writes `.nojekyll` for GitHub Pages.

## Preview locally

```bash
python3 -m http.server 8765 --directory catalog
# open http://localhost:8765
```

## Deploy

- **GitHub Pages**: push to `main`; workflow `.github/workflows/pages.yml` builds and deploys `catalog/`.
- Or host `catalog/` on any static CDN.

## Features

- Hero + task advisor (client-side recommend engine, same scoring as CLI)
- Bundle landing sections from `registry/bundles.json`
- Skill grid with domain / tier / risk / agent filters
- Copy install commands per skill and bundle
- Links to `SKILL.md` on GitHub

Regenerate after skill or registry changes, or run `python3 scripts/skillhub.py sync`.
