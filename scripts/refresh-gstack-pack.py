#!/usr/bin/env python3
"""Refresh the vendored gstack skill pack from upstream.

The repo keeps Cursor-format skills under .cursor/skills/gstack as the source of
truth, then regenerates Claude and registry artifacts from there. Upstream gstack
uses flat skill directories, so this script maps those flat directories into this
repo's nested gstack domain layout.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PACK_ROOT = ROOT / ".cursor" / "skills" / "gstack"
SYNC_JSON = ROOT / "registry" / "gstack-sync.json"
VERSION_FILE = "VERSION"
DEFAULT_UPSTREAM_URL = "https://github.com/garrytan/gstack.git"
DEFAULT_REF = "main"

# Upstream flat name -> path under .cursor/skills/gstack.
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
    "diagram": "utility/diagram",
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

AUX_DIRS = (
    "references",
    "scripts",
    "assets",
    "commands",
    "tests",
    "templates",
    "docs",
    "daemon",
    "sections",
    "specialists",
    "vendor",
    "migrations",
    "_lib",
    "fixtures",
)
AUX_FILE_NAMES = {"LICENSE", "LICENSE.txt", "config.yaml"}
AUX_FILE_SUFFIXES = (".md", ".json", ".yaml", ".yml", ".js", ".mjs", ".ts", ".tsx", ".swift", ".template")


def run_git(args: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(
        ["git", *args],
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        raise SystemExit(result.stderr.strip() or result.stdout.strip())
    return result.stdout.strip()


def checkout_upstream(upstream: Path | None, upstream_url: str, ref: str) -> tuple[Path, tempfile.TemporaryDirectory[str] | None]:
    if upstream is not None:
        path = upstream.resolve()
        if not path.is_dir():
            raise SystemExit(f"Upstream path not found: {path}")
        run_git(["rev-parse", "--is-inside-work-tree"], cwd=path)
        return path, None

    tmp = tempfile.TemporaryDirectory(prefix="gstack-upstream-")
    path = Path(tmp.name) / "gstack"
    run_git(["clone", "--depth", "1", "--branch", ref, upstream_url, str(path)])
    return path, tmp


def git_head(upstream: Path) -> str:
    return run_git(["rev-parse", "HEAD"], cwd=upstream)


def read_version(upstream: Path) -> str:
    version = upstream / VERSION_FILE
    if version.exists():
        return version.read_text(encoding="utf-8").strip()
    return "unknown"


def upstream_skill_paths(upstream: Path) -> set[str]:
    return {
        skill_md.parent.relative_to(upstream).as_posix()
        for skill_md in upstream.rglob("SKILL.md")
        if ".git" not in skill_md.parts
    }


def local_skill_paths() -> set[str]:
    if not PACK_ROOT.exists():
        return set()
    return {
        skill_md.parent.relative_to(PACK_ROOT).as_posix()
        for skill_md in PACK_ROOT.rglob("SKILL.md")
    }


def copy_skill(upstream: Path, rel_key: str, dest_rel: str, dry_run: bool) -> None:
    src_dir = upstream / rel_key
    src_skill = src_dir / "SKILL.md"
    if not src_skill.exists():
        raise SystemExit(f"Missing upstream skill: {src_skill}")

    dest_dir = PACK_ROOT / dest_rel
    if dry_run:
        print(f"  would copy {rel_key} -> gstack/{dest_rel}")
        return

    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_skill, dest_dir / "SKILL.md")

    for name in AUX_DIRS:
        aux = src_dir / name
        if aux.is_dir():
            shutil.copytree(aux, dest_dir / name)
    for aux in sorted(src_dir.iterdir()):
        if not aux.is_file() or aux.name in {"SKILL.md", "SKILL.md.tmpl"}:
            continue
        if aux.name in AUX_FILE_NAMES or aux.suffix in AUX_FILE_SUFFIXES:
            shutil.copy2(aux, dest_dir / aux.name)

    print(f"  copied {rel_key} -> gstack/{dest_rel}")


def copy_meta_skill(upstream: Path, dry_run: bool) -> None:
    src = upstream / "SKILL.md"
    dest = PACK_ROOT / "SKILL.md"
    if not src.exists():
        return
    if dry_run:
        print("  would copy SKILL.md -> gstack/SKILL.md")
        return
    PACK_ROOT.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dest)
    print("  copied SKILL.md -> gstack/SKILL.md")


def prune_stale(dry_run: bool) -> list[str]:
    desired = {".", *PATH_MAP.values()}
    stale = sorted(path for path in local_skill_paths() if path not in desired)
    for rel in stale:
        target = PACK_ROOT / rel
        if dry_run:
            print(f"  would remove stale gstack/{rel}")
        else:
            shutil.rmtree(target)
            print(f"  removed stale gstack/{rel}")
    return stale


def prune_empty_dirs(dry_run: bool) -> None:
    if dry_run or not PACK_ROOT.exists():
        return
    for child in sorted(PACK_ROOT.rglob("*"), key=lambda p: len(p.parts), reverse=True):
        if child.is_dir():
            try:
                child.rmdir()
            except OSError:
                pass


def read_prior_snapshot() -> dict[str, object]:
    if SYNC_JSON.exists():
        current = json.loads(SYNC_JSON.read_text(encoding="utf-8"))
        return {
            "upstream_commit": current.get("upstream_commit", "unknown"),
            "upstream_version": current.get("upstream_version", "unknown"),
            "local_skill_count": current.get("local_skill_count"),
            "synced_at": current.get("synced_at"),
        }
    return {
        "upstream_commit": "unknown",
        "upstream_version": "unknown",
        "local_skill_count": len(local_skill_paths()),
        "synced_at": None,
    }


def write_sync_json(
    upstream_url: str,
    ref: str,
    version: str,
    commit: str,
    synced_at: str,
    stale: list[str],
    prior: dict[str, object],
) -> None:
    payload = {
        "upstream_repo": upstream_url.removesuffix(".git"),
        "upstream_ref": ref,
        "upstream_version": version,
        "upstream_commit": commit,
        "synced_at": synced_at,
        "local_pack_path": ".cursor/skills/gstack",
        "prior_snapshot": prior,
        "local_skill_count": len(PATH_MAP) + 1,
        "upstream_skill_count": len(PATH_MAP) + 1,
        "removed_local_skill_paths": stale,
        "local_patches": [],
        "refresh_script": "scripts/refresh-gstack-pack.py",
        "staleness_policy": {"max_age_days": 30, "warn_if_commit_unknown": True},
    }
    SYNC_JSON.parent.mkdir(parents=True, exist_ok=True)
    SYNC_JSON.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Refresh vendored gstack skills from upstream")
    parser.add_argument("upstream", nargs="?", type=Path, help="Optional local gstack checkout")
    parser.add_argument("--upstream-url", default=DEFAULT_UPSTREAM_URL)
    parser.add_argument("--ref", default=DEFAULT_REF)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    upstream, tmp = checkout_upstream(args.upstream, args.upstream_url, args.ref)
    try:
        version = read_version(upstream)
        commit = git_head(upstream)
        prior = read_prior_snapshot()
        upstream_paths = upstream_skill_paths(upstream)
        missing = sorted(path for path in PATH_MAP if path not in upstream_paths)
        if missing:
            raise SystemExit("Missing mapped upstream skills:\n  " + "\n  ".join(missing))

        unmapped = sorted(upstream_paths - {".", *PATH_MAP.keys()})
        if unmapped:
            raise SystemExit("Unmapped upstream skills:\n  " + "\n  ".join(unmapped))

        print(f"Refreshing gstack from {args.upstream_url} @ {args.ref}")
        print(f"  upstream version={version} commit={commit}")
        print(f"  mapped skills={len(PATH_MAP)} + meta")

        stale = prune_stale(args.dry_run)
        for rel_key, dest_rel in sorted(PATH_MAP.items()):
            copy_skill(upstream, rel_key, dest_rel, args.dry_run)
        copy_meta_skill(upstream, args.dry_run)
        prune_empty_dirs(args.dry_run)

        if not args.dry_run:
            synced_at = datetime.now(timezone.utc).strftime("%Y-%m-%d")
            write_sync_json(args.upstream_url, args.ref, version, commit, synced_at, stale, prior)
            print(f"\nUpdated {SYNC_JSON.relative_to(ROOT)}")
            print("Next: regenerate Claude and registry artifacts.")
        else:
            print("\nDry run complete; no files written.")
    finally:
        if tmp is not None:
            tmp.cleanup()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
