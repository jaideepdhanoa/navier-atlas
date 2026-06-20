#!/usr/bin/env bash
# Portugal corridor completion + economics reseal (#79ap)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
INGEST_BY="$ROOT/_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"
SEAL_TAG="${SEAL_TAG:-#79ap-econ-portugal}"

echo "→ Phase 1: Portugal BPs"
python3 "$BY/portugal_bps_patch.py"

echo "→ Phase 2: Coastal routes (Portugal + geometry refresh)"
python3 "$BY/route_bolt_yango_markets.py" --dc data-clean --ingest "$INGEST_BY" --refresh-existing

echo "→ Phase 3: Journey / corridor binding"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$INGEST_BY"

echo "→ Phase 4: Economics reseal (8 fresh partners)"
python3 "$ECON/apply_econ_reseal.py" --dc data-clean

echo "→ Phase 5: Economics sidecar rebuild"
python3 "$BY/build_economics_sidecar.py" --dc data-clean

echo "→ Phase 6: Reseal"
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
root = Path(".")
bolt = json.loads((root / "data-clean/partners/bolt.json").read_text())
portugal = next(m for m in bolt["markets"] if m.get("id") == "portugal")
journeys = {j["from"]: j.get("route_id") for j in portugal.get("journeys_unlocked", [])}
print("Portugal journeys:", journeys)
econ = json.loads((root / "data-clean/economics_by_route_id.json").read_text())
print("econ records:", len(econ.get("records", [])))
print("pending:", len(econ.get("_pending_route_pin", [])))
gc = bolt.get("growth_case", {}).get("_provenance", {})
print("bolt growth provenance:", gc.get("source_rollup"), "sourced:", gc.get("sourced_corridors"))
PY

"$ROOT/scripts/publish-gold.sh" "Gold $SEAL_TAG — econ reseal + Portugal corridor bind + geometry polish"

echo "✓ lane complete: $SEAL_TAG"