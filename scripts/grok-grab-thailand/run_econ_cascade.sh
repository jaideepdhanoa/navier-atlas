#!/usr/bin/env bash
# Grab Thailand economics cascade: demand apply → aggregate → growth → splice → sidecar → sheet
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-grab-thailand"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PARTNER="grab-thailand"
CORR="$RECAL/corridors-grab-thailand.json"
MARKETS="koh-samui,phuket,bangkok"

step() { echo ""; echo "=== $* ==="; }

step "1/9 Apply Tasklet THAILAND demand anchors → scoped corridors"
python3 "$SCRIPTS/apply_thailand_demand.py"

step "2/9 aggregate.py (3 Thailand markets)"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "3/9 growth.py"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "4/9 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "5/9 splice growth_case → grab-thailand partner JSON"
python3 "$FINANCE/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$ROOT/partner-pitch/partners/$PARTNER.json"
cp "$ROOT/partner-pitch/partners/$PARTNER.json" "$ROOT/data-clean/partners/$PARTNER.json"

step "6/9 economics_by_route_id sidecar"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

step "6b/9 Bind Bucket-C mesh economics (inherit from anchors)"
python3 "$SCRIPTS/bind_bucketC_economics.py"

step "7/9 transparent unit-economics sheet"
python3 "$FINANCE/build_transparent_sheet.py" \
  --partner "$PARTNER" \
  --corridors "$CORR" \
  --out "$FINANCE/_refresh_$PARTNER.xlsx"

step "9/9 bind Bucket-C route economics_status on partner JSON"
python3 - <<'PY' "$ROOT"
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
partner_path = ROOT / "partner-pitch/partners/grab-thailand.json"
sidecar = json.loads((ROOT / "data-clean/economics_by_route_id.json").read_text())
by_rid = {r["route_id"]: r for r in sidecar.get("routes", []) if r.get("route_id")}
partner = json.loads(partner_path.read_text())
bound = pending = 0
for j in partner.get("connected_city_mesh", []):
    rid = j.get("route_id")
    if rid and rid in by_rid:
        j["economics_status"] = "bound"
        j["_economics_source"] = "economics_by_route_id.json"
        bound += 1
    else:
        j["economics_status"] = "pending_demand_anchor"
        pending += 1
for m in partner.get("markets", []):
    for j in m.get("journeys_unlocked", []):
        if j.get("_link_source") != "bucketC-thailand":
            continue
        rid = j.get("route_id")
        if rid and rid in by_rid:
            j["economics_status"] = "bound"
            bound += 1
        else:
            pending += 1
partner["economics_status"] = {
    "state": "grounded_floor_cascade_complete",
    "grounded_floor": "3 cascade-ready corridors (Samui↔Phangan, Phuket↔Phi Phi, Chao Phraya)",
    "cascade_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "agg": "finance/recal/agg-grab-thailand.json",
    "growth": "finance/recal/growth-grab-thailand.json",
    "sheet": "finance/_refresh_grab-thailand.xlsx",
}
partner_path.write_text(json.dumps(partner, indent=1) + "\n")
(ROOT / "data-clean/partners/grab-thailand.json").write_text(json.dumps(partner, indent=1) + "\n")
print(json.dumps({"bucketC_bound": bound, "bucketC_pending": pending}, indent=2))
PY

python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -6

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Grab Thailand economics cascade — COMPLETE                    │"
echo "│ agg: finance/recal/agg-grab-thailand.json                     │"
echo "│ growth: finance/recal/growth-grab-thailand.json               │"
echo "│ sheet: finance/_refresh_grab-thailand.xlsx                    │"
echo "└─────────────────────────────────────────────────────────────┘"