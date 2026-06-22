#!/usr/bin/env bash
# Minor Hotels economics cascade (Phase 2) — grounded-first: Phuket → Bali → Palm
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PARTNER="minor-hotels"
CORR="$RECAL/corridors-minor-hotels.json"
MARKETS="phuket,bali,palm-jumeirah"

step() { echo ""; echo "=== $* ==="; }

step "0/9 Ensure corridors view exists"
python3 "$ROOT/scripts/grok-minor-hotels/build_corridors_minor_hotels.py"

step "1/9 aggregate.py (3 Tier-1 clusters, captive)"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "2/9 growth.py (WIDTH headroom, LB-254 captive)"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "3/9 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "4/9 splice growth_case → minor-hotels partner JSON"
python3 "$FINANCE/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$ROOT/partner-pitch/partners/$PARTNER.json"
cp "$ROOT/partner-pitch/partners/$PARTNER.json" "$ROOT/data-clean/partners/$PARTNER.json"

step "5/9 economics_by_route_id sidecar"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

step "6/9 transparent unit-economics sheet"
python3 "$FINANCE/build_transparent_sheet.py" \
  --partner "$PARTNER" \
  --corridors "$CORR" \
  --out "$FINANCE/_refresh_$PARTNER.xlsx"

step "7/9 Bind economics_status on partner JSON"
python3 - <<'PY' "$ROOT"
import json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1])
partner_path = ROOT / "partner-pitch/partners/minor-hotels.json"
sidecar_path = ROOT / "data-clean/economics_by_route_id.json"
sidecar = json.loads(sidecar_path.read_text()) if sidecar_path.exists() else {"records": []}
by_rid = {r["route_id"]: r for r in sidecar.get("records", []) if r.get("route_id")}
partner = json.loads(partner_path.read_text())
bound = pending = 0
for m in partner.get("markets", []):
    for j in m.get("journeys_unlocked", []):
        rid = j.get("route_id")
        if rid and rid in by_rid:
            j["economics_status"] = "bound"
            j["_economics_source"] = "economics_by_route_id.json"
            bound += 1
        elif rid:
            pending += 1
agg = json.loads((ROOT / "finance/recal/agg-minor-hotels.json").read_text())
floor = agg.get("rollup", {}).get("grounded_floor", {}).get("market_rev_yr", 0)
partner["economics_status"] = {
    "state": "grounded_floor_cascade_complete",
    "archetype": "hospitality_developer",
    "grounded_floor_usd_yr": floor,
    "tier1_floors_usd_yr": {"phuket-phang-nga": 4380000, "bali": 630000, "palm-jumeirah": 3750000},
    "cascade_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "agg": "finance/recal/agg-minor-hotels.json",
    "growth": "finance/recal/growth-minor-hotels.json",
    "sheet": "finance/_refresh_minor-hotels.xlsx",
    "capture_frame": "captive LB-254 — headroom = WIDTH",
}
partner_path.write_text(json.dumps(partner, indent=1) + "\n")
(ROOT / "data-clean/partners/minor-hotels.json").write_text(json.dumps(partner, indent=1) + "\n")
print(json.dumps({"bound": bound, "pending": pending, "floor_usd_yr": floor}, indent=2))
PY

step "8/9 validate partner proposals"
python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -6

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Minor Hotels economics cascade — COMPLETE                   │"
echo "│ agg:    finance/recal/agg-minor-hotels.json                 │"
echo "│ growth: finance/recal/growth-minor-hotels.json              │"
echo "│ sheet:  finance/_refresh_minor-hotels.xlsx                    │"
echo "└─────────────────────────────────────────────────────────────┘"