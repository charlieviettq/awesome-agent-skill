#!/usr/bin/env bash
# Bootstrap SpecFlow AI private commercial repo from awesome-agent-skill.
# Usage: bash scripts/bootstrap-specflow-ai.sh [target-dir]
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
PERSONAL_RESEARCH="${PERSONAL_RESEARCH:-$HOME/Documents/OtherProject/personal-research}"
TARGET="${1:-$PERSONAL_RESEARCH/specflow-ai}"

if [[ -d "$TARGET/.git" ]]; then
  echo "Target already exists: $TARGET"
  echo "Run sync-from-upstream.sh inside specflow-ai instead."
  exit 1
fi

echo "==> Cloning awesome-agent-skill -> specflow-ai"
git clone --local "$SOURCE_REPO" "$TARGET"

cd "$TARGET"

# Remove public-only remote if it points to awesome-agent-skill; user adds private remote
git remote rename origin upstream 2>/dev/null || true

echo "==> Applying SpecFlow AI commercial overlay"
OVERLAY="$SOURCE_REPO/specflow-ai-overlay"
if [[ -d "$OVERLAY" ]]; then
  rsync -a "$OVERLAY/" "$TARGET/"
fi

# Merge commercial bundles into registry
if [[ -f "$TARGET/registry/commercial-bundles.json" ]]; then
  python3 << 'PY'
import json
from pathlib import Path

root = Path(".")
bundles_path = root / "registry" / "bundles.json"
commercial_path = root / "registry" / "commercial-bundles.json"

main = json.loads(bundles_path.read_text())
commercial = json.loads(commercial_path.read_text())

existing_ids = {b["id"] for b in main["bundles"]}
for bundle in commercial.get("bundles", []):
    if bundle["id"] not in existing_ids:
        # Insert before "full" bundle
        full_idx = next(
            (i for i, b in enumerate(main["bundles"]) if b["id"] == "full"),
            len(main["bundles"]),
        )
        main["bundles"].insert(full_idx, bundle)
        existing_ids.add(bundle["id"])

bundles_path.write_text(json.dumps(main, indent=2) + "\n")
print("Merged commercial bundles into registry/bundles.json")
PY
fi

git add -A
git commit -m "chore: bootstrap SpecFlow AI commercial workbench" || true

cat << EOF

SpecFlow AI bootstrap complete: $TARGET

Next steps:
  1. cd "$TARGET"
  2. git remote add origin git@github.com:charlieviettq/specflow-ai.git
  3. git push -u origin main
  4. python3 scripts/skillhub.py sync   # if using catalog/registry locally

Public repo remains: $SOURCE_REPO
Pull upstream: bash scripts/sync-from-upstream.sh (from specflow-ai)
EOF
