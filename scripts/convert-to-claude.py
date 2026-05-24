#!/usr/bin/env python3
"""
Convert Cursor-format skills (data-science-skills/.cursor/skills/) to Claude Code format
(.claude/skills/).

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

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_REPO_DIR = SCRIPT_DIR.parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"

COPY_DIRS = ("references", "scripts", "assets", "commands", "tests")
COPY_FILES = ("reference.md", "LICENSE.txt", "LICENSE", "forms.md", "config.yaml")

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

SKIP_PATH_PARTS = {".git", ".DS_Store", "__pycache__", "node_modules"}


def parse_frontmatter(content: str) -> tuple[dict[str, Any], str]:
    if not content.startswith("---"):
        return {}, content
    end = content.find("\n---", 3)
    if end == -1:
        return {}, content
    raw_fm = content[3:end].strip()
    body = content[end + 4 :].lstrip("\n")
    fm: dict[str, Any] = {}
    current_key: str | None = None
    current_lines: list[str] = []

    def flush() -> None:
        nonlocal current_key, current_lines
        if current_key is None:
            return
        text = "\n".join(current_lines).strip()
        if current_key == "metadata" and text:
            meta: dict[str, Any] = {}
            for line in text.splitlines():
                line = line.strip()
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip()] = v.strip().strip('"')
            fm[current_key] = meta
        elif current_key == "description" and text.startswith(">"):
            fm[current_key] = re.sub(r"^\s*>\s?", "", text, flags=re.MULTILINE).strip()
        else:
            fm[current_key] = text
        current_key = None
        current_lines = []

    for line in raw_fm.splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:\s*", line) and not line.startswith(" "):
            flush()
            key, _, val = line.partition(":")
            current_key = key.strip()
            val = val.strip()
            if val == ">":
                current_lines = []
            elif val:
                current_lines = [val]
            else:
                current_lines = []
        else:
            current_lines.append(line)
    flush()
    return fm, body


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

    # No structured tags — keep full description, strip only trailing metadata phrases
    text = re.sub(r"\[PROACTIVE\]:[^.]*\.?", "", text, flags=re.IGNORECASE)
    text = re.sub(r'Triggers:\s*"[^"]*"(,\s*"[^"]*")*', "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+\.\s*$", ".", text)
    text = re.sub(r"\.{2,}", ".", text)
    if text and not text.endswith("."):
        text += "."
    return text


def strip_related_skills(body: str) -> str:
    pattern = re.compile(
        r"\n## Related skills\b.*",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub("", body).rstrip() + "\n"


def cursor_path_from_skill_md(skill_md: Path, skills_root: Path) -> str:
    rel = skill_md.parent.relative_to(skills_root)
    return rel.as_posix()


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
        # Browser/ship skills need write; plan-review mostly read
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

    return out


def yaml_dump_simple(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, val in data.items():
        if isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        else:
            s = str(val).replace("\n", " ")
            if ":" in s or s.startswith('"') or len(s) > 80:
                s = s.replace('"', '\\"')
                lines.append(f'{key}: "{s}"')
            else:
                lines.append(f"{key}: {s}")
    lines.append("---")
    return "\n".join(lines)


def discover_skills(skills_root: Path) -> list[Path]:
    skip_suffixes = ("/skill-examples/", "/tests/", "/node_modules/")
    found: list[Path] = []
    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        rel = skill_md.parent.relative_to(skills_root).as_posix()
        if any(part in rel for part in skip_suffixes):
            continue
        if rel == "meta-tools/reflect-yourself" and (skills_root / "reflect-yourself" / "SKILL.md").is_file():
            continue
        found.append(skill_md)
    return found


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
            # Disambiguate with parent segment
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


def copy_skill_assets(src: Path, dest: Path, dry_run: bool) -> None:
    if dry_run:
        return
    dest.mkdir(parents=True, exist_ok=True)

    for name in COPY_FILES:
        src_file = src / name
        if src_file.is_file():
            shutil.copy2(src_file, dest / name)

    for dirname in COPY_DIRS:
        src_dir = src / dirname
        if src_dir.is_dir():
            shutil.copytree(src_dir, dest / dirname, dirs_exist_ok=True)

    # Copy office/docx nested trees not under standard dirs
    skip_names = {"SKILL.md", *COPY_DIRS, *COPY_FILES}
    for item in src.iterdir():
        if item.name in skip_names:
            continue
        if item.name in SKIP_PATH_PARTS:
            continue
        if item.is_file() and item.suffix in {".md", ".txt", ".json", ".yaml", ".yml"}:
            shutil.copy2(item, dest / item.name)
        elif item.is_dir() and item.name not in SKIP_PATH_PARTS:
            if not (dest / item.name).exists():
                shutil.copytree(
                    item,
                    dest / item.name,
                    dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(".git", "__pycache__", "node_modules"),
                )


def convert_skill(
    skills_root: Path,
    mapping: dict[str, str],
    claude_skills_root: Path,
    dry_run: bool,
    force: bool,
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
    args = parser.parse_args()

    repo_dir = Path(args.repo_dir).resolve()
    # Source: .cursor/skills/ (new layout) or skills/ (legacy fallback)
    skills_root = repo_dir / ".cursor" / "skills"
    if not skills_root.is_dir():
        skills_root = repo_dir / "skills"
    if not skills_root.is_dir():
        print(f"ERROR: skills root not found: {repo_dir / '.cursor' / 'skills'} or {repo_dir / 'skills'}", file=sys.stderr)
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
            msg = convert_skill(
                skills_root, m, claude_skills_root, args.dry_run, args.force
            )
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
        print("Restart Claude Code session to load new skills.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
