#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-bundle.sh <bundle> <target-project> [--format cursor|claude|both] [--dry-run] [--plan-json] [--no-overwrite] [--backup]

Bundles are defined in registry/bundles.json (starter, ship-ready, agent-builder, data-scientist, security-reviewer, full).
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

BUNDLE="$1"
TARGET="$2"
shift 2

FORMAT="both"
DRY_RUN=0
PLAN_JSON=0
NO_OVERWRITE=0
BACKUP=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --format)
      FORMAT="${2:-both}"
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
INSTALL="${SCRIPT_DIR}/install-domain.sh"

INSTALL_SKILL="${SCRIPT_DIR}/install-skill.sh"
RESOLVE="${REPO_ROOT}/scripts/resolve-bundle.py"

if ! PLAN="$(python3 "${RESOLVE}" "${BUNDLE}")"; then
  exit 1
fi

if [[ "${PLAN_JSON}" -eq 1 ]]; then
  # High-level bundle plan only; per-skill plans can be obtained by calling install-skill with --plan-json.
  cat <<EOF
{
  "bundle": "${BUNDLE}",
  "target": "${TARGET}",
  "format": "${FORMAT}",
  "note": "Detailed per-skill plans are available via install-skill.sh --plan-json"
}
EOF
  exit 0
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
      if [[ "${DRY_RUN}" -eq 1 ]]; then
        echo "Plan: install skill ${value} from bundle ${BUNDLE}"
      else
        extra=()
        if [[ "${NO_OVERWRITE}" -eq 1 ]]; then
          extra+=(--no-overwrite)
        fi
        if [[ "${BACKUP}" -eq 1 ]]; then
          extra+=(--backup)
        fi
        bash "${INSTALL_SKILL}" "${value}" "${TARGET}" --format "${FORMAT}" "${extra[@]}"
      fi
      ;;
    *)
      echo "Unknown plan entry: ${line}" >&2
      exit 1
      ;;
  esac
done <<< "${PLAN}"

echo "Bundle '${BUNDLE}' installed into ${TARGET}"
