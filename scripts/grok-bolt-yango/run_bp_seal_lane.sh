#!/usr/bin/env bash
# Full bp-seal-2026-06-20 mandate (#79aq-bp-seal-2026-06-20)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
ECON_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
SEAL_TAG="${SEAL_TAG:-#79aq-bp-seal-2026-06-20}"

echo "→ Phase 1: Snap 51 new BPs + lagoon/river allowlist"
python3 "$BY/snap_bp_coverage_new.py" --ingest "$BP_INGEST"

echo "→ Phase 2: Seal boarding points (bp-seal handoff)"
python3 "$BY/apply_boarding_points.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Phase 3: Route-seal kept markets (Spain/Sweden/thin)"
python3 "$BY/route_kept_markets.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 4: Refresh bolt/yango mesh + coastal geometry"
python3 "$BY/route_bolt_yango_markets.py" --dc data-clean \
  --ingest "$ROOT/_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19" --refresh-existing

echo "→ Phase 5: Splice enriched sub-proposals + bind routes"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Phase 6: Economics sidecar + triage"
python3 "$BY/build_economics_sidecar.py" --dc data-clean --corridors "$ECON_CORR"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 7: Scrub + reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
from collections import Counter

root = Path(".")
cov = json.load(open("_ingest/bp-seal-2026-06-20/inputs/BP-COVERAGE-NEW-2026-06-20.json"))
new_ids = {x["id"] for x in cov["new_bps"]}
bp_report = json.load(open("grok-routing-output/bolt-yango-bp-apply-report.json"))
ledger = {e["handoff_id"]: e.get("action") for e in bp_report["ledger"] if e.get("handoff_id") in new_ids}
print("51-new actions:", Counter(ledger.values()))
print("sealed total:", len(bp_report.get("sealed", [])))
route_report = json.load(open("grok-routing-output/route-kept-markets-report.json"))
print("kept-market routes:", len(route_report.get("synthesized", [])))

bolt = json.load(open("data-clean/partners/bolt.json"))
for mid in ("spain", "sweden", "portugal"):
    m = next(x for x in bolt["markets"] if x["id"] == mid)
    j = m.get("journeys_unlocked", [])
    linked = sum(1 for x in j if x.get("route_id"))
    print(f"bolt/{mid} journeys linked {linked}/{len(j)}")

econ = json.load(open("data-clean/economics_by_route_id.json"))
meta = econ["_meta"]
p = len(econ.get("_pending_route_pin", []))
r = meta["records"]
print(f"economics: {r} pinned, {p} pending, pin_rate={100*r/(r+p):.1f}%")
PY

if [[ "${BOLT_YANGO_PUSH:-}" == "1" ]]; then
  git add data-clean/ scripts/grok-bolt-yango/ scripts/grok-econ-reseal/ grok-routing-output/ _ingest/bp-seal-2026-06-20/
  git commit -m "Gold $SEAL_TAG — bp-seal snap + Spain/Sweden route-seal + 51 BP coverage"
  RELEASE=1 ./scripts/deploy.sh
fi

echo "✓ bp-seal lane complete: $SEAL_TAG"