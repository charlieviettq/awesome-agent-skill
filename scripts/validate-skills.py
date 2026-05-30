#!/usr/bin/env python3
"""Validate SKILL.md structure for awesome-agent-skill."""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
MAP_FILE = SCRIPT_DIR / "claude-skill-map.json"

ROOT = Path(__file__).resolve().parents[1]
CURSOR_ROOT = ROOT / ".cursor" / "skills"
CLAUDE_ROOT = ROOT / ".claude" / "skills"

SKIP_NAME_MISMATCH = {
    CURSOR_ROOT / "voltagent" / "SKILL.md": "voltagent-subagents",
}


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end]
    body = text[end + 4 :]
    fm: dict[str, str] = {}
    key: str | None = None
    buf: list[str] = []
    for line in raw.splitlines():
        if re.match(r"^[a-zA-Z0-9_-]+:\s*", line) and not line.startswith(" "):
            if key is not None:
                fm[key] = "\n".join(buf).strip().strip('"').strip("'")
            key, _, val = line.partition(":")
            key = key.strip()
            buf = [val.strip()]
        elif key is not None:
            buf.append(line)
    if key is not None:
        fm[key] = "\n".join(buf).strip().strip('"').strip("'")
    return fm, body


def rel_cursor_path(path: Path) -> str:
    return str(path.relative_to(CURSOR_ROOT))


ENFORCED_TRIGGER_DOMAINS = {
    "core-workflow",
    "frontend-engineering",
    "ai-agent-systems",
    "reliability-ops",
    "security-appsec",
    "mobile",
    "marketing",
    "architecture",
    "product-growth",
    "performance",
}

KNOWN_DUPLICATE_NAMES = {
    "reflect-yourself",
    "phase-kickoff",
    # knowledge-work plugins reuse leaf names across plugins; paths are unique
    "statistical-analysis",
    "start",
    "competitive-brief",
}


def has_trigger_hints(description: str) -> bool:
    return bool(
        re.search(
            r"(Triggers:|Use when|Use this skill when|Use for|Voice triggers)",
            description,
            flags=re.I,
        )
    )


def should_enforce_triggers(path: Path) -> bool:
    rel = rel_cursor_path(path)
    top = rel.split("/", 1)[0]
    return top in ENFORCED_TRIGGER_DOMAINS


def collect_markdown_links(text: str) -> list[str]:
    return re.findall(r"\]\(([^)]+)\)", text)


def validate_cursor_skills() -> list[str]:
    errors: list[str] = []
    names: dict[str, list[Path]] = defaultdict(list)

    for path in sorted(CURSOR_ROOT.rglob("SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{path}: missing frontmatter")
            continue

        fm, _body = parse_frontmatter(text)
        name = fm.get("name", "").strip()
        description = fm.get("description", "")

        if not name:
            errors.append(f"{path}: missing name in frontmatter")
            continue

        expected = path.parent.name
        if name != expected and path not in SKIP_NAME_MISMATCH:
            errors.append(f"{path}: name '{name}' != folder '{expected}'")

        if should_enforce_triggers(path) and not has_trigger_hints(description):
            errors.append(f"{path}: description missing trigger hints (Triggers:/Use when)")

        names[name].append(path)

        for link in collect_markdown_links(text):
            if link.startswith(("http://", "https://", "#", "mailto:")):
                continue
            target = (path.parent / link).resolve()
            if not target.exists():
                errors.append(f"{path}: broken relative link -> {link}")

    for name, paths in names.items():
        if name in KNOWN_DUPLICATE_NAMES:
            continue
        if len(paths) > 1:
            joined = ", ".join(str(p.relative_to(ROOT)) for p in paths)
            errors.append(f"duplicate skill name '{name}': {joined}")

    return errors


def validate_claude_frontmatter() -> list[str]:
    errors: list[str] = []
    for path in sorted(CLAUDE_ROOT.rglob("SKILL.md")):
        text = path.read_text(encoding="utf-8")
        if not text.startswith("---"):
            errors.append(f"{path}: missing frontmatter")
    return errors


def check_map_parity(strict_orphans: bool) -> list[str]:
    """Check claude-skill-map.json against on-disk Cursor and Claude flat skills."""
    issues: list[str] = []
    if not MAP_FILE.is_file():
        return issues

    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    mappings = data.get("mappings", [])
    allowed_flat = {m["claude_name"] for m in mappings}

    for m in mappings:
        cpath = CURSOR_ROOT / m["cursor_path"] / "SKILL.md"
        if not cpath.is_file():
            issues.append(f"map parity: missing Cursor file for {m['cursor_path']}")
        claude_md = CLAUDE_ROOT / m["claude_name"] / "SKILL.md"
        if not claude_md.is_file():
            issues.append(f"map parity: missing Claude flat for {m['claude_name']}")

    if CLAUDE_ROOT.is_dir():
        for child in sorted(CLAUDE_ROOT.iterdir()):
            if child.is_dir() and child.name not in allowed_flat:
                msg = f"map parity: Claude orphan directory {child.name}/ (run prune_claude_skills.py)"
                if strict_orphans:
                    issues.append(msg)
                else:
                    print(f"WARNING: {msg}", file=sys.stderr)

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md structure")
    parser.add_argument(
        "--parity",
        action="store_true",
        help="Also check claude-skill-map.json vs on-disk skills",
    )
    parser.add_argument(
        "--strict-orphans",
        action="store_true",
        help="With --parity, fail on nested Claude orphan directories",
    )
    args = parser.parse_args()

    errors = validate_cursor_skills() + validate_claude_frontmatter()
    if args.parity:
        errors.extend(check_map_parity(strict_orphans=args.strict_orphans))

    cursor_count = len(list(CURSOR_ROOT.rglob("SKILL.md")))
    claude_count = len(list(CLAUDE_ROOT.rglob("SKILL.md")))

    if errors:
        print("Skill validation failed:\n", file=sys.stderr)
        for err in errors:
            print(f"  - {err}", file=sys.stderr)
        return 1

    print(f"Validated {cursor_count} Cursor skills and {claude_count} Claude skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
