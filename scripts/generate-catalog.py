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
OUT_DIR = ROOT / "catalog"
DATA_DIR = OUT_DIR / "data"
ASSETS_SRC = OUT_DIR / "assets"
TEMPLATE = OUT_DIR / "index.template.html"


def main() -> int:
    if not REGISTRY.exists():
        print("Missing registry/skills.json", file=sys.stderr)
        return 1
    if not TEMPLATE.exists():
        print("Missing catalog/index.template.html", file=sys.stderr)
        return 1

    skills_data = json.loads(REGISTRY.read_text(encoding="utf-8"))
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

    html = TEMPLATE.read_text(encoding="utf-8")
    html = html.replace("178 skills", f"{skills_data['count']} skills")
    (OUT_DIR / "index.html").write_text(html, encoding="utf-8")
    (OUT_DIR / ".nojekyll").touch()

    if not ASSETS_SRC.is_dir():
        print("Warning: catalog/assets/ missing", file=sys.stderr)

    print(f"Wrote {OUT_DIR / 'index.html'} ({skills_data['count']} skills)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
