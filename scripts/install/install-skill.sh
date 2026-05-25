#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-skill.sh <skill-id> <target-project> [--format cursor|claude|both]

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
FORMAT="both"
if [[ "${3:-}" == "--format" && -n "${4:-}" ]]; then
  FORMAT="$4"
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/../.." && pwd)"
SRC="${REPO_ROOT}/.cursor/skills/${SKILL_ID}"
CLAUDE_SRC="${REPO_ROOT}/.claude/skills/${SKILL_ID}"

if [[ ! -d "${SRC}" ]]; then
  echo "Skill not found: ${SKILL_ID}" >&2
  exit 1
fi

mkdir -p "${TARGET}/.cursor/skills" "${TARGET}/.claude/skills"

if [[ "${FORMAT}" == "cursor" || "${FORMAT}" == "both" ]]; then
  rm -rf "${TARGET}/.cursor/skills/${SKILL_ID}"
  mkdir -p "$(dirname "${TARGET}/.cursor/skills/${SKILL_ID}")"
  cp -R "${SRC}" "${TARGET}/.cursor/skills/${SKILL_ID}"
fi

if [[ "${FORMAT}" == "claude" || "${FORMAT}" == "both" ]]; then
  if [[ -d "${CLAUDE_SRC}" ]]; then
    rm -rf "${TARGET}/.claude/skills/${SKILL_ID}"
    mkdir -p "$(dirname "${TARGET}/.claude/skills/${SKILL_ID}")"
    cp -R "${CLAUDE_SRC}" "${TARGET}/.claude/skills/${SKILL_ID}"
  fi
fi

echo "Installed skill ${SKILL_ID} into ${TARGET}"
