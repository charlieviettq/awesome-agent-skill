#!/usr/bin/env bash
# Pull latest skills/CLI/catalog from public awesome-agent-skill upstream.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if ! git remote get-url upstream &>/dev/null; then
  echo "Add upstream remote first:"
  echo "  git remote add upstream git@github.com:charlieviettq/awesome-agent-skill.git"
  exit 1
fi

git fetch upstream
git merge upstream/main -m "chore: sync from awesome-agent-skill upstream" || {
  echo "Merge conflicts — resolve manually, preserve docs/ and registry commercial bundles."
  exit 1
}

# Re-merge commercial bundles if upstream overwrote bundles.json
if [[ -f registry/commercial-bundles.json ]]; then
  python3 << 'PY'
import json
from pathlib import Path

bundles_path = Path("registry/bundles.json")
commercial_path = Path("registry/commercial-bundles.json")
main = json.loads(bundles_path.read_text())
commercial = json.loads(commercial_path.read_text())
existing_ids = {b["id"] for b in main["bundles"]}
for bundle in commercial.get("bundles", []):
    if bundle["id"] not in existing_ids:
        full_idx = next(
            (i for i, b in enumerate(main["bundles"]) if b["id"] == "full"),
            len(main["bundles"]),
        )
        main["bundles"].insert(full_idx, bundle)
bundles_path.write_text(json.dumps(main, indent=2) + "\n")
print("Re-applied commercial bundles")
PY
fi

echo "Sync complete. Run: python3 scripts/skillhub.py sync"
