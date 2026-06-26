#!/usr/bin/env python3
"""
Remove nested orphan directories under .claude/skills/ that are not flat map targets.

Usage:
  python3 scripts/prune_claude_skills.py [--dry-run] [--repo-dir PATH]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from skill_format import flat_claude_names, load_map

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_DIR = SCRIPT_DIR.parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"


def prune_orphans_v2(
    claude_skills_root: Path,
    mappings: list[dict[str, str]],
    dry_run: bool = False,
) -> int:
    """Remove any path under claude_skills_root that is not an allowed flat claude_name dir."""
    allowed_flat = flat_claude_names(mappings)
    removed = 0

    for child in sorted(claude_skills_root.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if name in allowed_flat:
            # Ensure no nested SKILL.md inside flat dir except at root of that dir
            nested_dirs = {
                nested_md.parent
                for nested_md in child.rglob("SKILL.md")
                if nested_md.parent != child
            }
            for nested_dir in sorted(nested_dirs, key=lambda p: len(p.parts), reverse=True):
                if not nested_dir.exists():
                    continue
                rel = nested_dir.relative_to(child).as_posix()
                if dry_run:
                    print(f"DRY-RUN remove nested under flat {name}: {rel}")
                else:
                    shutil.rmtree(nested_dir)
                    print(f"Removed nested under flat {name}: {rel}")
                removed += 1
            continue

        if dry_run:
            print(f"DRY-RUN remove: {name}/")
        else:
            shutil.rmtree(child)
            print(f"Removed: {name}/")
        removed += 1

    return removed


def main() -> int:
    parser = argparse.ArgumentParser(description="Prune orphan nested Claude skill directories")
    parser.add_argument("--repo-dir", default=str(DEFAULT_REPO_DIR))
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--map-file", default=str(MAP_FILE))
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    claude_root = repo_dir / ".claude" / "skills"
    if not claude_root.is_dir():
        print(f"ERROR: {claude_root} not found", file=sys.stderr)
        return 1

    map_file = Path(args.map_file)
    if not map_file.is_file():
        print(f"ERROR: {map_file} not found", file=sys.stderr)
        return 1

    mappings = load_map(map_file)
    removed = prune_orphans_v2(claude_root, mappings, dry_run=args.dry_run)
    print(f"\nPruned {removed} path(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
