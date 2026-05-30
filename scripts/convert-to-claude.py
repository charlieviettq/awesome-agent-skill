#!/usr/bin/env python3
"""
Convert Cursor-format skills (.cursor/skills/) to Claude Code format (.claude/skills/).

Usage:
  python3 scripts/convert-to-claude.py /path/to/project [--dry-run] [--force]
  python3 scripts/convert-to-claude.py /path/to/project --write-map
  python3 scripts/convert-to-claude.py --repo-dir /path/to/data-science-skills --write-map-only
  python3 scripts/convert-to-claude.py --in-repo             # convert into this repo's .claude/skills/
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path
from typing import Any

from skill_format import (
    copy_skill_assets,
    cursor_path_from_skill_md,
    discover_skills,
    parse_frontmatter,
    strip_related_skills,
    yaml_dump_simple,
)

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_DIR = SCRIPT_DIR.parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"

READ_ONLY_TOOLS = "Read, Glob, Grep"
WRITE_TOOLS = "Bash, Read, Write, Edit, Glob, Grep"

AUTO_USER_INVOCABLE_FALSE = frozenset(
    {
        "ds-modeling-credit",
        "ds-modeling-credit-automl-py",
        "ds-notebooks",
        "ds-partner-boundaries",
        "python-style-legacy",
    }
)


def flatten_description(desc: str) -> str:
    if not desc:
        return ""
    text = re.sub(r"\s+", " ", desc.strip())

    what_m = re.search(r"\[WHAT\]:\s*([^.\[]+)", text, re.IGNORECASE)
    when_m = re.search(r"\[WHEN\]:\s*([^.\[]+)", text, re.IGNORECASE)
    if what_m or when_m:
        parts: list[str] = []
        if what_m:
            parts.append(what_m.group(1).strip().rstrip("."))
        if when_m:
            when = when_m.group(1).strip().rstrip(".")
            if when.lower().startswith("use when"):
                parts.append(when)
            else:
                parts.append(f"Use when {when[0].lower()}{when[1:]}" if when else "")
        result = ". ".join(p for p in parts if p)
        if not result.endswith("."):
            result += "."
        return result

    text = re.sub(r"\[PROACTIVE\]:[^.]*\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r'Triggers:\s*"[^"]*"(,\s*"[^"]*")*', "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+\.\s*$", ".", text)
    text = re.sub(r"\.{2,}", ".", text)
    if text and not text.endswith("."):
        text += "."
    return text


def propose_claude_name(cursor_path: str, fm_name: str | None) -> str:
    parts = cursor_path.split("/")
    leaf = parts[-1] if parts else cursor_path

    if cursor_path.startswith("gstack/"):
        if leaf == "gstack" and len(parts) == 1:
            return "gstack"
        if leaf.startswith("gstack-"):
            return f"gstack-{leaf}"
        return f"gstack-{leaf}"

    if cursor_path.startswith("voltagent/"):
        if leaf.startswith("va-"):
            return leaf
        return f"va-{leaf}"

    if cursor_path.startswith("private/"):
        return f"private/{leaf}"

    if fm_name and re.match(r"^[a-z0-9][a-z0-9_-]*$", fm_name):
        return fm_name

    return leaf


def has_scripts(skill_dir: Path) -> bool:
    scripts = skill_dir / "scripts"
    if scripts.is_dir():
        return any(scripts.rglob("*.py")) or any(scripts.rglob("*.sh"))
    return False


def build_allowed_tools(skill_dir: Path, claude_name: str) -> str:
    if has_scripts(skill_dir):
        return WRITE_TOOLS
    gstack_write = {
        "gstack-ship",
        "gstack-land-and-deploy",
        "gstack-scrape",
        "gstack-skillify",
        "gstack-design-html",
        "gstack-qa",
        "gstack-freeze",
        "gstack-guard",
        "gstack-unfreeze",
        "gstack-codex",
        "gstack-health",
        "gstack-investigate",
        "gstack-review",
        "gstack-browse",
        "gstack-canary",
        "gstack-benchmark",
        "gstack-open-gstack-browser",
        "gstack-setup-browser-cookies",
        "gstack-gstack-upgrade",
        "gstack-document-release",
        "gstack-setup-deploy",
        "gstack-cso",
        "gstack-autoplan",
    }
    if claude_name in gstack_write or claude_name.startswith("gstack-"):
        read_only_gstack = {
            "gstack-plan-ceo-review",
            "gstack-plan-eng-review",
            "gstack-plan-design-review",
            "gstack-plan-devex-review",
            "gstack-devex-review",
            "gstack-plan-tune",
            "gstack-office-hours",
            "gstack-learn",
            "gstack-context-save",
            "gstack-context-restore",
            "gstack-landing-report",
            "gstack-qa-only",
            "gstack-benchmark-models",
            "gstack-hackernews-frontpage",
        }
        if claude_name not in read_only_gstack:
            return WRITE_TOOLS
    return READ_ONLY_TOOLS


def render_claude_frontmatter(
    fm: dict[str, Any],
    claude_name: str,
    skill_dir: Path,
) -> dict[str, Any]:
    name = str(fm.get("name") or claude_name)
    desc = flatten_description(str(fm.get("description") or ""))
    if not desc:
        desc = f"Skill {claude_name}."

    out: dict[str, Any] = {
        "name": name,
        "description": desc,
        "allowed-tools": build_allowed_tools(skill_dir, claude_name),
    }

    user_invocable = fm.get("user-invocable")
    if user_invocable is not None:
        out["user-invocable"] = user_invocable
    elif claude_name in AUTO_USER_INVOCABLE_FALSE:
        out["user-invocable"] = False

    if fm.get("allowed-tools"):
        out["allowed-tools"] = fm["allowed-tools"]

    if fm.get("argument-hint"):
        out["argument-hint"] = str(fm["argument-hint"]).strip()

    return out


def build_mappings(skills_root: Path) -> list[dict[str, str]]:
    skill_mds = discover_skills(skills_root)
    used: dict[str, str] = {}
    mappings: list[dict[str, str]] = []

    for skill_md in skill_mds:
        cursor_path = cursor_path_from_skill_md(skill_md, skills_root)
        content = skill_md.read_text(encoding="utf-8")
        fm, _ = parse_frontmatter(content)
        fm_name = str(fm.get("name") or "") if fm.get("name") else None
        claude_name = propose_claude_name(cursor_path, fm_name)

        if claude_name in used and used[claude_name] != cursor_path:
            parts = cursor_path.split("/")
            if len(parts) >= 2:
                claude_name = f"{parts[-2]}-{parts[-1]}".replace("/", "-")
            if claude_name.startswith("gstack-") is False and cursor_path.startswith("gstack/"):
                claude_name = f"gstack-{claude_name}"
            if cursor_path.startswith("voltagent/") and not claude_name.startswith("va-"):
                claude_name = f"va-{claude_name}"

        if claude_name in used and used[claude_name] != cursor_path:
            claude_name = cursor_path.replace("/", "-")

        used[claude_name] = cursor_path
        mappings.append(
            {
                "cursor_path": cursor_path,
                "claude_name": claude_name,
                "source_name": fm_name or Path(cursor_path).name,
            }
        )

    return mappings


def load_or_build_map(skills_root: Path, write_map: bool) -> list[dict[str, str]]:
    if MAP_FILE.exists() and not write_map:
        data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
        return data.get("mappings", [])

    mappings = build_mappings(skills_root)
    if write_map or not MAP_FILE.exists():
        payload = {
            "version": 1,
            "generated_from": ".cursor/skills",
            "mappings": mappings,
        }
        MAP_FILE.write_text(
            json.dumps(payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    return mappings


def convert_skill(
    skills_root: Path,
    mapping: dict[str, str],
    claude_skills_root: Path,
    dry_run: bool,
) -> str:
    cursor_path = mapping["cursor_path"]
    claude_name = mapping["claude_name"]
    src_dir = skills_root / cursor_path
    skill_md = src_dir / "SKILL.md"
    if not skill_md.is_file():
        return f"SKIP missing: {cursor_path}"

    dest_dir = claude_skills_root / claude_name
    content = skill_md.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    body = strip_related_skills(body)

    claude_fm = render_claude_frontmatter(fm, claude_name, src_dir)
    new_content = yaml_dump_simple(claude_fm) + "\n\n" + body.lstrip("\n")

    if dry_run:
        return f"OK {cursor_path} -> {claude_name}/"

    dest_dir.mkdir(parents=True, exist_ok=True)
    copy_skill_assets(src_dir, dest_dir, dry_run=False)
    (dest_dir / "SKILL.md").write_text(new_content, encoding="utf-8")
    return f"OK {cursor_path} -> {claude_name}/"


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert Cursor skills to Claude Code format")
    parser.add_argument(
        "project_dir",
        nargs="?",
        help="Target project root (writes .claude/skills/)",
    )
    parser.add_argument(
        "--repo-dir",
        default=str(DEFAULT_REPO_DIR),
        help="data-science-skills repo root",
    )
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true", help="Overwrite existing Claude skills")
    parser.add_argument("--write-map", action="store_true", help="Regenerate claude-skill-map.json")
    parser.add_argument(
        "--write-map-only",
        action="store_true",
        help="Only regenerate mapping file, no convert",
    )
    parser.add_argument(
        "--in-repo",
        action="store_true",
        help="Convert into this repo's own .claude/skills/ (project_dir = repo_dir)",
    )
    parser.add_argument(
        "--prune-orphans",
        action="store_true",
        help="After convert, remove nested .claude/skills paths not in flat map",
    )
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    skills_root = repo_dir / ".cursor" / "skills"
    if not skills_root.is_dir():
        skills_root = repo_dir / "skills"
    if not skills_root.is_dir():
        print(
            f"ERROR: skills root not found: {repo_dir / '.cursor' / 'skills'} or {repo_dir / 'skills'}",
            file=sys.stderr,
        )
        return 1

    mappings = load_or_build_map(skills_root, write_map=args.write_map or args.write_map_only)
    print(f"Mappings: {len(mappings)} skills")
    if args.write_map_only:
        print(f"Wrote {MAP_FILE}")
        return 0

    if args.in_repo:
        args.project_dir = str(repo_dir)

    if not args.project_dir:
        parser.error("project_dir is required unless --write-map-only or --in-repo")

    project_dir = Path(args.project_dir).resolve()
    claude_skills_root = project_dir / ".claude" / "skills"

    if claude_skills_root.exists() and args.force and not args.dry_run:
        shutil.rmtree(claude_skills_root)
    claude_skills_root.mkdir(parents=True, exist_ok=True)

    ok = 0
    errors: list[str] = []
    for m in mappings:
        try:
            msg = convert_skill(skills_root, m, claude_skills_root, args.dry_run)
            print(msg)
            ok += 1
        except Exception as exc:  # noqa: BLE001
            errors.append(f"{m.get('cursor_path')}: {exc}")

    print(f"\nConverted: {ok}/{len(mappings)}")
    if errors:
        print("Errors:", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    if not args.dry_run:
        print(f"\nOutput: {claude_skills_root}")
        if args.prune_orphans:
            from prune_claude_skills import prune_orphans_v2

            removed = prune_orphans_v2(claude_skills_root, mappings, dry_run=False)
            print(f"Pruned {removed} orphan path(s)")
        print("Restart Claude Code session to load new skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
