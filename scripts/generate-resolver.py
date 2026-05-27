#!/usr/bin/env python3
"""Generate a compact resolver markdown from registry/skills.json."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
OUT = ROOT / "docs" / "resolver.md"


def main() -> int:
    if not REGISTRY.exists():
        raise SystemExit("registry/skills.json missing, run generate-registry.py first")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = data.get("skills", [])

    by_domain: dict[str, list[dict]] = {}
    for s in skills:
        by_domain.setdefault(s["domain"], []).append(s)

    lines: list[str] = []
    lines.append("# Skill Resolver Overview")
    lines.append("")
    lines.append(
        "Compact view of skills by domain and tier to help routers and humans find the right skill quickly."
    )
    lines.append("")

    for dom in sorted(by_domain):
        lines.append(f"## {dom}")
        lines.append("")
        domain_skills = sorted(
            by_domain[dom],
            key=lambda s: (str(s.get("tier", "community")), s["id"]),
        )
        for s in domain_skills:
            tier = s.get("tier", "community")
            name = s.get("name", s["id"])
            summary = s.get("summary") or s.get("description", "")
            summary = summary.replace("\n", " ").strip()
            if len(summary) > 140:
                summary = summary[:137] + "..."
            lines.append(f"- **[{tier}]** `{s['id']}` — {name}: {summary}")
        lines.append("")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote resolver to {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

