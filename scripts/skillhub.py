#!/usr/bin/env python3
"""SkillHub CLI — list, search, install skills from the local registry."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
BUNDLES = ROOT / "registry" / "bundles.json"


def load_registry() -> dict:
    if not REGISTRY.exists():
        sys.exit("registry/skills.json missing. Run: python3 scripts/generate-registry.py")
    return json.loads(REGISTRY.read_text(encoding="utf-8"))


def load_bundles() -> dict:
    if not BUNDLES.exists():
        sys.exit("registry/bundles.json missing")
    return json.loads(BUNDLES.read_text(encoding="utf-8"))


def cmd_list(args: argparse.Namespace) -> int:
    data = load_registry()
    skills = data["skills"]
    if args.domain:
        skills = [s for s in skills if s["domain"] == args.domain]
    for s in skills:
        print(f"{s['id']}\t{s['name']}\t[{s['domain']}]")
    print(f"\n{len(skills)} skills", file=sys.stderr)
    return 0


def score_match(query: str, skill: dict) -> int:
    q = query.lower()
    score = 0
    for field in ("id", "name", "domain", "description"):
        val = str(skill.get(field, "")).lower()
        if q in val:
            score += 10
    for tag in skill.get("tags", []):
        if q in tag.lower():
            score += 5
    for trig in skill.get("triggers", []):
        if q in trig.lower():
            score += 8
    return score


def cmd_search(args: argparse.Namespace) -> int:
    data = load_registry()
    ranked = [(score_match(args.query, s), s) for s in data["skills"]]
    ranked = [(sc, s) for sc, s in ranked if sc > 0]
    ranked.sort(key=lambda x: (-x[0], x[1]["id"]))
    limit = args.limit
    for sc, s in ranked[:limit]:
        print(f"{sc:3d}  {s['id']}\t{s['name']}")
        if args.verbose:
            desc = s.get("description", "")[:120]
            print(f"      {desc}")
    if not ranked:
        print("No matches", file=sys.stderr)
        return 1
    return 0


def cmd_show(args: argparse.Namespace) -> int:
    data = load_registry()
    skill = next((s for s in data["skills"] if s["id"] == args.skill_id), None)
    if not skill:
        print(f"Unknown skill: {args.skill_id}", file=sys.stderr)
        return 1
    print(json.dumps(skill, indent=2, ensure_ascii=False))
    return 0


def cmd_bundles(args: argparse.Namespace) -> int:
    data = load_bundles()
    for b in data["bundles"]:
        domains = ", ".join(b.get("domains", [])) or "-"
        skills = len(b.get("skills", []))
        print(f"{b['id']}\t{b['title']}\tdomains={domains}\tskills={skills}")
        if args.verbose:
            print(f"  {b.get('description', '')}")
    return 0


def run_script(script: Path, argv: list[str]) -> int:
    result = subprocess.run(["bash", str(script), *argv], cwd=ROOT)
    return result.returncode


def cmd_install(args: argparse.Namespace) -> int:
    script = ROOT / "scripts" / "install" / "install-skill.sh"
    fmt_argv: list[str] = []
    if args.format:
        fmt_argv = ["--format", args.format]
    return run_script(script, [args.skill_id, args.target, *fmt_argv])


def cmd_install_bundle(args: argparse.Namespace) -> int:
    script = ROOT / "scripts" / "install" / "install-bundle.sh"
    fmt_argv: list[str] = []
    if args.format:
        fmt_argv = ["--format", args.format]
    return run_script(script, [args.bundle_id, args.target, *fmt_argv])


def cmd_validate(_: argparse.Namespace) -> int:
    return subprocess.run([sys.executable, str(ROOT / "scripts" / "validate-skills.py")], cwd=ROOT).returncode


def cmd_doctor(_: argparse.Namespace) -> int:
    ok = True

    def check(label: str, passed: bool, detail: str = "") -> None:
        nonlocal ok
        status = "ok" if passed else "FAIL"
        if not passed:
            ok = False
        line = f"[{status}] {label}"
        if detail:
            line += f" — {detail}"
        print(line)

    check("registry/skills.json", REGISTRY.exists())
    check("registry/bundles.json", BUNDLES.exists())
    if REGISTRY.exists():
        r = subprocess.run(
            [sys.executable, str(ROOT / "scripts" / "generate-registry.py"), "--check"],
            cwd=ROOT,
            capture_output=True,
            text=True,
        )
        check("registry sync", r.returncode == 0, r.stderr.strip() or r.stdout.strip())

    for name in ("install-domain.sh", "install-bundle.sh", "install-skill.sh"):
        p = ROOT / "scripts" / "install" / name
        check(name, p.exists() and p.stat().st_mode & 0o111)

    v = subprocess.run([sys.executable, str(ROOT / "scripts" / "validate-skills.py")], cwd=ROOT, capture_output=True)
    check("validate-skills.py", v.returncode == 0, "see output above" if v.returncode else "")

    return 0 if ok else 1


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="skillhub", description="SkillHub CLI for awesome-agent-skill")
    sub = p.add_subparsers(dest="command", required=True)

    ls = sub.add_parser("list", help="List skills")
    ls.add_argument("--domain", help="Filter by top-level domain")
    ls.set_defaults(func=cmd_list)

    sr = sub.add_parser("search", help="Search skills by keyword")
    sr.add_argument("query")
    sr.add_argument("-n", "--limit", type=int, default=15)
    sr.add_argument("-v", "--verbose", action="store_true")
    sr.set_defaults(func=cmd_search)

    sh = sub.add_parser("show", help="Show skill metadata as JSON")
    sh.add_argument("skill_id")
    sh.set_defaults(func=cmd_show)

    bd = sub.add_parser("bundles", help="List install bundles")
    bd.add_argument("-v", "--verbose", action="store_true")
    bd.set_defaults(func=cmd_bundles)

    ins = sub.add_parser("install", help="Install one skill into a project")
    ins.add_argument("skill_id")
    ins.add_argument("target")
    ins.add_argument("--format", choices=["cursor", "claude", "both"], default="both")
    ins.set_defaults(func=cmd_install)

    ib = sub.add_parser("install-bundle", help="Install a bundle into a project")
    ib.add_argument("bundle_id")
    ib.add_argument("target")
    ib.add_argument("--format", choices=["cursor", "claude", "both"], default="both")
    ib.set_defaults(func=cmd_install_bundle)

    val = sub.add_parser("validate", help="Run skill validation")
    val.set_defaults(func=cmd_validate)

    doc = sub.add_parser("doctor", help="Check registry, install scripts, validation")
    doc.set_defaults(func=cmd_doctor)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
