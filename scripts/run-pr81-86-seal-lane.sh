#!/usr/bin/env bash
# PR #81–#86 seal orchestrator — Bolt markets, Côte d'Azur de-bundle, UAE cleanup, East Africa
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GEO="$ROOT/scripts/grok-geometry"
ECON="$ROOT/scripts/grok-econ-reseal"
BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#pr81-86-seal}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

step "0/12 Baseline counts"
python3 - <<'PY'
import json
from pathlib import Path
root = Path(".")
fbt = json.loads((root / "data-clean/FEATURES_BY_TYPE.json").read_text())
routes = json.loads((root / "data-clean/ROUTES.json").read_text())
rn = len(routes) if isinstance(routes, list) else len(routes.get("features", []))
bolt = json.loads((root / "data-clean/partners/bolt.json").read_text())
print(json.dumps({
    "routes": rn,
    "pois": len(fbt.get("poi", [])),
    "uae_locales": sum(1 for l in fbt.get("locale", []) if (l.get("properties") or {}).get("parent_city_id", "").endswith("-uae")),
    "bolt_markets": len(bolt.get("markets", [])),
}, indent=2))
PY

step "1/12 UAE locale + POI cleanup (PR #82)"
python3 "$GEO/apply_uae_cleanup.py" --dc data-clean --apply

step "2/12 Lagos + Cape Town junk POI trim (PR #84)"
python3 "$GEO/apply_poi_junk_drops.py" --dc data-clean --apply

step "3/12 Côte d'Azur de-bundle (PR #81)"
python3 "$GEO/apply_cote_dazur_debundle.py" --dc data-clean --apply

step "4/12 Bolt East Africa geometry seal (PR #85)"
python3 "$GEO/mint_bolt_east_africa_geometry.py" --dc data-clean --apply

step "5/12 Merge bolt subproposal deltas (PR #83 + #81 + #85)"
python3 "$ECON/merge_bolt_subproposal_delta.py"

MERGED="$ROOT/grok-routing-output/merged-bolt-subproposals-pr81-86.json"
[[ -f "$MERGED" ]] || die "missing merged subproposals: $MERGED"

step "6/12 Splice Bolt/Yango partners from merged subproposals"
BY_INGEST="$ROOT/_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --authored "$MERGED" --ingest "$BY_INGEST"

step "7/12 Route Bolt/Yango affected markets"
ECON_CORR="$ROOT/finance/model/corridors.json"
python3 "$BY/route_bolt_yango_markets.py" --dc data-clean --ingest "$BY_INGEST" --refresh-existing

step "8/12 Route linkage lane (bolt)"
"$ROOT/scripts/run-route-linkage-lane.sh" --apply --partner bolt

step "9/12 Economics sidecar refresh"
python3 "$BY/build_economics_sidecar.py" --dc data-clean --corridors "$ECON_CORR"

step "10/12 Bolt hub narrative refresh — hub copy only (PR #86)"
python3 "$ECON/apply_bolt_hub_narrative.py" --dc data-clean --apply

step "11/12 Partner map scope materialize"
python3 "$ROOT/scripts/materialize_partner_map_scope.py" bolt 2>/dev/null || echo "WARN: map scope handoff skip"

step "12/12 Reseal SEAL.json hashes"
python3 "$ECON/update_seal_hashes.py"
python3 "$GEO/update_seal_geometry_gate.py" --apply 2>/dev/null || true

step "Acceptance QA"
python3 - <<'PY'
import json, sys
from pathlib import Path
root = Path(".")
fail = []

def load(p):
    return json.loads(p.read_text()) if p.exists() else {}

uae = load(root / "grok-routing-output/uae-cleanup-seal-report.json")
junk = load(root / "grok-routing-output/lagos-capetown-junk-trim-report.json")
cda = load(root / "grok-routing-output/cote-dazur-debundle-report.json")
ea = load(root / "grok-routing-output/bolt-east-africa-seal-report.json")
splice = load(root / "grok-routing-output/bolt-yango-splice-report.json")

bolt = load(root / "data-clean/partners/bolt.json")
markets = {m.get("id"): m for m in bolt.get("markets", [])}

# KSA rescope
ksa = next((m for m in bolt.get("markets", []) if m.get("id") in ("ksa-commercial", "bolt-ksa-commercial")), None)
if ksa:
    anchors = set(ksa.get("anchor_cities") or [])
    bad = anchors & {"neom-ksa", "neom-sindalah-ksa", "amaala-ksa", "red-sea-global", "red-sea-global-ksa"}
    if bad:
        fail.append(f"KSA still has giga anchors: {bad}")
    want = {"jeddah-ksa", "dammam-khobar-ksa", "manama-bahrain"}
    if not want <= anchors:
        fail.append(f"KSA anchors missing: {want - anchors}")

for mid in ("estonia", "thailand", "nigeria", "south-africa", "east-africa"):
    m = markets.get(mid) or markets.get(f"bolt-{mid}")
    if not m:
        fail.append(f"missing market: {mid}")
    elif not m.get("anchor_cities"):
        fail.append(f"zero anchors: {mid}")

if uae.get("silent_drops", 1) != 0:
    fail.append("UAE silent drops")
if junk.get("silent_drops", 1) != 0:
    fail.append("junk trim silent drops")
if cda.get("silent_drops", 1) != 0:
    fail.append("cote-dazur silent drops")

print("QA markets:", len(bolt.get("markets", [])))
print("QA splice:", {k: splice.get(k) for k in ("bolt_markets", "markets_zero_anchors_after_crosswalk")})
print("QA east-africa corridors:", len(ea.get("corridors_built", [])))

if fail:
    print("QA FAIL:", fail)
    sys.exit(1)
print("QA PASS")
PY

"$ROOT/scripts/publish-gold.sh" "Gold $SEAL_TAG — PR #81–#86 Bolt seal lane"
echo "✓ PR #81–#86 seal lane complete ($SEAL_TAG)"