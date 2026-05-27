#!/usr/bin/env python3
"""Generate static SkillHub marketplace under catalog/."""

from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
BUNDLES = ROOT / "registry" / "bundles.json"
QUALITY = ROOT / "registry" / "quality.json"
SKILLS_ROOT = ROOT / ".cursor" / "skills"
OUT_DIR = ROOT / "catalog"
DATA_DIR = OUT_DIR / "data"
ASSETS_SRC = OUT_DIR / "assets"
TEMPLATE = OUT_DIR / "index.template.html"


def generate_skill_content(skills: list[dict]) -> dict[str, dict]:
    """Extract SKILL.md bodies for inline preview on GitHub Pages."""
    content: dict[str, dict] = {}
    for skill in skills:
        sid = skill["id"]
        path = SKILLS_ROOT / sid / "SKILL.md"
        if not path.is_file():
            continue
        md = path.read_text(encoding="utf-8")
        content[sid] = {
            "name": skill.get("name", sid),
            "domain": skill.get("domain", ""),
            "tier": skill.get("tier"),
            "risk": skill.get("risk"),
            "markdown": md,
        }
    return content


def main() -> int:
    if not REGISTRY.exists():
        print("Missing registry/skills.json", file=sys.stderr)
        return 1
    if not TEMPLATE.exists():
        print("Missing catalog/index.template.html", file=sys.stderr)
        return 1

    skills_data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills_list = skills_data.get("skills", [])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    DATA_DIR.mkdir(parents=True, exist_ok=True)

    shutil.copy2(REGISTRY, DATA_DIR / "skills.json")
    if BUNDLES.exists():
        shutil.copy2(BUNDLES, DATA_DIR / "bundles.json")
    if QUALITY.exists():
        shutil.copy2(QUALITY, DATA_DIR / "quality.json")
        qdata = json.loads(QUALITY.read_text(encoding="utf-8"))
        quality_map = {r["id"]: r["score"] for r in qdata.get("skills", [])}
        (DATA_DIR / "quality-map.json").write_text(
            json.dumps(quality_map, ensure_ascii=False), encoding="utf-8"
        )

    skill_content = generate_skill_content(skills_list)
    (DATA_DIR / "skill-content.json").write_text(
        json.dumps(skill_content, ensure_ascii=False),
        encoding="utf-8",
    )

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("178 skills", f"{skills_data['count']} skills")
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    (OUT_DIR / ".nojekyll").touch()

    if not ASSETS_SRC.is_dir():
        print("Warning: catalog/assets/ missing", file=sys.stderr)

    print(
        f"Wrote {OUT_DIR / 'index.html'} ({skills_data['count']} skills, "
        f"{len(skill_content)} previews)"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
