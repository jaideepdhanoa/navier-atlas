#!/usr/bin/env bash
# AirAsia MOVE economics cascade: demand apply → aggregate → growth → splice
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-airasia"
MODEL="$ROOT/finance/model"
RECAL="$ROOT/finance/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PARTNER="airasia-move"
CORR="$RECAL/corridors-$PARTNER.json"
MARKETS="$PARTNER"

step() { echo ""; echo "=== $* ==="; }

step "0 build scoped corridors from partner route_ids"
python3 "$ROOT/scripts/grok-bite2/build_partner_corridors.py" --partner "$PARTNER"

step "1 apply arriving-seat demand anchors (PH/SG + Phase-1 hubs)"
python3 "$SCRIPTS/apply_airasia_demand.py"

step "2 aggregate.py"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "3 growth.py"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "4 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "5 splice growth_case"
python3 "$ROOT/finance/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$ROOT/partner-pitch/partners/$PARTNER.json"
cp "$ROOT/partner-pitch/partners/$PARTNER.json" "$ROOT/data-clean/partners/$PARTNER.json"

step "6 economics sidecar refresh"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$ROOT/finance/economics_url_map.json" || true

step "7 publish transparent economics sheet"
PY="$ROOT/deck-studio/.venv/bin/python3"
"$PY" "$ROOT/finance/publish_partner_economics.py" airasia-move \
  --title "Navier — AirAsia MOVE Unit Economics"

step "8 mark PH/SG economics_status bound where sidecar exists"
python3 - <<'PY' "$ROOT"
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
partner_path = ROOT / "partner-pitch/partners/airasia-move.json"
sidecar = json.loads((ROOT / "data-clean/economics_by_route_id.json").read_text())
by_rid = {r["route_id"]: r for r in sidecar.get("records", []) if r.get("route_id")}
partner = json.loads(partner_path.read_text())
ph_sg = {"manila", "cebu", "boracay", "palawan", "siargao", "singapore"}
bound = pending = roadmap = 0
for m in partner.get("markets", []):
    if m.get("slug") not in ph_sg:
        continue
    for j in m.get("journeys_unlocked", []) or []:
        rid = j.get("route_id")
        if rid == "rn-81f865bba3ac":
            j["economics_status"] = "roadmap_quanta_lr"
            j["_roadmap"] = True
            roadmap += 1
        elif rid and rid in by_rid:
            j["economics_status"] = "bound"
            bound += 1
        else:
            pending += 1
partner.setdefault("economics_status", {})["state"] = "ph_sg_model_pass_complete"
partner["economics_status"]["agg"] = "finance/recal/agg-airasia-move.json"
partner["economics_status"]["growth"] = "finance/recal/growth-airasia-move.json"
partner["economics_status"]["cascade_at"] = __import__("datetime").datetime.now(__import__("datetime").timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
partner_path.write_text(json.dumps(partner, indent=1) + "\n")
(ROOT / "data-clean/partners/airasia-move.json").write_text(json.dumps(partner, indent=1) + "\n")
print(json.dumps({"ph_sg_bound": bound, "ph_sg_pending": pending, "roadmap": roadmap}, indent=2))
PY

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ AirAsia MOVE economics cascade — COMPLETE                     │"
echo "│ agg: finance/recal/agg-airasia-move.json                      │"
echo "│ growth: finance/recal/growth-airasia-move.json                │"
echo "└─────────────────────────────────────────────────────────────┘"