#!/usr/bin/env bash
# Finance sheet lane — cascade (optional) → build transparent sheets → publish to Drive.
# Closes PR #50 loop: Grok runs build→publish without a Tasklet round-trip.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FINANCE="$ROOT/finance"
FINANCE_MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
SEAL_TAG="${SEAL_TAG:-#79ba-finance-sheet-refresh}"
PARTNERS="${PARTNERS:-}"
RUN_CASCADE="${RUN_CASCADE:-0}"
DRY_RUN="${DRY_RUN:-0}"

mkdir -p "$RECAL"

engine_partner() {
  python3 -c "from finance.partner_keys import engine_partner; print(engine_partner('$1'))"
}

cascade_partner() {
  local p="$1"
  local engine
  engine="$(engine_partner "$p")"
  echo "  [$p] cascade (engine=$engine)"
  python3 "$FINANCE_MODEL/aggregate.py" --partner "$engine" --json "$RECAL/agg-$p.json"
  python3 "$FINANCE_MODEL/growth.py" --partner "$engine" --agg "$RECAL/agg-$p.json" --json "$RECAL/growth-$p.json"
}

if [[ "$RUN_CASCADE" == "1" ]]; then
  echo "→ Finance cascade (agg only — sheets read agg-*.json)"
  if [[ -n "$PARTNERS" ]]; then
    IFS=',' read -ra TARGETS <<< "$PARTNERS"
  else
    TARGETS=(grab bolt yango careem jih-global qatar red-sea-global saudi-pif)
  fi
  for p in "${TARGETS[@]}"; do
    p="${p// /}"
    [[ -z "$p" ]] && continue
    cascade_partner "$p"
  done
fi

echo "→ Build + publish transparent sheets + master tracker"
REFRESH_ARGS=()
if [[ -n "$PARTNERS" ]]; then
  REFRESH_ARGS+=(--partners "$PARTNERS")
fi
if [[ "$DRY_RUN" == "1" ]]; then
  REFRESH_ARGS+=(--dry-run)
fi
python3 "$FINANCE/refresh_all_sheets.py" "${REFRESH_ARGS[@]}"

echo "✓ finance sheet lane: $SEAL_TAG"