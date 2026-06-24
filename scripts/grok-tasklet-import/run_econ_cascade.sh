#!/usr/bin/env bash
# Tasklet proposal economics cascade (Phase B) for one partner.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-tasklet-import"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PACKAGE="${TASKLET_PACKAGE:-curacao-caribbean-2026-06-24}"

PARTNER="${1:-}"
if [[ -z "$PARTNER" ]]; then
  echo "Usage: $0 <partner-id> [markets_csv]" >&2
  exit 1
fi
MARKETS="${2:-$PARTNER}"
CORR="$RECAL/corridors-$PARTNER.json"

step() { echo ""; echo "=== $* ==="; }

step "0/9 Bind corridors from staging (idempotent)"
python3 "$SCRIPTS/bind_corridors_from_staging.py" --package "$PACKAGE" --partner "$PARTNER"

step "1/9 Build scoped corridors view"
python3 "$SCRIPTS/build_scoped_corridors.py" --partner "$PARTNER"

step "2/9 Apply Tasklet demand anchors"
python3 "$SCRIPTS/apply_demand_anchors.py" --partner "$PARTNER" --package "$PACKAGE"

step "3/9 aggregate.py"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "4/9 growth.py (greenfield WIDTH — rising ladder, not FP-flat)"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "5/9 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "6/9 splice growth_case → partner JSON"
PJ="$ROOT/partner-pitch/partners/$PARTNER.json"
DC="$ROOT/data-clean/partners/$PARTNER.json"
python3 "$FINANCE/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$PJ"
cp "$PJ" "$DC"

step "7/9 economics_by_route_id sidecar"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

step "8/9 transparent unit-economics sheet"
python3 "$FINANCE/build_transparent_sheet.py" \
  --partner "$PARTNER" \
  --corridors "$CORR" \
  --out "$FINANCE/_refresh_$PARTNER.xlsx"

step "9/9 Bind economics_status on partner JSON"
python3 - <<'PY' "$ROOT" "$PARTNER"
import json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT, PARTNER = Path(sys.argv[1]), sys.argv[2]
partner_path = ROOT / f"partner-pitch/partners/{PARTNER}.json"
sidecar = json.loads((ROOT / "data-clean/economics_by_route_id.json").read_text())
by_rid = {r["route_id"]: r for r in sidecar.get("records", []) if r.get("route_id")}
partner = json.loads(partner_path.read_text())
bound = pending = roadmap = 0
def resolve_rid(j):
    rid = j.get("route_id")
    if not rid:
        ids = j.get("route_ids") or []
        rid = ids[0] if ids else None
        if rid:
            j["route_id"] = rid
    return rid

for j in partner.get("journeys_unlocked", []):
    rid = resolve_rid(j)
    est = j.get("economics_status", "")
    if est == "roadmap_excluded" or j.get("render", "").startswith("roadmap"):
        roadmap += 1
        continue
    if rid and rid in by_rid:
        j["economics_status"] = "bound"
        j["_economics_source"] = "economics_by_route_id.json"
        bound += 1
    elif rid:
        pending += 1
for ph in partner.get("phases", []):
    for fr in ph.get("featured_routes", []):
        rid = resolve_rid(fr)
        if rid and rid in by_rid:
            fr["economics_status"] = "bound"
            fr["_economics_source"] = "economics_by_route_id.json"
            bound += 1
agg = json.loads((ROOT / f"finance/recal/agg-{PARTNER}.json").read_text())
floor = agg.get("rollup", {}).get("grounded_floor", {}).get("market_rev_yr", 0)
pool = agg.get("rollup", {}).get("grounded_floor", {}).get("transport_spend_pool_yr", 0)
eff = agg.get("rollup", {}).get("grounded_floor", {}).get("effective_capture")
partner["economics_status"] = {
    "state": "grounded_floor_cascade_complete",
    "grounded_floor_usd_yr": floor,
    "transport_spend_pool_usd_yr": pool,
    "effective_capture": eff,
    "cascade_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "agg": f"finance/recal/agg-{PARTNER}.json",
    "growth": f"finance/recal/growth-{PARTNER}.json",
    "sheet": f"finance/_refresh_{PARTNER}.xlsx",
    "capture_frame": "captive 0.55 — rising ladder (not FP-flat)",
}
partner.pop("_economics_status", None)
partner.pop("_economics_note", None)
partner_path.write_text(json.dumps(partner, indent=2) + "\n")
(ROOT / f"data-clean/partners/{PARTNER}.json").write_text(json.dumps(partner, indent=2) + "\n")
print(json.dumps({"bound": bound, "pending": pending, "roadmap_excluded": roadmap, "floor_usd_yr": floor, "eff_capture": eff}, indent=2))
PY

python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -6 || true

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ $PARTNER economics cascade — COMPLETE                        │"
echo "│ agg:    finance/recal/agg-$PARTNER.json                       │"
echo "│ growth: finance/recal/growth-$PARTNER.json                    │"
echo "│ sheet:  finance/_refresh_$PARTNER.xlsx                        │"
echo "└─────────────────────────────────────────────────────────────┘"