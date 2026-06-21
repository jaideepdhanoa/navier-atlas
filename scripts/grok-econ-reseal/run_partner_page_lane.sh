#!/usr/bin/env bash
# Canonical partner-page lane (schema → use-cases → relink → page QA → build-site).
#
# Usage:
#   ./scripts/grok-econ-reseal/run_partner_page_lane.sh
#   PARTNERS="rapido ola noon careem" ./scripts/grok-econ-reseal/run_partner_page_lane.sh
#   ./scripts/grok-econ-reseal/run_partner_page_lane.sh --write-tasklet-note
#   ./scripts/grok-econ-reseal/run_partner_page_lane.sh --fail-on-warn
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PARTNERS="${PARTNERS:-}"
WRITE_TASKLET=0
FAIL_ON_WARN=0
EXTRA_ARGS=()

while [ $# -gt 0 ]; do
  case "$1" in
    --write-tasklet-note) WRITE_TASKLET=1 ;;
    --fail-on-warn) FAIL_ON_WARN=1 ;;
    --partner)
      shift
      PARTNERS="${1:-}"
      ;;
    *)
      EXTRA_ARGS+=("$1")
      ;;
  esac
  shift || true
done

RELINK_ARGS=(--apply)
QA_ARGS=()
if [ -n "$PARTNERS" ]; then
  # shellcheck disable=SC2206
  RELINK_ARGS+=(--partner $PARTNERS)
  # shellcheck disable=SC2206
  QA_ARGS+=(--partner $PARTNERS)
fi
if [ "$WRITE_TASKLET" -eq 1 ]; then
  QA_ARGS+=(--write-tasklet-note)
fi
if [ "$FAIL_ON_WARN" -eq 1 ]; then
  QA_ARGS+=(--fail-on-warn)
fi

echo "=== Partner page lane ==="
echo "  1/5 schema validation"
python3 "$ROOT/scripts/validate_partner_proposals.py"

echo "  2/5 use-case completeness"
UC_ARGS=()
if [ -n "$PARTNERS" ]; then
  # shellcheck disable=SC2206
  UC_ARGS=(--partner $PARTNERS)
fi
python3 "$ROOT/scripts/audit_partner_proposal_use_cases.py" "${UC_ARGS[@]}"

echo "  3/5 journey + featured re-link"
python3 "$ROOT/scripts/relink_partner_journeys.py" "${RELINK_ARGS[@]}"

echo "  4/5 page completeness + linkability QA"
python3 "$ROOT/scripts/audit_partner_page_qa.py" "${QA_ARGS[@]}"

echo "  5/5 build-site smoke"
node "$ROOT/scripts/build-site.mjs" 2>&1 | tail -8

echo "✓ Partner page lane complete"