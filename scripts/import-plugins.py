#!/usr/bin/env python3
"""
Import SKILL.md files from anthropics/knowledge-work-plugins into .cursor/skills/knowledge-work/.

Usage:
  python3 scripts/import-plugins.py [--dry-run] [--force]
  python3 scripts/import-plugins.py --plugins data,engineering
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

from skill_format import generate_triggers, parse_frontmatter

ROOT = Path(__file__).resolve().parents[1]
OUT_ROOT = ROOT / ".cursor" / "skills" / "knowledge-work"

GITHUB_API = "https://api.github.com/repos/anthropics/knowledge-work-plugins/contents"
GITHUB_RAW = "https://raw.githubusercontent.com/anthropics/knowledge-work-plugins/main"

PLUGINS = [
    "data",
    "engineering",
    "product-management",
    "productivity",
    "marketing",
    "sales",
    "finance",
    "legal",
    "customer-support",
    "bio-research",
    "cowork-plugin-management",
]

PLUGIN_TITLES = {
    "data": "Data",
    "engineering": "Engineering",
    "product-management": "Product Management",
    "productivity": "Productivity",
    "marketing": "Marketing",
    "sales": "Sales",
    "finance": "Finance",
    "legal": "Legal",
    "customer-support": "Customer Support",
    "bio-research": "Bio Research",
    "cowork-plugin-management": "Cowork Plugin Management",
}


def http_get(url: str) -> bytes:
    req = urllib.request.Request(
        url,
        headers={"Accept": "application/vnd.github+json", "User-Agent": "awesome-agent-skill-import"},
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def list_skill_dirs(plugin: str) -> list[str]:
    url = f"{GITHUB_API}/{plugin}/skills"
    raw = http_get(url)
    data = json.loads(raw.decode("utf-8"))
    if not isinstance(data, list):
        raise RuntimeError(f"Unexpected API response for {plugin}/skills")
    return sorted(item["name"] for item in data if item.get("type") == "dir")


def fetch_skill_md(plugin: str, skill: str) -> str:
    url = f"{GITHUB_RAW}/{plugin}/skills/{skill}/SKILL.md"
    return http_get(url).decode("utf-8")


def render_cursor_skill(
    plugin: str,
    fm: dict[str, str],
    body: str,
) -> str:
    name = fm.get("name", "unknown")
    desc = fm.get("description", "").strip()
    arg_hint = fm.get("argument-hint", "").strip()

    triggers = generate_triggers(name, desc, arg_hint)
    source = f"anthropics/knowledge-work-plugins/{plugin}"

    lines = [
        "---",
        f"name: {name}",
        "version: 1",
        f"description: {desc}" if "\n" not in desc else f"description: >\n  {desc.replace(chr(10), chr(10) + '  ')}",
        f"argument-hint: {arg_hint}" if arg_hint else None,
        "triggers:",
    ]
    for t in triggers:
        lines.append(f'  - "{t}"')
    lines.extend(
        [
            "tools: []",
            "mutating: false",
            "priority: normal",
            f'source: "{source}"',
            "---",
            "",
        ]
    )
    header = "\n".join(l for l in lines if l is not None)
    # Fix relative CONNECTORS links in body
    body = body.replace("../../CONNECTORS.md", f"../CONNECTORS-{plugin}.md")
    return header + body


def write_hub_skills(plugins_imported: list[str], dry_run: bool) -> None:
    hub = OUT_ROOT / "SKILL.md"
    lines = [
        "---",
        "name: knowledge-work",
        "version: 1",
        "description: >",
        "  Anthropic knowledge-work-plugins — passive skills for data, engineering,",
        "  product, sales, finance, legal, support, and research workflows.",
        "triggers:",
        '  - "knowledge work"',
        '  - "cowork plugin"',
        "tools: []",
        "mutating: false",
        "priority: normal",
        'source: "anthropics/knowledge-work-plugins"',
        "---",
        "",
        "# Knowledge Work (Anthropic plugins)",
        "",
        "Imported from [anthropics/knowledge-work-plugins](https://github.com/anthropics/knowledge-work-plugins) (MIT).",
        "",
        "## Plugins",
        "",
    ]
    for p in plugins_imported:
        title = PLUGIN_TITLES.get(p, p)
        lines.append(f"- **{title}** — `knowledge-work/{p}/`")
    lines.append("")
    lines.append("Install a plugin bundle via SkillHub: `knowledge-work-<plugin>` or `knowledge-work-all`.")
    lines.append("")
    content = "\n".join(lines)
    if dry_run:
        print(f"[dry-run] would write hub {hub}")
        return
    hub.parent.mkdir(parents=True, exist_ok=True)
    hub.write_text(content, encoding="utf-8")
    print(f"Wrote hub {hub}")


def import_plugin(plugin: str, dry_run: bool, force: bool) -> tuple[int, int, int]:
    added = skipped = errors = 0
    try:
        skills = list_skill_dirs(plugin)
    except urllib.error.HTTPError as e:
        print(f"ERROR {plugin}: cannot list skills ({e})", file=sys.stderr)
        return 0, 0, 1

    for skill in skills:
        dest = OUT_ROOT / plugin / skill / "SKILL.md"
        if dest.exists() and not force:
            skipped += 1
            continue
        try:
            raw = fetch_skill_md(plugin, skill)
        except urllib.error.HTTPError as e:
            print(f"ERROR {plugin}/{skill}: fetch failed ({e})", file=sys.stderr)
            errors += 1
            continue

        fm, body = parse_frontmatter(raw)
        if not fm.get("name"):
            fm["name"] = skill
        out = render_cursor_skill(plugin, fm, body)

        if dry_run:
            print(f"[dry-run] {dest}")
            added += 1
            continue

        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(out, encoding="utf-8")
        added += 1

    return added, skipped, errors


def write_connector_stubs(plugins: list[str], dry_run: bool) -> None:
    for plugin in plugins:
        stub = OUT_ROOT / plugin / f"CONNECTORS-{plugin}.md"
        if stub.exists():
            continue
        content = (
            f"# Connectors ({plugin})\n\n"
            f"See [CONNECTORS.md](https://github.com/anthropics/knowledge-work-plugins/blob/main/{plugin}/CONNECTORS.md) "
            f"in the upstream plugin for MCP setup.\n"
        )
        if dry_run:
            print(f"[dry-run] connector stub {stub}")
            continue
        stub.write_text(content, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Import knowledge-work-plugins skills")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--force", action="store_true", help="Overwrite existing SKILL.md")
    ap.add_argument("--plugins", type=str, default="", help="Comma-separated plugin ids")
    args = ap.parse_args()

    plugins = [p.strip() for p in args.plugins.split(",") if p.strip()] or PLUGINS
    unknown = [p for p in plugins if p not in PLUGINS]
    if unknown:
        print(f"Unknown plugins: {unknown}", file=sys.stderr)
        return 1

    total_added = total_skipped = total_errors = 0
    for plugin in plugins:
        a, s, e = import_plugin(plugin, args.dry_run, args.force)
        total_added += a
        total_skipped += s
        total_errors += e
        print(f"{plugin}: added={a} skipped={s} errors={e}")

    write_hub_skills(plugins, args.dry_run)
    write_connector_stubs(plugins, args.dry_run)

    print(
        f"Done: added={total_added} skipped={total_skipped} errors={total_errors} "
        f"dry_run={args.dry_run}"
    )
    return 1 if total_errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
