#!/usr/bin/env python3
"""
Report parity between Cursor skills, Claude flat skills, and claude-skill-map.json.

Usage:
  python3 scripts/audit-skill-parity.py [--json]
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from skill_format import discover_skills, flat_claude_names, load_map

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_DIR = SCRIPT_DIR.parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit Cursor vs Claude skill parity")
    parser.add_argument("--repo-dir", default=str(DEFAULT_REPO_DIR))
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--map-file", default=str(MAP_FILE))
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    cursor_root = repo_dir / ".cursor" / "skills"
    claude_root = repo_dir / ".claude" / "skills"
    map_file = Path(args.map_file)

    if not map_file.is_file():
        print(f"ERROR: {map_file} missing", file=sys.stderr)
        return 1

    mappings = load_map(map_file)
    allowed_flat = flat_claude_names(mappings)

    cursor_paths = {
        p.parent.relative_to(cursor_root).as_posix()
        for p in discover_skills(cursor_root)
    }

    map_cursor = {m["cursor_path"] for m in mappings}
    missing_cursor_files = [
        m["cursor_path"]
        for m in mappings
        if not (cursor_root / m["cursor_path"] / "SKILL.md").is_file()
    ]
    missing_claude_flat = [
        m["claude_name"]
        for m in mappings
        if not (claude_root / m["claude_name"] / "SKILL.md").is_file()
    ]

    claude_nested_orphans: list[str] = []
    claude_flat_extra: list[str] = []
    if claude_root.is_dir():
        for child in sorted(claude_root.iterdir()):
            if not child.is_dir():
                continue
            if child.name not in allowed_flat:
                claude_nested_orphans.append(child.name + "/")
            elif (child / "SKILL.md").is_file():
                for nested in child.rglob("SKILL.md"):
                    rel = nested.parent.relative_to(child).as_posix()
                    if rel != ".":
                        claude_nested_orphans.append(f"{child.name}/{rel}")
            else:
                claude_flat_extra.append(child.name)

        for skill_md in claude_root.rglob("SKILL.md"):
            rel = skill_md.parent.relative_to(claude_root).as_posix()
            if "/" in rel and rel.split("/")[0] not in allowed_flat:
                if rel.split("/")[0] + "/" not in claude_nested_orphans:
                    claude_nested_orphans.append(rel.split("/")[0] + "/")

    unmapped_cursor = sorted(cursor_paths - map_cursor)

    report = {
        "mapping_count": len(mappings),
        "cursor_skill_count": len(cursor_paths),
        "claude_flat_in_map": len(allowed_flat),
        "missing_cursor_files": missing_cursor_files,
        "missing_claude_flat_files": missing_claude_flat,
        "claude_orphan_top_level_dirs": sorted(set(claude_nested_orphans)),
        "cursor_paths_not_in_map": unmapped_cursor[:20],
        "cursor_paths_not_in_map_count": len(unmapped_cursor),
        "suggested_commands": [],
    }

    if missing_cursor_files:
        report["suggested_commands"].append("python3 scripts/import-plugins.py")
        report["suggested_commands"].append(
            "python3 scripts/convert-to-cursor.py --in-repo --force"
        )
    if missing_claude_flat:
        report["suggested_commands"].append(
            "python3 scripts/convert-to-claude.py --in-repo --force --write-map"
        )
    if claude_nested_orphans:
        report["suggested_commands"].append(
            "python3 scripts/prune_claude_skills.py --dry-run"
        )
        report["suggested_commands"].append(
            "python3 scripts/convert-to-claude.py --in-repo --force --prune-orphans"
        )

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print("Skill parity audit")
        print(f"  Map entries:              {report['mapping_count']}")
        print(f"  Cursor skills:            {report['cursor_skill_count']}")
        print(f"  Missing Cursor files:     {len(missing_cursor_files)}")
        print(f"  Missing Claude flat:      {len(missing_claude_flat)}")
        print(f"  Claude orphan dirs:       {len(report['claude_orphan_top_level_dirs'])}")
        print(f"  Cursor paths not in map:  {report['cursor_paths_not_in_map_count']}")
        if missing_cursor_files:
            print("\nMissing Cursor (sample):", missing_cursor_files[:5])
        if missing_claude_flat:
            print("Missing Claude flat (sample):", missing_claude_flat[:5])
        if report["claude_orphan_top_level_dirs"]:
            print("Claude orphans (sample):", report["claude_orphan_top_level_dirs"][:8])
        if report["suggested_commands"]:
            print("\nSuggested:")
            for cmd in report["suggested_commands"]:
                print(f"  {cmd}")

    has_issues = bool(
        missing_cursor_files
        or missing_claude_flat
        or report["claude_orphan_top_level_dirs"]
    )
    return 1 if has_issues else 0


if __name__ == "__main__":
    sys.exit(main())
