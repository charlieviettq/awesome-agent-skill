#!/usr/bin/env python3
"""Generate registry/skills.json and verify sync with .cursor/skills."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CURSOR_ROOT = ROOT / ".cursor" / "skills"
REGISTRY_DIR = ROOT / "registry"
SKILLS_JSON = REGISTRY_DIR / "skills.json"
BUNDLES_JSON = REGISTRY_DIR / "bundles.json"

DOMAIN_RISK = {
    "security-appsec": "medium",
    "gstack": "medium",
    "frontend-engineering": "medium",
    "mobile": "medium",
    "marketing": "medium",
    "ai-agent-systems": "low",
    "reliability-ops": "low",
    "core-workflow": "low",
}

DOMAIN_TAGS: dict[str, list[str]] = {
    "core-workflow": ["workflow", "planning", "review", "testing"],
    "ai-agent-systems": ["agents", "mcp", "rag", "tools"],
    "security-appsec": ["security", "api", "audit"],
    "reliability-ops": ["ci", "ops", "launch", "observability"],
    "frontend-engineering": ["frontend", "ui", "browser"],
    "gstack": ["qa", "ship", "browser", "gstack", "ios"],
    "voltagent": ["persona", "subagent", "roles"],
    "ml-dl": ["ml", "deep-learning"],
    "analysis-stats": ["statistics", "shap", "modeling"],
    "data-compute": ["data", "etl", "compute"],
    "eda-research": ["eda", "research"],
    "visualization": ["viz", "charts"],
    "writing-docs": ["docs", "writing"],
    "meta-tools": ["meta", "skills"],
    "performance": ["performance"],
    "product-growth": ["product", "growth"],
    "mobile": ["mobile", "ios", "android"],
    "marketing": ["marketing", "ads"],
    "architecture": ["architecture", "diagrams"],
}


def default_tier(domain: str) -> str:
    """Coarse tiering for now; can be refined later."""
    if domain in {"core-workflow", "ai-agent-systems", "reliability-ops", "security-appsec"}:
        return "core"
    if domain in {"gstack", "voltagent"}:
        return "imported"
    return "community"


def default_provenance(domain: str) -> str:
    if domain in {"gstack", "voltagent"}:
        return "imported-pack"
    return "awesome-agent-skill"


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    raw = text[3:end]
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
    return fm


def extract_triggers_from_fm(fm: dict[str, str], description: str) -> list[str]:
    """Pull triggers from YAML list frontmatter or legacy Triggers: in description."""
    raw = fm.get("triggers", "").strip()
    if raw.startswith("-"):
        out: list[str] = []
        for line in raw.splitlines():
            line = line.strip()
            if line.startswith("- "):
                out.append(line[2:].strip().strip('"').strip("'"))
        if out:
            return out
    m = re.search(r'Triggers:\s*(.+?)(?:\.|$)', description, flags=re.I | re.S)
    if not m:
        return []
    chunk = m.group(1)
    return [t.strip().strip('"').strip("'") for t in re.findall(r'"([^"]+)"', chunk)]


def extract_triggers(description: str) -> list[str]:
    m = re.search(r'Triggers:\s*(.+?)(?:\.|$)', description, flags=re.I | re.S)
    if not m:
        return []
    chunk = m.group(1)
    return [t.strip().strip('"').strip("'") for t in re.findall(r'"([^"]+)"', chunk)]


def skill_id(path: Path) -> str:
    rel = path.relative_to(CURSOR_ROOT)
    if rel.name == "SKILL.md":
        return str(rel.parent).replace("\\", "/")
    return str(rel).replace("\\", "/")


def domain_of(skill_id_str: str) -> str:
    return skill_id_str.split("/", 1)[0] if "/" in skill_id_str else skill_id_str


def collect_skills() -> list[dict]:
    entries: list[dict] = []
    for skill_md in sorted(CURSOR_ROOT.rglob("SKILL.md")):
        rel = skill_id(skill_md)
        text = skill_md.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        name = fm.get("name", skill_md.parent.name)
        desc = fm.get("description", "").replace("\n", " ").strip()
        dom = domain_of(rel)
        tags = list(DOMAIN_TAGS.get(dom, [dom]))
        if name not in tags:
            tags.append(name)
        triggers = extract_triggers_from_fm(fm, desc)
        summary = desc[:240] if desc else ""
        skill_version = fm.get("version", "").strip() or None
        preamble_tier = fm.get("preamble-tier", "").strip() or None
        entries.append(
            {
                "id": rel,
                "name": name,
                "domain": dom,
                "path": f".cursor/skills/{rel}/SKILL.md",
                "description": desc[:500],
                "summary": summary,
                "triggers": triggers,
                "trigger_phrases": triggers,
                "skill_version": skill_version,
                "preamble_tier": preamble_tier,
                "risk": DOMAIN_RISK.get(dom, "low"),
                "formats": ["cursor", "claude"],
                "source": "awesome-agent-skill",
                "license": "MIT",
                "tags": tags[:8],
                # v2 metadata — defaults; can be refined by other tooling
                "requires_tools": [],
                "writes_files": [],
                "network_access": "unknown",
                "risk_reason": "",
                "provenance": default_provenance(dom),
                "related": [],
                "tier": default_tier(dom),
                "quality_score": None,
            }
        )
    return entries


def load_bundles() -> dict:
    if not BUNDLES_JSON.exists():
        raise SystemExit(f"Missing {BUNDLES_JSON}")
    return json.loads(BUNDLES_JSON.read_text(encoding="utf-8"))


def validate_bundles(skills: list[dict]) -> list[str]:
    errors: list[str] = []
    skill_ids = {s["id"] for s in skills}
    domain_skills: dict[str, list[str]] = {}
    for s in skills:
        domain_skills.setdefault(s["domain"], []).append(s["id"])

    data = load_bundles()
    for bundle in data.get("bundles", []):
        bid = bundle.get("id", "?")
        for sid in bundle.get("skills", []):
            if sid not in skill_ids:
                errors.append(f"bundle {bid}: unknown skill id {sid}")
        for dom in bundle.get("domains", []):
            if dom not in domain_skills:
                errors.append(f"bundle {bid}: unknown domain {dom}")
    return errors


def build_payload(skills: list[dict]) -> dict:
    return {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "schema_version": 2,
        "count": len(skills),
        "skills": skills,
    }


def registry_body(payload: dict) -> dict:
    """Stable subset for sync checks (ignore generated_at)."""
    return {
        "schema_version": payload["schema_version"],
        "count": payload["count"],
        "skills": payload["skills"],
    }


def check_sync(payload: dict) -> list[str]:
    if not SKILLS_JSON.exists():
        return ["registry/skills.json is missing; run scripts/generate-registry.py"]
    committed = json.loads(SKILLS_JSON.read_text(encoding="utf-8"))
    if registry_body(payload) != registry_body(committed):
        return ["registry/skills.json is out of date; run scripts/generate-registry.py"]
    return []


def main() -> int:
    check_only = "--check" in sys.argv
    skills = collect_skills()
    payload = build_payload(skills)

    errors = validate_bundles(skills)
    if errors:
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1

    if check_only:
        sync_errors = check_sync(payload)
        if sync_errors:
            for e in sync_errors:
                print(f"ERROR: {e}", file=sys.stderr)
            return 1
        print(f"Registry OK ({len(skills)} skills)")
        return 0

    REGISTRY_DIR.mkdir(parents=True, exist_ok=True)
    SKILLS_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"Wrote {len(skills)} skills to {SKILLS_JSON}")
    print("Bundles validated against skills registry")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
