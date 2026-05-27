#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-skill.sh <skill-id> <target-project> [--format cursor|claude|both] [--dry-run] [--plan-json] [--no-overwrite] [--backup]

Example:
  install-skill.sh core-workflow/verify-before-done ~/my-app --format cursor
EOF
}

if [[ $# -lt 2 ]]; then
  usage
  exit 1
fi

SKILL_ID="$1"
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
SRC="${REPO_ROOT}/.cursor/skills/${SKILL_ID}"
CLAUDE_SRC="${REPO_ROOT}/.claude/skills/${SKILL_ID}"

if [[ ! -d "${SRC}" ]]; then
  echo "Skill not found: ${SKILL_ID}" >&2
  exit 1
fi

CURSOR_DEST="${TARGET}/.cursor/skills/${SKILL_ID}"
CLAUDE_DEST="${TARGET}/.claude/skills/${SKILL_ID}"

if [[ "${PLAN_JSON}" -eq 1 ]]; then
  cat <<EOF
{
  "skill_id": "${SKILL_ID}",
  "target": "${TARGET}",
  "format": "${FORMAT}",
  "operations": [
    {
      "op": "copy_tree",
      "from": "${SRC}",
      "to": "${CURSOR_DEST}",
      "kind": "cursor"
    },
    {
      "op": "copy_tree",
      "from": "${CLAUDE_SRC}",
      "to": "${CLAUDE_DEST}",
      "kind": "claude",
      "conditional": true
    }
  ]
}
EOF
  exit 0
fi

mkdir -p "${TARGET}/.cursor/skills" "${TARGET}/.claude/skills"

backup_dir() {
  local src="$1"
  local rel="$2"
  local root="${TARGET}/.skillhub-backup/$(date +%Y%m%d%H%M%S)"
  mkdir -p "${root}/$(dirname "${rel}")"
  if [[ -d "${src}" ]]; then
    cp -R "${src}" "${root}/${rel}"
  fi
}

if [[ "${FORMAT}" == "cursor" || "${FORMAT}" == "both" ]]; then
  if [[ -d "${CURSOR_DEST}" ]]; then
    if [[ "${NO_OVERWRITE}" -eq 1 ]]; then
      echo "Refusing to overwrite existing skill at ${CURSOR_DEST} (use --no-overwrite=0 or remove first)" >&2
      exit 1
    fi
    if [[ "${BACKUP}" -eq 1 && "${DRY_RUN}" -eq 0 ]]; then
      backup_dir "${CURSOR_DEST}" ".cursor/skills/${SKILL_ID}"
    fi
  fi
  echo "Plan: install Cursor skill ${SKILL_ID} -> ${CURSOR_DEST}"
  if [[ "${DRY_RUN}" -eq 0 ]]; then
    rm -rf "${CURSOR_DEST}"
    mkdir -p "$(dirname "${CURSOR_DEST}")"
    cp -R "${SRC}" "${CURSOR_DEST}"
  fi
fi

if [[ "${FORMAT}" == "claude" || "${FORMAT}" == "both" ]]; then
  if [[ -d "${CLAUDE_SRC}" ]]; then
    if [[ -d "${CLAUDE_DEST}" ]]; then
      if [[ "${NO_OVERWRITE}" -eq 1 ]]; then
        echo "Refusing to overwrite existing Claude skill at ${CLAUDE_DEST}" >&2
        exit 1
      fi
      if [[ "${BACKUP}" -eq 1 && "${DRY_RUN}" -eq 0 ]]; then
        backup_dir "${CLAUDE_DEST}" ".claude/skills/${SKILL_ID}"
      fi
    fi
    echo "Plan: install Claude skill ${SKILL_ID} -> ${CLAUDE_DEST}"
    if [[ "${DRY_RUN}" -eq 0 ]]; then
      rm -rf "${CLAUDE_DEST}"
      mkdir -p "$(dirname "${CLAUDE_DEST}")"
      cp -R "${CLAUDE_SRC}" "${CLAUDE_DEST}"
    fi
  fi
fi

if [[ "${DRY_RUN}" -eq 1 ]]; then
  echo "Dry-run complete for skill ${SKILL_ID} into ${TARGET}"
else
  echo "Installed skill ${SKILL_ID} into ${TARGET}"
fi
