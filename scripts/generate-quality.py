#!/usr/bin/env python3
"""Compute per-skill quality scores and write registry/quality.json."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
QUALITY_JSON = ROOT / "registry" / "quality.json"
CURSOR_ROOT = ROOT / ".cursor" / "skills"


def score_skill(skill: dict, skill_path: Path) -> dict:
    text = skill_path.read_text(encoding="utf-8") if skill_path.exists() else ""
    desc = skill.get("description", "")
    triggers = skill.get("triggers", [])
    has_h2 = bool(re.search(r"^##\s+", text, re.M))
    has_examples = "Good:" in text or "Bad:" in text or "```" in text
    ref_dir = skill_path.parent
    has_reference = (ref_dir / "reference.md").exists() or any(ref_dir.glob("references/*"))

    checks = {
        "description_min_80": len(desc) >= 80,
        "has_triggers": len(triggers) >= 1,
        "has_usage_section": has_h2,
        "has_examples": has_examples,
        "has_reference": has_reference,
        "risk_set": skill.get("risk") in ("low", "medium", "high"),
    }
    points = sum(1 for ok in checks.values() if ok)
    score = round(100 * points / len(checks))

    issues = []
    if not checks["description_min_80"]:
        issues.append("short description")
    if not checks["has_triggers"]:
        issues.append("no triggers in description")
    if not checks["has_usage_section"]:
        issues.append("missing ## section")
    if score < 50:
        issues.append("low overall score")

    return {
        "id": skill["id"],
        "score": score,
        "checks": checks,
        "issues": issues,
    }


def main() -> int:
    if not REGISTRY.exists():
        print("Run generate-registry.py first", file=sys.stderr)
        return 1
    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    rows = []
    for skill in data["skills"]:
        path = ROOT / skill["path"]
        rows.append(score_skill(skill, path))

    low = [r for r in rows if r["score"] < 50]
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_version": 1,
        "count": len(rows),
        "average_score": round(sum(r["score"] for r in rows) / len(rows)) if rows else 0,
        "low_score_count": len(low),
        "skills": rows,
    }
    QUALITY_JSON.parent.mkdir(parents=True, exist_ok=True)
    QUALITY_JSON.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    print(f"Wrote quality scores for {len(rows)} skills (avg {payload['average_score']}, low {len(low)})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
