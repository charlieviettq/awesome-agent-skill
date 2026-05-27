#!/usr/bin/env python3
"""Generate static SkillHub web catalog under catalog/."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
BUNDLES = ROOT / "registry" / "bundles.json"
QUALITY = ROOT / "registry" / "quality.json"
OUT_DIR = ROOT / "catalog"
DATA_DIR = OUT_DIR / "data"


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>SkillHub Catalog — awesome-agent-skill</title>
  <style>
    :root {{ font-family: system-ui, sans-serif; color: #111; background: #f6f7f9; }}
    body {{ margin: 0; padding: 1.5rem; max-width: 1100px; margin-inline: auto; }}
    h1 {{ margin-top: 0; }}
    .meta {{ color: #555; margin-bottom: 1rem; }}
    input {{ width: 100%; padding: 0.6rem 0.8rem; font-size: 1rem; border: 1px solid #ccc; border-radius: 8px; }}
    .filters {{ display: flex; gap: 0.5rem; flex-wrap: wrap; margin: 0.75rem 0 1rem; }}
    .filters button {{ padding: 0.35rem 0.7rem; border-radius: 999px; border: 1px solid #ccc; background: #fff; cursor: pointer; }}
    .filters button.active {{ background: #1a56db; color: #fff; border-color: #1a56db; }}
    .grid {{ display: grid; gap: 0.75rem; }}
    .card {{ background: #fff; border: 1px solid #e5e7eb; border-radius: 10px; padding: 0.9rem 1rem; }}
    .card h3 {{ margin: 0 0 0.35rem; font-size: 1rem; }}
    .card .id {{ font-family: ui-monospace, monospace; font-size: 0.85rem; color: #374151; }}
    .card p {{ margin: 0.4rem 0 0; color: #4b5563; font-size: 0.9rem; line-height: 1.4; }}
    .badge {{ display: inline-block; font-size: 0.75rem; padding: 0.1rem 0.45rem; border-radius: 4px; background: #eef2ff; color: #3730a3; margin-right: 0.25rem; }}
    .score {{ float: right; font-size: 0.8rem; color: #6b7280; }}
  </style>
</head>
<body>
  <h1>SkillHub Catalog</h1>
  <p class="meta">{count} skills · generated from <code>registry/skills.json</code></p>
  <input id="q" type="search" placeholder="Search skills, domains, triggers…" autofocus />
  <div class="filters" id="domains"></div>
  <div class="grid" id="list"></div>
  <script>
    const skills = SKILLS_DATA;
    const quality = QUALITY_MAP;
    const params = new URLSearchParams(location.search);
    let domainFilter = params.get('domain') || '';
    const q = document.getElementById('q');
    const list = document.getElementById('list');
    const domains = document.getElementById('domains');

    const domainSet = [...new Set(skills.map(s => s.domain))].sort();
    function renderFilters() {{
      domains.innerHTML = '';
      const all = document.createElement('button');
      all.textContent = 'All';
      all.className = domainFilter ? '' : 'active';
      all.onclick = () => {{ domainFilter = ''; render(); }};
      domains.appendChild(all);
      domainSet.forEach(d => {{
        const b = document.createElement('button');
        b.textContent = d;
        b.className = domainFilter === d ? 'active' : '';
        b.onclick = () => {{ domainFilter = d; render(); }};
        domains.appendChild(b);
      }});
    }}

    function render() {{
      const term = (q.value || '').toLowerCase();
      const filtered = skills.filter(s => {{
        if (domainFilter && s.domain !== domainFilter) return false;
        if (!term) return true;
        const blob = [s.id, s.name, s.domain, s.description, ...(s.tags||[]), ...(s.triggers||[])].join(' ').toLowerCase();
        return blob.includes(term);
      }});
      list.innerHTML = filtered.map(s => {{
        const sc = quality[s.id];
        const scoreHtml = sc != null ? `<span class="score">Q${{sc}}</span>` : '';
        const tags = (s.tags || []).slice(0, 4).map(t => `<span class="badge">${{t}}</span>`).join('');
        return `<article class="card">${{scoreHtml}}<h3>${{s.name}}</h3><div class="id">${{s.id}}</div><div>${{tags}}</div><p>${{(s.description||'').slice(0, 200)}}</p></article>`;
      }}).join('');
      document.querySelector('.meta').textContent = `${{filtered.length}} / ${{skills.length}} skills shown`;
    }}

    q.addEventListener('input', render);
    renderFilters();
    render();
  </script>
</body>
</html>
"""


def main() -> int:
    if not REGISTRY.exists():
        print("Missing registry/skills.json", file=sys.stderr)
        return 1
    skills_data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    quality_map: dict[str, int] = {}
    if QUALITY.exists():
        qdata = json.loads(QUALITY.read_text(encoding="utf-8"))
        quality_map = {r["id"]: r["score"] for r in qdata.get("skills", [])}

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    shutil.copy2(REGISTRY, DATA_DIR / "skills.json")
    if BUNDLES.exists():
        shutil.copy2(BUNDLES, DATA_DIR / "bundles.json")

    skills_json = json.dumps(skills_data["skills"], ensure_ascii=False)
    quality_json = json.dumps(quality_map, ensure_ascii=False)
    html = (
        HTML_TEMPLATE.replace("SKILLS_DATA", skills_json)
        .replace("QUALITY_MAP", quality_json)
        .replace("{count}", str(skills_data["count"]))
    )
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    print(f"Wrote {OUT_DIR / 'index.html'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
