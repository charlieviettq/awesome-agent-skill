"""Shared recommendation engine for SkillHub CLI and catalog generation."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

SYNONYM_MAP: dict[str, list[str]] = {
    "tdd": ["test", "tests"],
    "spec": ["requirements", "design"],
    "rag": ["retrieval", "embeddings"],
    "debug": ["investigate", "fix", "bug"],
    "ci": ["test", "pipeline", "github"],
    "pr": ["review", "pull", "merge"],
    "pdf": ["document", "docx", "summarize"],
    "summarize": ["pdf", "document", "summary"],
    "analyze": ["pdf", "analysis", "document"],
    "document": ["pdf", "docx"],
    "deploy": ["ship", "release", "launch"],
    "monitor": ["observability", "slo", "alert"],
}

FIELD_WEIGHTS: tuple[tuple[str, int], ...] = (
    ("id", 18),
    ("name", 15),
    ("domain", 8),
    ("description", 8),
    ("summary", 6),
)


def token_in_text(token: str, text: str) -> bool:
    """Substring match with word boundaries for short tokens (avoids 'end' in 'frontend')."""
    text_l = text.lower()
    token_l = token.lower()
    if len(token_l) <= 4:
        return re.search(r"\b" + re.escape(token_l) + r"\b", text_l) is not None
    return token_l in text_l


def expand_tokens(query: str) -> list[str]:
    tokens = [t for t in re.split(r"[^\w]+", query.lower()) if len(t) > 2]
    if not tokens:
        tokens = [query.lower()]
    expanded: list[str] = []
    for t in tokens:
        expanded.append(t)
        expanded.extend(SYNONYM_MAP.get(t, []))
    return expanded


def match_reasons(query: str, skill: dict[str, Any]) -> list[str]:
    reasons: list[str] = []
    tokens = expand_tokens(query)
    for token in tokens:
        for field, _weight in FIELD_WEIGHTS:
            val = str(skill.get(field, ""))
            if token_in_text(token, val):
                reasons.append(f"matched {field}")
                break
        for trig in skill.get("triggers", []) + skill.get("trigger_phrases", []):
            if token_in_text(token, str(trig)):
                reasons.append(f"trigger: {trig}")
                break
        for tag in skill.get("tags", []):
            if token_in_text(token, str(tag)):
                reasons.append(f"tag: {tag}")
                break
    # dedupe preserving order
    seen: set[str] = set()
    out: list[str] = []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            out.append(r)
    return out[:4]


def score_match(query: str, skill: dict[str, Any]) -> int:
    score = 0
    for token in expand_tokens(query):
        for field, weight in FIELD_WEIGHTS:
            val = str(skill.get(field, ""))
            if token_in_text(token, val):
                score += weight
        for tag in skill.get("tags", []):
            if token_in_text(token, str(tag)):
                score += 5
        for trig in skill.get("triggers", []):
            if token_in_text(token, str(trig)):
                score += 10
        for trig in skill.get("trigger_phrases", []):
            if token_in_text(token, str(trig)):
                score += 10

    tier = skill.get("tier")
    if tier == "core":
        score += 5
    risk = skill.get("risk")
    if risk == "low":
        score += 2
    elif risk == "high":
        score -= 3

    q_lower = query.lower()
    sid = str(skill.get("id", "")).lower()
    if "pdf" in q_lower and "pdf" in sid:
        score += 20
    if "document" in q_lower and any(x in sid for x in ("pdf", "docx", "writing-docs")):
        score += 8
    if "changelog" in q_lower and sid == "gstack/deploy-ship/ship":
        score += 22
    if "ship" in q_lower and sid == "gstack/deploy-ship/ship":
        score += 12
    if any(k in q_lower for k in ("xlsx", "csv", "spreadsheet", ".tsv", ".xlsm")) and sid == "writing-docs/xlsx":
        score += 22

    return score


def rank_skills(skills: list[dict[str, Any]], query: str) -> list[tuple[int, dict[str, Any]]]:
    ranked = [(score_match(query, s), s) for s in skills]
    ranked = [(sc, s) for sc, s in ranked if sc > 0]
    ranked.sort(key=lambda x: (-x[0], x[1]["id"]))
    return ranked


def bundle_skill_ids(bundle: dict[str, Any]) -> set[str]:
    ids: set[str] = set(bundle.get("skills", []))
    for domain in bundle.get("domains", []):
        ids.add(f"domain:{domain}")
    return ids


def suggest_bundle(
    ranked: list[tuple[int, dict[str, Any]]],
    bundles: list[dict[str, Any]],
    limit: int = 5,
) -> dict[str, Any] | None:
    if not ranked:
        return None
    top_ids = {s["id"] for _, s in ranked[:limit]}
    top_domains = {s["domain"] for _, s in ranked[:limit]}
    best: tuple[int, dict[str, Any]] | None = None
    for bundle in bundles:
        if bundle.get("id") == "full":
            continue
        score = 0
        explicit = set(bundle.get("skills", []))
        for sid in explicit:
            if sid in top_ids:
                score += 3
        for domain in bundle.get("domains", []):
            if domain in top_domains:
                score += 2
        if score > 0 and (best is None or score > best[0]):
            best = (score, bundle)
    return best[1] if best else None


def install_skill_command(skill_id: str, fmt: str = "cursor", *, pip_cli: bool = False) -> str:
    cmd = "skillhub" if pip_cli else "python3 scripts/skillhub.py"
    return f"{cmd} install {skill_id} . --format {fmt}"


def install_bundle_command(bundle_id: str, fmt: str = "cursor", *, pip_cli: bool = False) -> str:
    cmd = "skillhub" if pip_cli else "python3 scripts/skillhub.py"
    return f"{cmd} install-bundle {bundle_id} . --format {fmt}"


def clone_and_install_prefix() -> str:
    return (
        "git clone https://github.com/charlieviettq/awesome-agent-skill.git "
        "&& cd awesome-agent-skill"
    )


def reload_note(fmt: str) -> str:
    if fmt == "cursor":
        return "Reload Cursor window or start a new chat to pick up skills."
    if fmt == "claude":
        return "Restart Claude Code session to pick up skills."
    return "Reload your agent session (Cursor window / Claude Code restart)."


def github_skill_url(skill_id: str, repo: str = "charlieviettq/awesome-agent-skill") -> str:
    path = f".cursor/skills/{skill_id}/SKILL.md"
    return f"https://github.com/{repo}/blob/main/{path}"


def build_recommendation(
    query: str,
    skills: list[dict[str, Any]],
    bundles: list[dict[str, Any]],
    *,
    limit: int = 5,
    fmt: str = "cursor",
    pip_cli: bool = False,
) -> dict[str, Any]:
    ranked = rank_skills(skills, query)
    top = ranked[:limit]
    bundle = suggest_bundle(ranked, bundles, limit=limit)
    bundle_id = bundle["id"] if bundle else None
    return {
        "query": query,
        "format": fmt,
        "bundle": bundle,
        "bundle_id": bundle_id,
        "skills": [
            {
                "score": sc,
                "id": s["id"],
                "name": s["name"],
                "domain": s["domain"],
                "description": (s.get("description") or "")[:240],
                "tier": s.get("tier"),
                "risk": s.get("risk"),
                "reasons": match_reasons(query, s),
            }
            for sc, s in top
        ],
        "install_bundle_command": (
            install_bundle_command(bundle_id, fmt, pip_cli=pip_cli) if bundle_id else None
        ),
        "install_skill_commands": [
            install_skill_command(s["id"], fmt, pip_cli=pip_cli) for _, s in top[:3]
        ],
        "full_workflow": (
            f"{clone_and_install_prefix()} && "
            f"{install_bundle_command(bundle_id, fmt, pip_cli=pip_cli) if bundle_id else install_skill_command(top[0][1]['id'], fmt, pip_cli=pip_cli)}"
            if top
            else None
        ),
        "reload_note": reload_note(fmt),
    }


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))
