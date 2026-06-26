#!/usr/bin/env bash
# Centara Thailand hospitality economics cascade — corridor examples only (no SOM ladder)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-centara-thailand"
FINANCE="$ROOT/finance"
MODEL="$FINANCE/model"
RECAL="$FINANCE/recal"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
BY="$ROOT/scripts/grok-bolt-yango"
PARTNER="centara-thailand"
CORR="$RECAL/corridors-$PARTNER.json"
MARKETS="bangkok-river,western-gulf,eastern-gulf,phuket-andaman,krabi-phi-phi,samui-gulf"

step() { echo ""; echo "=== $* ==="; }

step "0/8 Seal routes + partner page (if not already applied)"
python3 "$SCRIPTS/seal_centara_thailand.py" --apply

step "1/8 aggregate.py (6 hospitality clusters)"
python3 "$MODEL/aggregate.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --corridors "$CORR" \
  --json "$RECAL/agg-$PARTNER.json"

step "2/8 growth.py (corridor headroom)"
python3 "$MODEL/growth.py" \
  --partner "$PARTNER" \
  --markets "$MARKETS" \
  --agg "$RECAL/agg-$PARTNER.json" \
  --json "$RECAL/growth-$PARTNER.json"

step "3/8 growth_frontend_block.py"
mkdir -p "$GROWTH_DRAFT"
python3 "$MODEL/growth_frontend_block.py" \
  --partner "$PARTNER" \
  --partner-json "$ROOT/partner-pitch/partners/$PARTNER.json" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --rollup "$RECAL/agg-$PARTNER.json" \
  --out "$GROWTH_DRAFT/$PARTNER.growth.json"

step "4/8 splice growth_case → centara-thailand partner JSON"
python3 "$FINANCE/splice_growth_into_partner.py" \
  --partner "$PARTNER" \
  --growth "$RECAL/growth-$PARTNER.json" \
  --frontend "$GROWTH_DRAFT/$PARTNER.growth.json" \
  --partner-json "$ROOT/partner-pitch/partners/$PARTNER.json"
cp "$ROOT/partner-pitch/partners/$PARTNER.json" "$ROOT/data-clean/partners/$PARTNER.json"

step "5/8 economics_by_route_id sidecar"
python3 "$BY/build_economics_sidecar.py" \
  --dc "$ROOT/data-clean" \
  --corridors "$CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

step "6/8 transparent unit-economics sheet (hospitality capex)"
python3 "$FINANCE/build_transparent_sheet.py" \
  --partner "$PARTNER" \
  --corridors "$CORR" \
  --out "$FINANCE/_refresh_$PARTNER.xlsx" \
  --capex-tier hospitality

step "7/8 bind economics_status on partner JSON"
python3 - <<'PY' "$ROOT"
import json, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT = Path(sys.argv[1])
partner_path = ROOT / "partner-pitch/partners/centara-thailand.json"
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
agg = json.loads((ROOT / "finance/recal/agg-centara-thailand.json").read_text())
floor = agg.get("rollup", {}).get("grounded_floor", {}).get("market_rev_yr", 0)
partner["economics_status"] = {
    "state": "hospitality_corridor_cascade_complete",
    "archetype": "hospitality_operator",
    "corridor_examples_only": True,
    "grounded_floor_usd_yr": floor,
    "cascade_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    "agg": "finance/recal/agg-centara-thailand.json",
    "growth": "finance/recal/growth-centara-thailand.json",
    "sheet": "finance/_refresh_centara-thailand.xlsx",
    "sidecar": "handoff/centara-thailand/centara-thailand-economics-sidecar.json",
}
partner_path.write_text(json.dumps(partner, indent=1) + "\n")
(ROOT / "data-clean/partners/centara-thailand.json").write_text(json.dumps(partner, indent=1) + "\n")
print(json.dumps({"bound": bound, "pending": pending, "floor_usd_yr": floor}, indent=2))
PY

step "8/8 validate partner proposals"
python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -8

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Centara Thailand economics cascade — COMPLETE               │"
echo "│ agg:    finance/recal/agg-centara-thailand.json             │"
echo "│ growth: finance/recal/growth-centara-thailand.json          │"
echo "│ sheet:  finance/_refresh_centara-thailand.xlsx              │"
echo "└─────────────────────────────────────────────────────────────┘"