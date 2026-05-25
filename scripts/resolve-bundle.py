#!/usr/bin/env python3
"""Print bundle install plan: domains and explicit skill ids (one per line, prefixed)."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLES_JSON = ROOT / "registry" / "bundles.json"
CURSOR_ROOT = ROOT / ".cursor" / "skills"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: resolve-bundle.py <bundle-id>", file=sys.stderr)
        return 1
    bundle_id = sys.argv[1]
    data = json.loads(BUNDLES_JSON.read_text(encoding="utf-8"))
    bundle = next((b for b in data["bundles"] if b["id"] == bundle_id), None)
    if bundle is None:
        print(f"Unknown bundle: {bundle_id}", file=sys.stderr)
        return 1

    if bundle.get("install_all_domains"):
        for d in sorted(p.name for p in CURSOR_ROOT.iterdir() if p.is_dir()):
            print(f"domain:{d}")
        return 0

    for dom in bundle.get("domains", []):
        print(f"domain:{dom}")
    for sid in bundle.get("skills", []):
        print(f"skill:{sid}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
