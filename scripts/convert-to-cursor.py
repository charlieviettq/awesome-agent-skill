#!/usr/bin/env python3
"""
Sync Claude-format skills (.claude/skills/{flat}/) back to Cursor format (.cursor/skills/{nested}/).

Uses scripts/claude-skill-map.json for path mapping. Preserves Cursor-only frontmatter
(triggers, version, tools, mutating, priority, source) when present.

Usage:
  python3 scripts/convert-to-cursor.py --in-repo [--dry-run] [--force] [--only-newer]
  python3 scripts/convert-to-cursor.py --in-repo --write-body-only
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any

from skill_format import (
    CLAUDE_ONLY_KEYS,
    CURSOR_PRESERVE_KEYS,
    copy_skill_assets,
    generate_triggers,
    load_map,
    parse_frontmatter,
    yaml_dump_simple,
)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_DIR = SCRIPT_DIR.parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"


def merge_cursor_frontmatter(
    claude_fm: dict[str, Any],
    cursor_fm: dict[str, Any],
    cursor_path: str,
    write_body_only: bool,
) -> dict[str, Any]:
    leaf = Path(cursor_path).name
    name = str(cursor_fm.get("name") or claude_fm.get("name") or leaf)
    description = str(claude_fm.get("description") or cursor_fm.get("description") or "")
    arg_hint = str(claude_fm.get("argument-hint") or cursor_fm.get("argument-hint") or "").strip()

    out: dict[str, Any] = {
        "name": name,
        "version": cursor_fm.get("version") or 1,
        "description": description,
    }

    if arg_hint:
        out["argument-hint"] = arg_hint

    triggers = cursor_fm.get("triggers")
    if isinstance(triggers, list) and triggers:
        out["triggers"] = triggers
    elif not write_body_only:
        out["triggers"] = generate_triggers(name, description, arg_hint)

    for key in ("tools", "mutating", "priority", "source"):
        if key in cursor_fm and cursor_fm[key] not in (None, ""):
            out[key] = cursor_fm[key]
        elif key == "tools" and not write_body_only:
            out["tools"] = []
        elif key == "mutating" and not write_body_only:
            out["mutating"] = False
        elif key == "priority" and not write_body_only:
            out["priority"] = "normal"

    if write_body_only:
        for key in CURSOR_PRESERVE_KEYS:
            if key in cursor_fm:
                out[key] = cursor_fm[key]

    for key in CLAUDE_ONLY_KEYS:
        out.pop(key, None)

    return out


def should_skip(
    claude_skill_md: Path,
    cursor_skill_md: Path,
    only_newer: bool,
    force: bool,
) -> bool:
    if not cursor_skill_md.is_file():
        return False
    if force:
        return False
    if only_newer:
        return claude_skill_md.stat().st_mtime <= cursor_skill_md.stat().st_mtime
    return True


def sync_skill(
    mapping: dict[str, str],
    claude_root: Path,
    cursor_root: Path,
    dry_run: bool,
    force: bool,
    only_newer: bool,
    write_body_only: bool,
) -> str:
    cursor_path = mapping["cursor_path"]
    claude_name = mapping["claude_name"]

    claude_dir = claude_root / claude_name
    claude_md = claude_dir / "SKILL.md"
    if not claude_md.is_file():
        return f"SKIP missing claude: {claude_name}"

    cursor_dir = cursor_root / cursor_path
    cursor_md = cursor_dir / "SKILL.md"

    if should_skip(claude_md, cursor_md, only_newer, force):
        return f"SKIP up-to-date: {cursor_path}"

    claude_content = claude_md.read_text(encoding="utf-8")
    claude_fm, claude_body = parse_frontmatter(claude_content)

    cursor_fm: dict[str, Any] = {}
    if cursor_md.is_file():
        cursor_content = cursor_md.read_text(encoding="utf-8")
        cursor_fm, _ = parse_frontmatter(cursor_content)

    merged_fm = merge_cursor_frontmatter(
        claude_fm, cursor_fm, cursor_path, write_body_only
    )
    body = claude_body.lstrip("\n")
    new_content = yaml_dump_simple(merged_fm) + "\n\n" + body

    if dry_run:
        return f"OK {claude_name} -> {cursor_path}"

    cursor_dir.mkdir(parents=True, exist_ok=True)
    copy_skill_assets(claude_dir, cursor_dir, dry_run=False)
    cursor_md.write_text(new_content, encoding="utf-8")
    return f"OK {claude_name} -> {cursor_path}"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Sync Claude flat skills back to Cursor nested paths via map"
    )
    parser.add_argument(
        "--repo-dir",
        default=str(DEFAULT_REPO_DIR),
        help="Repository root",
    )
    parser.add_argument(
        "--in-repo",
        action="store_true",
        help="Use repo .cursor/skills and .claude/skills",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite even if Cursor is newer")
    parser.add_argument(
        "--only-newer",
        action="store_true",
        help="Only update when Claude SKILL.md is newer than Cursor",
    )
    parser.add_argument(
        "--write-body-only",
        action="store_true",
        help="Only replace body; keep all existing Cursor frontmatter",
    )
    parser.add_argument("--map-file", default=str(MAP_FILE))
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    cursor_root = repo_dir / ".cursor" / "skills"
    claude_root = repo_dir / ".claude" / "skills"

    if not cursor_root.is_dir():
        print(f"ERROR: {cursor_root} not found", file=sys.stderr)
        return 1
    if not claude_root.is_dir():
        print(f"ERROR: {claude_root} not found", file=sys.stderr)
        return 1

    map_file = Path(args.map_file)
    if not map_file.is_file():
        print(f"ERROR: {map_file} not found", file=sys.stderr)
        return 1

    mappings = load_map(map_file)
    print(f"Mappings: {len(mappings)}")

    ok = 0
    skipped = 0
    errors: list[str] = []
    for m in mappings:
        try:
            msg = sync_skill(
                m,
                claude_root,
                cursor_root,
                args.dry_run,
                args.force,
                args.only_newer,
                args.write_body_only,
            )
            print(msg)
            if msg.startswith("SKIP"):
                skipped += 1
            else:
                ok += 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{m.get('cursor_path')}: {exc}")

    print(f"\nSynced: {ok}, skipped: {skipped}, total: {len(mappings)}")
    if errors:
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    if not args.dry_run:
        print(f"\nOutput: {cursor_root}")
        print("Reload Cursor to pick up updated skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
