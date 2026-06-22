#!/usr/bin/env bash
# Grok Bucket-C Thailand: validate coords → seal BPs → route mesh → land-crossing QA
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-bucketC-thailand"

step() { echo ""; echo "=== $* ==="; }

step "1/7 Gazetteer-validate 19 boarding points"
python3 "$SCRIPTS/validate_bp_coords.py"

step "2/7 Seal BPs + bind anchor corridors (grab-thailand)"
python3 "$SCRIPTS/seal_grab_thailand.py" --apply

step "3/7 Rebuild connected-city BP↔BP route mesh (tuned waypoints)"
python3 "$SCRIPTS/route_bucketC_thailand.py" --repo "$ROOT"

step "4/7 Link Bucket-C mesh onto grab-thailand partner JSON"
python3 "$SCRIPTS/link_bucketC_mesh.py"

step "5/7 Sync city + locale briefs to data-clean"
python3 "$SCRIPTS/sync_thailand_assets.py"

step "6/7 Land-crossing QA (LB-242 interior gate)"
python3 - <<'PY' "$ROOT"
import json, sys
from pathlib import Path
ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "scripts/grok-bucketB"))
from bucketB_shared import load_json, route_features, route_id_of, interior_land_km, load_land_mask

dc = ROOT / "data-clean"
routes = route_features(load_json(dc / "ROUTES.json"))
allow = set(load_json(dc / "route_water_allowlist.json").get("ids", []))
mask = load_land_mask()
THRESH = 0.05

flagged = []
bucketC = []
for feat in routes:
    props = feat.get("properties", feat)
    if not props.get("_bucketC_thailand"):
        continue
    bucketC.append(feat)
    coords = feat["geometry"]["coordinates"]
    land_km = interior_land_km(coords, mask)
    rid = route_id_of(feat)
    if land_km > THRESH and rid not in allow:
        flagged.append({"route_id": rid, "land_km": land_km, "label": props.get("label")})

report = {
    "qa_at": __import__("datetime").datetime.now(__import__("datetime").timezone.utc).isoformat(),
    "bucketC_routes": len(bucketC),
    "land_crossing_clean": len(flagged) == 0,
    "flagged_unallowlisted": flagged,
    "allowlisted": sum(1 for f in bucketC if route_id_of(f) in allow),
}
out = ROOT / "grok-routing-output/grab-thailand-land-qa-report.json"
out.write_text(json.dumps(report, indent=2) + "\n")
print(json.dumps({"bucketC_routes": report["bucketC_routes"], "land_crossing_clean": report["land_crossing_clean"], "flagged": len(flagged)}, indent=2))
if flagged:
    print("FLAGGED (unallowlisted land crossings):", flagged, file=sys.stderr)
    sys.exit(1)
PY

step "7/7 Partner schema validation"
python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -8

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Grok Bucket-C Thailand — COMPLETE                           │"
echo "│ Partner slug: /grab-thailand/                               │"
echo "│ Reports: grok-routing-output/grab-thailand-*-report.json    │"
echo "└─────────────────────────────────────────────────────────────┘"