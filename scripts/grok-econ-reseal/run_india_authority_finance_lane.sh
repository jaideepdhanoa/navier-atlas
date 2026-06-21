#!/usr/bin/env bash
# India KCC + extension markets finance cascade (rapido, ola, uber-india)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
PARTNERS="rapido,ola,uber-india-derivative"
mkdir -p "$RECAL"

echo "→ Patch India corridors (incl. Kolkata/Chennai spine rows)"
python3 "$ROOT/scripts/grok-econ-reseal/build_india_noon_corridor_markets.py"
python3 "$ROOT/scripts/grok-econ-reseal/build_india_kcc_corridor_markets.py"

IFS=',' read -ra TARGETS <<< "$PARTNERS"
for p in "${TARGETS[@]}"; do
  engine="$(python3 -c "from finance.partner_keys import engine_partner; print(engine_partner('$p'))")"
  echo "  [$p] cascade (engine=$engine)"
  python3 "$MODEL/aggregate.py" --partner "$engine" --json "$RECAL/agg-$p.json"
  python3 "$MODEL/growth.py" --agg "$RECAL/agg-$p.json" --partner "$engine" --json "$RECAL/growth-$p.json"
  python3 "$MODEL/growth_frontend_block.py" --partner "$engine" \
    --growth "$RECAL/growth-$p.json" --rollup "$RECAL/agg-$p.json" \
    --out "$RECAL/growth-frontend-$p.json"
  python3 "$FINANCE/splice_growth_into_partner.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" \
    --frontend "$RECAL/growth-frontend-$p.json" \
    --partner-json "$ROOT/partner-pitch/partners/$p.json"
  cp "$ROOT/partner-pitch/partners/$p.json" "$ROOT/data-clean/partners/$p.json"
done

KNOWN="$(python3 -c "import json; print(','.join(k for k in json.load(open('$FINANCE/PARTNER-SHEET-IDS.json')) if not k.startswith('_')))")"
SHEET_TARGETS=""
IFS=',' read -ra WANT <<< "$PARTNERS"
for p in "${WANT[@]}"; do
  if echo ",$KNOWN," | grep -q ",$p,"; then
    SHEET_TARGETS="${SHEET_TARGETS:+$SHEET_TARGETS,}$p"
  else
    echo "    warn: no sheet id for $p — skip sheet refresh"
  fi
done
if [[ -n "$SHEET_TARGETS" ]]; then
  RUN_CASCADE=0 PARTNERS="$SHEET_TARGETS" "$ROOT/scripts/grok-econ-reseal/run_finance_sheet_lane.sh"
fi
python3 "$FINANCE/wire_partner_economics_urls.py"
echo "→ Rebuild agg-global + economics sidecar"
python3 "$MODEL/aggregate.py" --partner global --json "$RECAL/agg-global.json"
python3 "$FINANCE/build_economics_sidecar.py" --gold "$ROOT/data-clean" --aggdir "$RECAL" \
  --out "$ROOT/data-clean/economics_by_route_id.json" --global
echo "✓ India authority finance lane complete"