#!/usr/bin/env python3
"""Create deterministic skillpack tarball from the current registry and skills."""

from __future__ import annotations

import json
import tarfile
from pathlib import Path
from io import BytesIO

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "skills.json"
BUNDLES = ROOT / "registry" / "bundles.json"
OUT_DIR = ROOT / "dist"
MANIFEST = ROOT / "registry" / "manifest.json"


def add_file(tar: tarfile.TarFile, path: Path, arcname: str) -> None:
    data = path.read_bytes()
    info = tarfile.TarInfo(name=arcname)
    info.size = len(data)
    info.mtime = 0  # deterministic
    info.mode = 0o644
    tar.addfile(info, BytesIO(data))


def main() -> int:
    if not REGISTRY.exists():
        raise SystemExit("registry/skills.json missing; run generate-registry.py first")

    data = json.loads(REGISTRY.read_text(encoding="utf-8"))
    skills = data.get("skills", [])

    manifest_body: dict = {
        "schema_version": 1,
        "registry_schema_version": data.get("schema_version"),
        "count": data.get("count"),
        "paths": [
            "registry/skills.json",
            "registry/bundles.json",
            ".cursor/skills/**",
        ],
    }
    gstack_sync = ROOT / "registry" / "gstack-sync.json"
    if gstack_sync.exists():
        gs = json.loads(gstack_sync.read_text(encoding="utf-8"))
        manifest_body["gstack_version"] = gs.get("upstream_version")
        manifest_body["gstack_commit"] = gs.get("upstream_commit")
        manifest_body["gstack_synced_at"] = gs.get("synced_at")
        manifest_body["gstack_skill_count"] = gs.get("local_skill_count")
    elif MANIFEST.exists():
        existing = json.loads(MANIFEST.read_text(encoding="utf-8"))
        for key in ("gstack_version", "gstack_commit", "gstack_synced_at", "gstack_skill_count"):
            if key in existing:
                manifest_body[key] = existing[key]

    MANIFEST.write_text(
        json.dumps(manifest_body, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    tar_path = OUT_DIR / "skillpack.tar"

    with tarfile.open(tar_path, "w") as tar:
        # registry
        for p in sorted([REGISTRY, BUNDLES] if BUNDLES.exists() else [REGISTRY]):
            rel = p.relative_to(ROOT).as_posix()
            add_file(tar, p, rel)

        # skills tree (cursor only; claude is derivable)
        skills_root = ROOT / ".cursor" / "skills"
        if skills_root.exists():
            files = sorted(skills_root.rglob("*"))
            for f in files:
                if f.is_dir():
                    continue
                rel = f.relative_to(ROOT).as_posix()
                add_file(tar, f, rel)

        add_file(tar, MANIFEST, "registry/manifest.json")

    print(f"Wrote deterministic skillpack tarball to {tar_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

