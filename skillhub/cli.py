#!/usr/bin/env python3
"""SkillHub CLI — list, search, install skills from the local registry."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from pathlib import Path

from skillhub.recommend import build_recommendation, rank_skills, reload_note

_PKG = Path(__file__).resolve().parents[1]


def resolve_root() -> Path:
    """Repo root for registry, install scripts, and skill sources."""
    env = os.environ.get("SKILLHUB_ROOT")
    if env:
        p = Path(env).expanduser().resolve()
        if (p / "registry" / "skills.json").exists():
            return p
        sys.exit(f"SKILLHUB_ROOT invalid (missing registry): {p}")
    if (_PKG / "registry" / "skills.json").exists():
        return _PKG
    sys.exit(
        "Cannot find registry/skills.json. Clone awesome-agent-skill or set SKILLHUB_ROOT."
    )


def invoked_as_entry_point() -> bool:
    exe = Path(sys.argv[0]).name
    return exe == "skillhub" or exe.startswith("skillhub-")


REPO = resolve_root()
REGISTRY = REPO / "registry" / "skills.json"
BUNDLES = REPO / "registry" / "bundles.json"
FIXTURES = REPO / "registry" / "recommend-fixtures.json"
QUALITY = REPO / "registry" / "quality.json"


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



def cmd_search(args: argparse.Namespace) -> int:
    data = load_registry()
    ranked = rank_skills(data["skills"], args.query)
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
    result = subprocess.run(["bash", str(script), *argv], cwd=REPO)
    return result.returncode


def cmd_install(args: argparse.Namespace) -> int:
    script = REPO / "scripts" / "install" / "install-skill.sh"
    fmt_argv: list[str] = []
    if args.format:
        fmt_argv = ["--format", args.format]
    extra: list[str] = []
    if getattr(args, "dry_run", False):
        extra.append("--dry-run")
    if getattr(args, "plan_json", False):
        extra.append("--plan-json")
    if getattr(args, "no_overwrite", False):
        extra.append("--no-overwrite")
    if getattr(args, "backup", False):
        extra.append("--backup")
    return run_script(script, [args.skill_id, args.target, *fmt_argv, *extra])


def cmd_install_bundle(args: argparse.Namespace) -> int:
    script = REPO / "scripts" / "install" / "install-bundle.sh"
    fmt_argv: list[str] = []
    if args.format:
        fmt_argv = ["--format", args.format]
    extra: list[str] = []
    if getattr(args, "dry_run", False):
        extra.append("--dry-run")
    if getattr(args, "plan_json", False):
        extra.append("--plan-json")
    if getattr(args, "no_overwrite", False):
        extra.append("--no-overwrite")
    if getattr(args, "backup", False):
        extra.append("--backup")
    return run_script(script, [args.bundle_id, args.target, *fmt_argv, *extra])


def cmd_validate(_: argparse.Namespace) -> int:
    return subprocess.run([sys.executable, str(REPO / "scripts" / "validate-skills.py")], cwd=REPO).returncode


def cmd_recommend(args: argparse.Namespace) -> int:
    data = load_registry()
    bundles_data = load_bundles()
    fmt = args.format or "cursor"
    rec = build_recommendation(
        args.query,
        data["skills"],
        bundles_data["bundles"],
        limit=args.limit,
        fmt=fmt,
        pip_cli=invoked_as_entry_point(),
    )
    if args.json:
        print(json.dumps(rec, indent=2, ensure_ascii=False))
        return 0 if rec["skills"] else 1

    if not rec["skills"]:
        print("No recommendations", file=sys.stderr)
        return 1

    if rec.get("bundle"):
        b = rec["bundle"]
        print(f"Recommended bundle: {b['id']} — {b['title']}")
        print(f"  {b.get('description', '')}")
        if rec.get("install_bundle_command"):
            print(f"\nInstall:\n  {rec['install_bundle_command']}")
        if rec.get("full_workflow"):
            print(f"\nFull workflow (clone + install):\n  {rec['full_workflow']}")
        print()

    print("Top skills:")
    for item in rec["skills"]:
        reasons = ", ".join(item.get("reasons") or []) or "keyword match"
        print(f"  {item['score']:3d}  {item['id']}\t{item['name']}")
        print(f"       why: {reasons}")

    print(f"\nReload: {reload_note(fmt)}")
    return 0


def bundle_domains(bundle_id: str) -> set[str]:
    data = load_bundles()
    bundle = next((b for b in data["bundles"] if b["id"] == bundle_id), None)
    if not bundle:
        return set()
    return set(bundle.get("domains", []))


def cmd_quality(args: argparse.Namespace) -> int:
    gen = REPO / "scripts" / "generate-quality.py"
    if args.regenerate or not QUALITY.exists():
        r = subprocess.run([sys.executable, str(gen)], cwd=REPO)
        if r.returncode != 0:
            return r.returncode
    if not QUALITY.exists():
        print("quality.json missing", file=sys.stderr)
        return 1
    data = json.loads(QUALITY.read_text(encoding="utf-8"))
    rows = data["skills"]
    if args.low_only:
        rows = [r for r in rows if r["score"] < 50]
    rows.sort(key=lambda r: r["score"])
    for r in rows[: args.limit]:
        issues = ", ".join(r.get("issues", [])) or "-"
        print(f"{r['score']:3d}  {r['id']}\t{issues}")
    print(
        f"\navg={data.get('average_score')} low={data.get('low_score_count')}",
        file=sys.stderr,
    )
    return 0


def cmd_resolver_generate(_: argparse.Namespace) -> int:
    script = REPO / "scripts" / "generate-resolver.py"
    if not script.exists():
        print("generate-resolver.py missing", file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(script)], cwd=REPO).returncode


def cmd_pack(_: argparse.Namespace) -> int:
    script = REPO / "scripts" / "pack-skills.py"
    if not script.exists():
        print("pack-skills.py missing", file=sys.stderr)
        return 1
    return subprocess.run([sys.executable, str(script)], cwd=REPO).returncode


def cmd_eval_recommend(_: argparse.Namespace) -> int:
    if not FIXTURES.exists():
        print("Missing registry/recommend-fixtures.json", file=sys.stderr)
        return 1
    data = load_registry()
    fixtures = json.loads(FIXTURES.read_text(encoding="utf-8"))["fixtures"]
    k = 5
    hits = 0
    hits_at_1 = 0
    hits_at_3 = 0
    mrr_sum = 0.0
    for fx in fixtures:
        query = fx["query"]
        expect = set(fx.get("expect_any", []))
        ranked = rank_skills(data["skills"], query)
        top_ids = [s["id"] for _, s in ranked[:k]]
        found_rank: int | None = None
        for idx, (_sc, skill) in enumerate(ranked):
            if skill["id"] in expect:
                found_rank = idx + 1
                break
        ok = found_rank is not None and found_rank <= k
        if found_rank is not None:
            if found_rank <= 1:
                hits_at_1 += 1
            if found_rank <= 3:
                hits_at_3 += 1
            if found_rank <= 5:
                hits += 1
            mrr_sum += 1.0 / float(found_rank)
        mark = "PASS" if ok else "FAIL"
        print(f"[{mark}] {query}")
        if not ok:
            print(f"       expected any of: {', '.join(sorted(expect))}")
            print(f"       got top-{k}: {', '.join(top_ids[:3])}...")
    total = len(fixtures)
    rate_top5 = hits / total if total else 0.0
    rate_top1 = hits_at_1 / total if total else 0.0
    rate_top3 = hits_at_3 / total if total else 0.0
    mrr = mrr_sum / total if total else 0.0
    print(f"\n{hits}/{total} passed (top-{k} hit rate {rate_top5:.0%})")
    print(f"top-1={rate_top1:.0%} top-3={rate_top3:.0%} MRR={mrr:.3f}")
    return 0 if hits == len(fixtures) else 1


def cmd_sync(args: argparse.Namespace) -> int:
    scripts_dir = REPO / "scripts"
    steps: list[tuple[str, list[str]]] = []

    reg = scripts_dir / "generate-registry.py"
    if reg.exists():
        cmd = [sys.executable, str(reg)]
        if args.check:
            cmd.append("--check")
        steps.append(("generate-registry", cmd))

    qual = scripts_dir / "generate-quality.py"
    if qual.exists() and not args.check:
        steps.append(("generate-quality", [sys.executable, str(qual)]))

    cat = scripts_dir / "generate-catalog.py"
    if cat.exists() and not args.check:
        steps.append(("generate-catalog", [sys.executable, str(cat)]))

    val = scripts_dir / "validate-skills.py"
    if val.exists():
        steps.append(("validate-skills", [sys.executable, str(val)]))

    ok = True
    for label, cmd in steps:
        r = subprocess.run(cmd, cwd=REPO)
        status = "ok" if r.returncode == 0 else "FAIL"
        print(f"[{status}] {label}")
        if r.returncode != 0:
            ok = False
    return 0 if ok else 1


def cmd_doctor(args: argparse.Namespace) -> int:
    ok = True
    results: list[dict[str, object]] = []

    def check(label: str, passed: bool, detail: str = "") -> None:
        nonlocal ok
        passed_bool = bool(passed)
        status = "ok" if passed_bool else "FAIL"
        if not passed_bool:
            ok = False
        entry = {"label": label, "passed": passed_bool, "detail": detail}
        results.append(entry)
        if not args.json:
            line = f"[{status}] {label}"
            if detail:
                line += f" — {detail}"
            print(line)

    check("registry/skills.json", REGISTRY.exists())
    check("registry/bundles.json", BUNDLES.exists())
    if REGISTRY.exists():
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "generate-registry.py"), "--check"],
            cwd=REPO,
            capture_output=True,
            text=True,
        )
        check("registry sync", r.returncode == 0, r.stderr.strip() or r.stdout.strip())

        # Count drift checks: .cursor vs registry vs README badge vs metrics snapshot.
        try:
            data = load_registry()
            registry_count = int(data.get("count", 0))
        except Exception:
            registry_count = -1

        cursor_root = REPO / ".cursor" / "skills"
        cursor_count = len(list(cursor_root.rglob("SKILL.md"))) if cursor_root.exists() else -1
        check(
            "count: cursor vs registry",
            cursor_count == registry_count and cursor_count >= 0,
            f"cursor={cursor_count}, registry={registry_count}",
        )

        readme = REPO / "README.md"
        readme_count = None
        if readme.exists():
            m = re.search(r"skills-(\d+)-", readme.read_text(encoding="utf-8"))
            if m:
                readme_count = int(m.group(1))
                check(
                    "count: README badge vs registry",
                    readme_count == registry_count,
                    f"readme={readme_count}, registry={registry_count}",
                )

        metrics_path = REPO / "docs" / "metrics" / "2026-05.md"
        if metrics_path.exists():
            m = re.search(
                r"Cursor `SKILL\.md` files:\s*\*\*(\d+)\*\*",
                metrics_path.read_text(encoding="utf-8"),
            )
            if m:
                metrics_count = int(m.group(1))
                check(
                    "count: metrics vs registry",
                    metrics_count == registry_count,
                    f"metrics={metrics_count}, registry={registry_count}",
                )

    for name in ("install-domain.sh", "install-bundle.sh", "install-skill.sh"):
        p = REPO / "scripts" / "install" / name
        check(name, p.exists() and p.stat().st_mode & 0o111)

    v = subprocess.run([sys.executable, str(REPO / "scripts" / "validate-skills.py")], cwd=REPO, capture_output=True)
    check("validate-skills.py", v.returncode == 0, "see output above" if v.returncode else "")

    catalog_index = REPO / "catalog" / "index.html"
    check("catalog/index.html", catalog_index.exists())
    check("catalog/assets/app.js", (REPO / "catalog" / "assets" / "app.js").exists())

    if getattr(args, "target", None):
        target = Path(args.target).expanduser().resolve()
        check("install target exists", target.is_dir(), str(target))
        if target.is_dir():
            check(
                "install target writable",
                os.access(target, os.W_OK),
                str(target),
            )

    if args.json:
        print(
            json.dumps(
                {
                    "ok": ok,
                    "checks": results,
                },
                indent=2,
                ensure_ascii=False,
            )
        )

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

    rc = sub.add_parser("recommend", help="Recommend skills for a task description")
    rc.add_argument("query")
    rc.add_argument("-n", "--limit", type=int, default=8)
    rc.add_argument("--bundle", help="Deprecated: bundle is auto-suggested")
    rc.add_argument("--format", choices=["cursor", "claude", "both"], default="cursor")
    rc.add_argument("--json", action="store_true", help="Structured JSON output")
    rc.set_defaults(func=cmd_recommend)

    ev = sub.add_parser("eval-recommend", help="Run recommendation fixture eval")
    ev.set_defaults(func=cmd_eval_recommend)

    ql = sub.add_parser("quality", help="List skill quality scores")
    ql.add_argument("--regenerate", action="store_true", help="Run generate-quality.py first")
    ql.add_argument("--low-only", action="store_true")
    ql.add_argument("-n", "--limit", type=int, default=20)
    ql.set_defaults(func=cmd_quality)

    sh = sub.add_parser("show", help="Show skill metadata as JSON")
    sh.add_argument("skill_id")
    sh.set_defaults(func=cmd_show)

    bd = sub.add_parser("bundles", help="List install bundles")
    bd.add_argument("-v", "--verbose", action="store_true")
    bd.set_defaults(func=cmd_bundles)

    rv = sub.add_parser("resolver-generate", help="Generate compact resolver markdown")
    rv.set_defaults(func=cmd_resolver_generate)

    ins = sub.add_parser("install", help="Install one skill into a project")
    ins.add_argument("skill_id")
    ins.add_argument("target")
    ins.add_argument("--format", choices=["cursor", "claude", "both"], default="both")
    ins.add_argument("--dry-run", action="store_true", help="Show what would be installed without writing")
    ins.add_argument("--plan-json", action="store_true", help="Print JSON install plan instead of writing")
    ins.add_argument("--no-overwrite", action="store_true", help="Fail if target already has this skill")
    ins.add_argument("--backup", action="store_true", help="Backup existing skill before overwriting")
    ins.set_defaults(func=cmd_install)

    ib = sub.add_parser("install-bundle", help="Install a bundle into a project")
    ib.add_argument("bundle_id")
    ib.add_argument("target")
    ib.add_argument("--format", choices=["cursor", "claude", "both"], default="both")
    ib.add_argument("--dry-run", action="store_true", help="Show what would be installed without writing")
    ib.add_argument("--plan-json", action="store_true", help="Print JSON install plan instead of writing")
    ib.add_argument("--no-overwrite", action="store_true", help="Fail if target already has any of these skills")
    ib.add_argument("--backup", action="store_true", help="Backup existing skills before overwriting")
    ib.set_defaults(func=cmd_install_bundle)

    val = sub.add_parser("validate", help="Run skill validation")
    val.set_defaults(func=cmd_validate)

    pk = sub.add_parser("pack", help="Create deterministic skillpack tarball")
    pk.set_defaults(func=cmd_pack)

    doc = sub.add_parser("doctor", help="Check registry, install scripts, validation")
    doc.add_argument("--json", action="store_true", help="Output machine-readable JSON")
    doc.add_argument("--target", help="Optional install target directory to validate")
    doc.set_defaults(func=cmd_doctor)

    sync = sub.add_parser("sync", help="Regenerate registry/quality/catalog and validate")
    sync.add_argument(
        "--check",
        action="store_true",
        help="Use lightweight checks when available instead of full regeneration",
    )
    sync.set_defaults(func=cmd_sync)

    return p


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
