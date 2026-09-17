#!/usr/bin/env bash
# Stage the toolkit on local storage: cloud-mounted folders may not support
# package-manager symlinks or atomic directory renames.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")" && pwd)"
MODE="${1:-}"; [ -n "$MODE" ] || { echo 'Usage: bash run.sh build|test|schema|init|review|check-sources [arguments]'; exit 1; }
shift
RUNTIME="$(mktemp -d "${TMPDIR:-/tmp}/navier-brief-runtime.XXXXXX")"
trap 'rm -rf "$RUNTIME"' EXIT
# Never drag build outputs or dependency trees into the disposable runtime.
tar -C "$ROOT" --exclude=node_modules --exclude=.git --exclude=exports --exclude='exports-archive-*' -cf - . | tar -C "$RUNTIME" -xf -
if [ -f "$RUNTIME/bun.lock" ]; then
  (cd "$RUNTIME" && bun install --frozen-lockfile --ignore-scripts >/dev/null)
else
  (cd "$RUNTIME" && bun install --ignore-scripts >/dev/null)
fi
case "$MODE" in
 build) bun "$RUNTIME/scripts/build.ts" "$@" ;;
 test) (cd "$RUNTIME" && bun test "$@") ;;
 schema) bun "$RUNTIME/scripts/schema.ts" "${1:-$ROOT/content.schema.json}" ;;
 init) bun "$RUNTIME/scripts/init.ts" "$@" ;;
 review) bun "$RUNTIME/scripts/record-review.ts" "$@" ;;
 check-sources) bun "$RUNTIME/scripts/check-sources.ts" "$@" ;;
 *) echo "Unknown command: $MODE" >&2; exit 1 ;;
esac
