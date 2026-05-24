#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-domain.sh <domain> <target-project> [--format cursor|claude|both]

Examples:
  ./scripts/install/install-domain.sh core-workflow ~/my-app --format cursor
  ./scripts/install/install-domain.sh security-appsec ~/my-app --format both
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

DOMAIN="$1"
TARGET="$2"
FORMAT="cursor"
if [[ "${3:-}" == "--format" && -n "${4:-}" ]]; then
  FORMAT="$4"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SOURCE="${REPO_ROOT}/.cursor/skills/${DOMAIN}"

if [[ ! -d "${SOURCE}" ]]; then
  echo "Domain not found: ${DOMAIN}" >&2
  exit 1
fi

mkdir -p "${TARGET}"

install_cursor() {
  mkdir -p "${TARGET}/.cursor/skills"
  rsync -a "${SOURCE}/" "${TARGET}/.cursor/skills/${DOMAIN}/"
  echo "Installed Cursor skills: ${DOMAIN}"
}

install_claude() {
  mkdir -p "${TARGET}/.claude/skills"
  while IFS= read -r name; do
    [[ -z "${name}" ]] && continue
    if [[ -d "${REPO_ROOT}/.claude/skills/${name}" ]]; then
      rsync -a "${REPO_ROOT}/.claude/skills/${name}/" "${TARGET}/.claude/skills/${name}/"
    fi
  done < <(python3 - "${DOMAIN}" "${REPO_ROOT}" <<'PY'
import json, sys
from pathlib import Path
domain, repo = sys.argv[1], Path(sys.argv[2])
data = json.loads((repo / "scripts/claude-skill-map.json").read_text())
for item in data.get("mappings", []):
    path = item["cursor_path"]
    if path == domain or path.startswith(domain + "/"):
        print(item["claude_name"])
PY
)
  echo "Installed Claude skills for domain: ${DOMAIN}"
}

case "${FORMAT}" in
  cursor) install_cursor ;;
  claude) install_claude ;;
  both)
    install_cursor
    install_claude
    ;;
  *)
    echo "Unknown format: ${FORMAT}" >&2
    exit 1
    ;;
esac

echo "Reload your agent session to pick up new skills."
