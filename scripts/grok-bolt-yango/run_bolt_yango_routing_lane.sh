#!/usr/bin/env bash
# Bolt/Yango routing lane: BPs → coastal routes → economics → splice → seal
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-bolt-yango"
SEAL_LABEL="${BOLT_YANGO_SEAL:-#79ar-routing}"

step() { echo ""; echo "=== $* ==="; }

step "B — Re-seal BPs (expanded water allowlist, max-inland 0.35km)"
python3 "$SCRIPTS/apply_boarding_points.py" --dc "$ROOT/data-clean" --max-inland-km 0.35

step "A — Coastal route synthesis + geometry refresh"
python3 "$SCRIPTS/route_bolt_yango_markets.py" --dc "$ROOT/data-clean" --refresh-existing

step "Partner splice + economics + growth_case"
python3 "$SCRIPTS/scrub_exclusion_pois.py" --dc "$ROOT/data-clean"
python3 "$SCRIPTS/apply_bolt_yango.py" --dc "$ROOT/data-clean"
python3 "$SCRIPTS/build_economics_sidecar.py" --dc "$ROOT/data-clean"
python3 "$SCRIPTS/bind_yango_growth_case.py" --dc "$ROOT/data-clean"

step "D — Finalize seal $SEAL_LABEL"
python3 "$SCRIPTS/finalize_seal_79aq.py" --dc "$ROOT/data-clean" --seal "$SEAL_LABEL"

step "QA"
python3 - <<'PY' "$ROOT"
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
dc = root / "data-clean"
routes = json.loads((dc / "ROUTES.json").read_text())
n = len(routes) if isinstance(routes, list) else len(routes.get("features", []))
report = json.loads((root / "grok-routing-output/bolt-yango-route-report.json").read_text())
splice = json.loads((root / "grok-routing-output/bolt-yango-splice-report.json").read_text())
econ = json.loads((dc / "economics_by_route_id.json").read_text())
pinned = len(econ.get("records", []))
print(f"routes={n} synthesized={len(report.get('synthesized',[]))} refreshed={len(report.get('refreshed',[]))}")
print(f"binding bolt={splice.get('binding_bolt')} yango={splice.get('binding_yango')}")
print(f"economics pinned records={pinned} pending={len(econ.get('_pending_route_pin',[]))}")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_LABEL — Bolt/Yango coastal routing + economics rebind" \
  _ingest/bolt-yango-seal-2026-06-19/