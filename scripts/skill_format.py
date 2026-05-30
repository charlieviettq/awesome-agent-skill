"""Shared skill frontmatter parsing, asset copy, and trigger helpers."""

from __future__ import annotations

import re
import shutil
from pathlib import Path
from typing import Any

COPY_DIRS = ("references", "scripts", "assets", "commands", "tests")
COPY_FILES = ("reference.md", "LICENSE.txt", "LICENSE", "forms.md", "config.yaml")
SKIP_PATH_PARTS = {".git", ".DS_Store", "__pycache__", "node_modules"}

CURSOR_PRESERVE_KEYS = frozenset(
    {
        "triggers",
        "version",
        "tools",
        "mutating",
        "priority",
        "source",
    }
)

CLAUDE_ONLY_KEYS = frozenset(
    {
        "allowed-tools",
        "user-invocable",
    }
)


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
        elif current_key == "triggers" and text:
            items: list[str] = []
            for line in text.splitlines():
                line = line.strip()
                if line.startswith("- "):
                    item = line[2:].strip().strip('"').strip("'")
                    if item:
                        items.append(item)
            fm[current_key] = items
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


def generate_triggers(name: str, description: str, argument_hint: str = "") -> list[str]:
    triggers: list[str] = []
    slug = name.replace("_", "-")
    triggers.append(slug)
    triggers.append(f"/{slug}")

    if argument_hint:
        hint = argument_hint.strip("<>\"' ")
        if hint and hint not in triggers:
            triggers.append(hint)

    desc = description.replace("\n", " ")
    first = desc.split(".")[0] if desc else ""
    for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]{2,}", first):
        low = token.lower()
        if low in {"use", "when", "the", "and", "for", "with", "this", "that", "from", "into"}:
            continue
        phrase = low.replace("_", " ")
        if phrase not in triggers and len(triggers) < 8:
            triggers.append(phrase)

    seen: set[str] = set()
    out: list[str] = []
    for t in triggers:
        k = t.lower()
        if k not in seen:
            seen.add(k)
            out.append(t)
    return out[:8]


def yaml_dump_simple(data: dict[str, Any]) -> str:
    lines = ["---"]
    for key, val in data.items():
        if key == "triggers" and isinstance(val, list):
            lines.append("triggers:")
            for item in val:
                s = str(item).replace('"', '\\"')
                lines.append(f'  - "{s}"')
        elif isinstance(val, bool):
            lines.append(f"{key}: {'true' if val else 'false'}")
        elif isinstance(val, list):
            lines.append(f"{key}:")
            for item in val:
                lines.append(f"  - {item}")
        else:
            s = str(val)
            if "\n" in s:
                lines.append(f"{key}: >")
                for line in s.splitlines():
                    lines.append(f"  {line}")
            elif ":" in s or s.startswith('"') or len(s) > 80:
                s = s.replace('"', '\\"')
                lines.append(f'{key}: "{s}"')
            else:
                lines.append(f"{key}: {s}")
    lines.append("---")
    return "\n".join(lines)


def strip_related_skills(body: str) -> str:
    pattern = re.compile(
        r"\n## Related skills\b.*",
        re.IGNORECASE | re.DOTALL,
    )
    return pattern.sub("", body).rstrip() + "\n"


def cursor_path_from_skill_md(skill_md: Path, skills_root: Path) -> str:
    rel = skill_md.parent.relative_to(skills_root)
    return rel.as_posix()


def discover_skills(skills_root: Path) -> list[Path]:
    skip_suffixes = ("/skill-examples/", "/tests/", "/node_modules/")
    found: list[Path] = []
    for skill_md in sorted(skills_root.rglob("SKILL.md")):
        rel = skill_md.parent.relative_to(skills_root).as_posix()
        if any(part in rel for part in skip_suffixes):
            continue
        if rel == "meta-tools/reflect-yourself" and (
            skills_root / "reflect-yourself" / "SKILL.md"
        ).is_file():
            continue
        found.append(skill_md)
    return found


def copy_skill_assets(src: Path, dest: Path, dry_run: bool = False) -> None:
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


def load_map(map_file: Path) -> list[dict[str, str]]:
    import json

    data = json.loads(map_file.read_text(encoding="utf-8"))
    return data.get("mappings", [])


def flat_claude_names(mappings: list[dict[str, str]]) -> set[str]:
    return {m["claude_name"] for m in mappings}
