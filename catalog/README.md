# SkillHub Web Catalog (static)

Mini browser for the skill registry. No build step beyond Python generation.

## Generate

```bash
python3 scripts/generate-catalog.py
```

Requires `registry/skills.json`. Optionally includes quality scores if `registry/quality.json` exists.

## Preview locally

```bash
python3 -m http.server 8765 --directory catalog
# open http://localhost:8765
```

## Deploy

Host the `catalog/` folder on GitHub Pages, S3, or any static host. Commit regenerated `index.html` when skills change, or run generate step in CI before deploy.
