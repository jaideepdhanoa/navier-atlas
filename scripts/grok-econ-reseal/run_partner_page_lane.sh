#!/usr/bin/env bash
# Canonical partner-page lane (schema → use-cases → inherit bind → spine parity → relink → page QA → build-site).
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
INHERIT_ARGS=(--bind)
PARITY_ARGS=()
QA_ARGS=()
if [ -n "$PARTNERS" ]; then
  # shellcheck disable=SC2206
  RELINK_ARGS+=(--partner $PARTNERS)
  # shellcheck disable=SC2206
  INHERIT_ARGS+=(--partner $PARTNERS)
  # shellcheck disable=SC2206
  PARITY_ARGS=(--partner $PARTNERS)
  # shellcheck disable=SC2206
  QA_ARGS+=(--partner $PARTNERS)
else
  INHERIT_ARGS+=(--all)
  PARITY_ARGS=(--all)
fi
if [ "$WRITE_TASKLET" -eq 1 ]; then
  QA_ARGS+=(--write-tasklet-note)
fi
if [ "$FAIL_ON_WARN" -eq 1 ]; then
  QA_ARGS+=(--fail-on-warn)
fi

echo "=== Partner page lane ==="
echo "  1/8 schema validation"
python3 "$ROOT/scripts/validate_partner_proposals.py"

echo "  2/8 use-case completeness"
if [ -n "$PARTNERS" ]; then
  # shellcheck disable=SC2206
  python3 "$ROOT/scripts/audit_partner_proposal_use_cases.py" --partner $PARTNERS
else
  python3 "$ROOT/scripts/audit_partner_proposal_use_cases.py" --warn-only
fi

echo "  3/8 regional spine inherit bind"
python3 "$ROOT/scripts/grok-econ-reseal/inherit_regional_spine.py" "${INHERIT_ARGS[@]}"

echo "  4/8 spine parity audit"
python3 "$ROOT/scripts/audit_partner_spine_parity.py" "${PARITY_ARGS[@]}"

echo "  5/8 journey + featured re-link"
python3 "$ROOT/scripts/relink_partner_journeys.py" "${RELINK_ARGS[@]}"

echo "  6/8 page completeness + linkability QA"
if [ ${#QA_ARGS[@]} -gt 0 ]; then
  python3 "$ROOT/scripts/audit_partner_page_qa.py" "${QA_ARGS[@]}"
else
  python3 "$ROOT/scripts/audit_partner_page_qa.py"
fi

echo "  7/8 build-site smoke"
node "$ROOT/scripts/build-site.mjs" 2>&1 | tail -8

echo "  8/8 partner tracker sheet"
python3 "$ROOT/finance/build_partner_tracker.py" --upload

echo "✓ Partner page lane complete"