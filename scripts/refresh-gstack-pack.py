#!/usr/bin/env python3
"""Re-vendor the gstack skill pack from an upstream gstack checkout.

Maps upstream flat skill dirs to nested paths under .cursor/skills/gstack/.
Updates registry/gstack-sync.json and registry/manifest.json gstack fields.

Usage:
  python3 scripts/refresh-gstack-pack.py /path/to/gstack [--dry-run]
"""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / ".cursor" / "skills" / "gstack"
SYNC_JSON = ROOT / "registry" / "gstack-sync.json"
MANIFEST = ROOT / "registry" / "manifest.json"
VERSION_FILE = "VERSION"

# Upstream flat name -> path under gstack/ (excluding gstack/SKILL.md meta)
PATH_MAP: dict[str, str] = {
    "autoplan": "plan-review/autoplan",
    "benchmark": "browser-qa/benchmark",
    "benchmark-models": "browser-qa/benchmark-models",
    "browse": "browser-qa/browse",
    "browser-skills/hackernews-frontpage": "scrape/browser-skills/hackernews-frontpage",
    "canary": "browser-qa/canary",
    "careful": "security-safety/careful",
    "codex": "code-quality/codex",
    "context-restore": "context-memory/context-restore",
    "context-save": "context-memory/context-save",
    "cso": "security-safety/cso",
    "design-consultation": "design/design-consultation",
    "design-html": "design/design-html",
    "design-review": "design/design-review",
    "design-shotgun": "design/design-shotgun",
    "devex-review": "plan-review/devex-review",
    "document-generate": "deploy-ship/document-generate",
    "document-release": "deploy-ship/document-release",
    "freeze": "security-safety/freeze",
    "gstack-upgrade": "utility/gstack-upgrade",
    "guard": "security-safety/guard",
    "health": "code-quality/health",
    "investigate": "code-quality/investigate",
    "ios-clean": "ios/ios-clean",
    "ios-design-review": "ios/ios-design-review",
    "ios-fix": "ios/ios-fix",
    "ios-qa": "ios/ios-qa",
    "ios-sync": "ios/ios-sync",
    "land-and-deploy": "deploy-ship/land-and-deploy",
    "landing-report": "deploy-ship/landing-report",
    "learn": "context-memory/learn",
    "make-pdf": "utility/make-pdf",
    "office-hours": "utility/office-hours",
    "open-gstack-browser": "utility/open-gstack-browser",
    "openclaw/skills/gstack-openclaw-ceo-review": "remote-agents/openclaw/gstack-openclaw-ceo-review",
    "openclaw/skills/gstack-openclaw-investigate": "remote-agents/openclaw/gstack-openclaw-investigate",
    "openclaw/skills/gstack-openclaw-office-hours": "remote-agents/openclaw/gstack-openclaw-office-hours",
    "openclaw/skills/gstack-openclaw-retro": "remote-agents/openclaw/gstack-openclaw-retro",
    "pair-agent": "remote-agents/pair-agent",
    "plan-ceo-review": "plan-review/plan-ceo-review",
    "plan-design-review": "plan-review/plan-design-review",
    "plan-devex-review": "plan-review/plan-devex-review",
    "plan-eng-review": "plan-review/plan-eng-review",
    "plan-tune": "plan-review/plan-tune",
    "qa": "browser-qa/qa",
    "qa-only": "browser-qa/qa-only",
    "retro": "utility/retro",
    "review": "code-quality/review",
    "scrape": "scrape/scrape",
    "setup-browser-cookies": "utility/setup-browser-cookies",
    "setup-deploy": "deploy-ship/setup-deploy",
    "setup-gbrain": "context-memory/setup-gbrain",
    "ship": "deploy-ship/ship",
    "skillify": "scrape/skillify",
    "spec": "plan-review/spec",
    "sync-gbrain": "context-memory/sync-gbrain",
    "unfreeze": "security-safety/unfreeze",
}

AUX_DIRS = ("references", "scripts", "assets", "commands", "tests")
AUX_FILES = ("reference.md", "LICENSE.txt", "LICENSE", "forms.md", "config.yaml")


def git_head(upstream: Path) -> str:
    import subprocess

    r = subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=upstream,
        capture_output=True,
        text=True,
        check=False,
    )
    return r.stdout.strip() if r.returncode == 0 else ""


def read_version(upstream: Path) -> str:
    vf = upstream / VERSION_FILE
    if vf.exists():
        return vf.read_text(encoding="utf-8").strip()
    return "unknown"


