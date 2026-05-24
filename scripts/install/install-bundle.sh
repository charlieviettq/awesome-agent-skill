#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage: install-bundle.sh <bundle> <target-project> [--format cursor|claude|both]

Bundles:
  starter   core-workflow + security-appsec + reliability-ops
  full      all top-level domains
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

case "${BUNDLE}" in
  starter)
    DOMAINS="core-workflow security-appsec reliability-ops"
    ;;
  full)
    DOMAINS="$(find "${REPO_ROOT}/.cursor/skills" -mindepth 1 -maxdepth 1 -type d -exec basename {} \; | sort | tr '\n' ' ')"
    ;;
  *)
    echo "Unknown bundle: ${BUNDLE}" >&2
    exit 1
    ;;
esac

for domain in ${DOMAINS}; do
  bash "${INSTALL}" "${domain}" "${TARGET}" --format "${FORMAT}"
done

echo "Bundle '${BUNDLE}' installed into ${TARGET}"
