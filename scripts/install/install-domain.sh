#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-domain.sh <domain> <target-project> [--format cursor|claude|both] [--dry-run] [--plan-json] [--no-overwrite] [--backup]

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
shift 2

FORMAT="cursor"
DRY_RUN=0
PLAN_JSON=0
NO_OVERWRITE=0
BACKUP=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      FORMAT="${2:-cursor}"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    --plan-json)
      PLAN_JSON=1
      DRY_RUN=1
      shift
      ;;
    --no-overwrite)
      NO_OVERWRITE=1
      shift
      ;;
    --backup)
      BACKUP=1
      shift
      ;;
    *)
      echo "Unknown option: $1" >&2
      usage
      exit 1
      ;;
  esac
done

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SOURCE="${REPO_ROOT}/.cursor/skills/${DOMAIN}"

if [[ ! -d "${SOURCE}" ]]; then
  echo "Domain not found: ${DOMAIN}" >&2
  exit 1
fi

if [[ "${PLAN_JSON}" -eq 1 ]]; then
  cat <<EOF
{
  "domain": "${DOMAIN}",
  "target": "${TARGET}",
  "format": "${FORMAT}"
}
EOF
  exit 0
fi

mkdir -p "${TARGET}"

backup_dir() {
  local src="$1"
  local rel="$2"
  local root="${TARGET}/.skillhub-backup/$(date +%Y%m%d%H%M%S)"
  mkdir -p "${root}/$(dirname "${rel}")"
  if [[ -d "${src}" ]]; then
    cp -R "${src}" "${root}/${rel}"
  fi
}

install_cursor() {
  mkdir -p "${TARGET}/.cursor/skills"
  local dest="${TARGET}/.cursor/skills/${DOMAIN}"
  if [[ -d "${dest}" ]]; then
    if [[ "${NO_OVERWRITE}" -eq 1 ]]; then
      echo "Refusing to overwrite existing domain at ${dest}" >&2
      exit 1
    fi
    if [[ "${BACKUP}" -eq 1 && "${DRY_RUN}" -eq 0 ]]; then
      backup_dir "${dest}" ".cursor/skills/${DOMAIN}"
    fi
  fi
  echo "Plan: install Cursor domain ${DOMAIN} -> ${dest}"
  if [[ "${DRY_RUN}" -eq 0 ]]; then
    rsync -a "${SOURCE}/" "${dest}/"
    echo "Installed Cursor skills: ${DOMAIN}"
  fi
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
