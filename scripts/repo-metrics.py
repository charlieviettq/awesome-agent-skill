#!/usr/bin/env python3
"""Generate a lightweight repo metrics snapshot markdown report."""

from __future__ import annotations

import json
import subprocess
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURSOR_ROOT = ROOT / ".cursor" / "skills"
METRICS_DIR = ROOT / "docs" / "metrics"


def gh_json(args: list[str]) -> dict | list | None:
    try:
        out = subprocess.check_output(["gh"] + args, cwd=ROOT, text=True)
        return json.loads(out)
    except Exception:
        return None


def count_domains() -> Counter[str]:
    counts: Counter[str] = Counter()
    for path in CURSOR_ROOT.rglob("SKILL.md"):
        rel = path.relative_to(CURSOR_ROOT)
        domain = rel.parts[0] if len(rel.parts) > 1 else rel.parts[0]
        counts[domain] += 1
    return counts


def main() -> None:
    METRICS_DIR.mkdir(parents=True, exist_ok=True)
    today = date.today()
    out_path = METRICS_DIR / f"{today:%Y-%m}.md"

    domain_counts = count_domains()
    cursor_total = sum(domain_counts.values())

    repo = gh_json(["repo", "view", "--json", "stargazerCount,forkCount,pushedAt,updatedAt"])
    releases = gh_json(["release", "list", "--limit", "5"]) or []

    lines = [
        f"# Repo metrics — {today:%Y-%m}",
        "",
        "## Snapshot",
        "",
        f"- Cursor `SKILL.md` files: **{cursor_total}**",
        f"- Claude mapped skills: **170** (see `scripts/claude-skill-map.json`)",
        "",
    ]

    if isinstance(repo, dict):
        lines.extend(
            [
                f"- Stars: **{repo.get('stargazerCount', 'n/a')}**",
                f"- Forks: **{repo.get('forkCount', 'n/a')}**",
                f"- Last push: `{repo.get('pushedAt', 'n/a')}`",
                "",
            ]
        )

    lines.extend(["## Skills by domain", ""])
    for domain, count in domain_counts.most_common():
        lines.append(f"- `{domain}/`: {count}")

    lines.extend(["", "## Recent releases", ""])
    if releases:
        for rel in releases:
            lines.append(f"- `{rel.get('tagName', '?')}` — {rel.get('name', rel.get('tagName', ''))}")
    else:
        lines.append("- No GitHub releases found (or `gh` unavailable).")

    lines.extend(
        [
            "",
            "## Release cadence",
            "",
            "Target: one tagged release every 2–4 weeks when skills or docs change materially.",
            "See [`docs/RELEASE_CADENCE.md`](../RELEASE_CADENCE.md).",
            "",
            "## Notes",
            "",
            "Regenerate with:",
            "",
            "```bash",
            "python3 scripts/repo-metrics.py",
            "```",
            "",
        ]
    )

    out_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {out_path}")


if __name__ == "__main__":
    main()