def copy_skill(upstream: Path, rel_key: str, dest_rel: str, dry_run: bool) -> None:
    src_dir = upstream / rel_key
    src_skill = src_dir / "SKILL.md"
    if not src_skill.exists():
        raise SystemExit(f"Missing upstream skill: {src_skill}")

    dest_dir = PACK_ROOT / dest_rel
    if not dry_run:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src_skill, dest_dir / "SKILL.md")

        for name in AUX_DIRS:
            aux = src_dir / name
            if aux.is_dir():
                shutil.copytree(aux, dest_dir / name, dirs_exist_ok=True)
        for name in AUX_FILES:
            aux = src_dir / name
            if aux.is_file():
                shutil.copy2(aux, dest_dir / name)

    print(f"  {'would copy' if dry_run else 'copied'} {rel_key} -> gstack/{dest_rel}")


def copy_meta_skill(upstream: Path, dry_run: bool) -> None:
    src = upstream / "SKILL.md"
    dest = PACK_ROOT / "SKILL.md"
    if not src.exists():
        return
    if dry_run:
        print("  would copy SKILL.md -> gstack/SKILL.md (pack meta)")
    else:
        shutil.copy2(src, dest)
        print("  copied SKILL.md -> gstack/SKILL.md (pack meta)")


def update_manifest(version: str, commit: str, synced_at: str, skill_count: int) -> None:
    base: dict = {}
    if MANIFEST.exists():
        base = json.loads(MANIFEST.read_text(encoding="utf-8"))
    base.update(
        {
            "gstack_version": version,
            "gstack_commit": commit,
            "gstack_synced_at": synced_at,
            "gstack_skill_count": skill_count,
        }
    )
    MANIFEST.write_text(json.dumps(base, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def update_sync_json(
    upstream: Path,
    version: str,
    commit: str,
    synced_at: str,
    skill_count: int,
    prior: dict | None,
) -> None:
    payload = {
        "upstream_repo": "https://github.com/garrytan/gstack",
        "upstream_version": version,
        "upstream_commit": commit,
        "synced_at": synced_at,
        "local_pack_path": ".cursor/skills/gstack",
        "prior_snapshot": prior or {},
        "local_skill_count": skill_count,
        "upstream_skill_count": len(PATH_MAP),
        "local_patches": [],
        "refresh_script": "scripts/refresh-gstack-pack.py",
        "staleness_policy": {"max_age_days": 90, "warn_if_commit_unknown": True},
    }
    SYNC_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh vendored gstack pack from upstream")
    parser.add_argument("upstream", type=Path, help="Path to gstack repo checkout")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    upstream = args.upstream.resolve()
    if not upstream.is_dir():
        raise SystemExit(f"Upstream path not found: {upstream}")

    prior = None
    if SYNC_JSON.exists():
        prior = json.loads(SYNC_JSON.read_text(encoding="utf-8"))
        prior_snapshot = {
            "commit": prior.get("upstream_commit", "unknown"),
            "version": prior.get("upstream_version", "unknown"),
            "skill_count": prior.get("local_skill_count"),
            "notes": "Snapshot before refresh-gstack-pack.py run",
        }
    else:
        prior_snapshot = {
            "commit": "unknown",
            "version": "unknown",
            "skill_count": len(list(PACK_ROOT.rglob("SKILL.md"))) if PACK_ROOT.exists() else 0,
            "notes": "First tracked refresh",
        }

    version = read_version(upstream)
    commit = git_head(upstream)
    synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    print(f"Refreshing gstack pack from {upstream}")
    print(f"  upstream version={version} commit={commit[:12] if commit else '?'}")
    print(f"  mapping {len(PATH_MAP)} skills")

    for rel_key, dest_rel in sorted(PATH_MAP.items()):
        copy_skill(upstream, rel_key, dest_rel, args.dry_run)

    copy_meta_skill(upstream, args.dry_run)

    skill_count = len(PATH_MAP) + 1  # mapped skills + meta SKILL.md

    if not args.dry_run:
        update_sync_json(upstream, version, commit, synced_at, skill_count, prior_snapshot)
        update_manifest(version, commit, synced_at, skill_count)
        print(f"\nUpdated {SYNC_JSON.relative_to(ROOT)} and {MANIFEST.relative_to(ROOT)}")
        print("Next: python3 scripts/generate-registry.py && python3 scripts/convert-to-claude.py --in-repo")
    else:
        print("\nDry run complete; no files written.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
