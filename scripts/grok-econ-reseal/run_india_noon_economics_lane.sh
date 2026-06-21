#!/usr/bin/env bash
# India + Noon economics lane: corridors → cascade → sheets → sidecar → partner URL wire
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
PARTNERS_CASCADE="careem,jih-global,qatar,rapido,ola,noon"
PARTNERS_SHEETS="$PARTNERS_CASCADE"

mkdir -p "$RECAL"

echo "→ Create Google Sheets for rapido, ola, noon (if missing)"
python3 "$FINANCE/create_partner_sheets.py"

echo "→ Patch corridors.json with India + Noon markets"
python3 "$ROOT/scripts/grok-econ-reseal/build_india_noon_corridor_markets.py"

echo "→ Finance cascade (aggregate + growth + frontend + splice)"
IFS=',' read -ra TARGETS <<< "$PARTNERS_CASCADE"
for p in "${TARGETS[@]}"; do
  p="${p// /}"
  [[ -z "$p" ]] && continue
  engine="$(python3 -c "from finance.partner_keys import engine_partner; print(engine_partner('$p'))")"
  echo "  [$p] aggregate (engine=$engine)"
  python3 "$MODEL/aggregate.py" --partner "$engine" --json "$RECAL/agg-$p.json"
  echo "  [$p] growth"
  python3 "$MODEL/growth.py" --agg "$RECAL/agg-$p.json" --partner "$engine" --json "$RECAL/growth-$p.json"
  echo "  [$p] frontend block"
  python3 "$MODEL/growth_frontend_block.py" --partner "$engine" \
    --growth "$RECAL/growth-$p.json" --rollup "$RECAL/agg-$p.json" \
    --out "$RECAL/growth-frontend-$p.json"
  echo "  [$p] splice"
  python3 "$FINANCE/splice_growth_into_partner.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" \
    --frontend "$RECAL/growth-frontend-$p.json" \
    --partner-json "$ROOT/partner-pitch/partners/$p.json"
done

echo "→ Build + publish transparent sheets + master tracker"
RUN_CASCADE=0 PARTNERS="$PARTNERS_SHEETS" "$ROOT/scripts/grok-econ-reseal/run_finance_sheet_lane.sh"

echo "→ Rebuild agg-global.json (India/Noon markets for route-keyed sidecar)"
python3 "$MODEL/aggregate.py" --partner global --json "$RECAL/agg-global.json"
echo "→ Rebuild agg-unique-global.json + growth-unique-global.json (global TAM on unique geometry)"
python3 "$MODEL/aggregate.py" --partner global --dedup unique --json "$RECAL/agg-unique-global.json"
python3 "$MODEL/growth.py" --agg "$RECAL/agg-unique-global.json" --partner global-unique --json "$RECAL/growth-unique-global.json"

echo "→ Wire economics_url + model_link into partner JSON"
python3 "$FINANCE/wire_partner_economics_urls.py"

echo "→ Economics sidecar (global)"
python3 "$FINANCE/build_economics_sidecar.py" \
  --gold "$ROOT/data-clean" \
  --aggdir "$RECAL" \
  --out "$ROOT/data-clean/economics_by_route_id.json" \
  --global

echo "→ Validate + build-site smoke"
python3 "$ROOT/scripts/validate_partner_proposals.py"
node "$ROOT/scripts/build-site.mjs" >/dev/null
echo "✓ India + Noon economics lane complete"