#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-bundle.sh <bundle> <target-project> [--format cursor|claude|both]

Bundles are defined in registry/bundles.json (starter, ship-ready, agent-builder, data-scientist, security-reviewer, full).
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

BUNDLE="$1"
TARGET="$2"
FORMAT="both"
if [[ "${3:-}" == "--format" && -n "${4:-}" ]]; then
  FORMAT="$4"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
INSTALL="${SCRIPT_DIR}/install-domain.sh"

INSTALL_SKILL="${SCRIPT_DIR}/install-skill.sh"
RESOLVE="${REPO_ROOT}/scripts/resolve-bundle.py"

if ! PLAN="$(python3 "${RESOLVE}" "${BUNDLE}")"; then
  exit 1
fi

while IFS= read -r line; do
  [[ -z "${line}" ]] && continue
  kind="${line%%:*}"
  value="${line#*:}"
  case "${kind}" in
    domain)
      bash "${INSTALL}" "${value}" "${TARGET}" --format "${FORMAT}"
      ;;
    skill)
      bash "${INSTALL_SKILL}" "${value}" "${TARGET}" --format "${FORMAT}"
      ;;
    *)
      echo "Unknown plan entry: ${line}" >&2
      exit 1
      ;;
  esac
done <<< "${PLAN}"

echo "Bundle '${BUNDLE}' installed into ${TARGET}"
