#!/usr/bin/env bash
# BP-seal + GCN mint + pending economics lane (#79aq / #79ar-pending-uae)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
BY_INGEST="$ROOT/_ingest/bolt-yango-seal-2026-06-19/bolt-yango-seal-2026-06-19"
ECON_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
SEAL_TAG="${SEAL_TAG:-#79ar-pending-uae}"

echo "→ Phase 0: Seal boarding points (bp-seal handoff)"
python3 "$BY/apply_boarding_points.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Phase 1: Coastal routes (bolt/yango markets + mesh)"
python3 "$BY/route_bolt_yango_markets.py" --dc data-clean --ingest "$BY_INGEST" --refresh-existing

echo "→ Phase 2: Mint declared gcn-* corridor routes (UAE pass + full sweep)"
python3 "$ECON/mint_gcn_corridor_routes.py" --dc data-clean --corridors "$ECON_CORR" \
  --markets "bolt-,yango-,uae-careem"
python3 "$ECON/mint_gcn_corridor_routes.py" --dc data-clean --corridors "$ECON_CORR"
python3 "$ECON/portugal_corridors_patch.py" --corridors "$ECON_CORR"

echo "→ Phase 3: Splice enriched sub-proposals (22 active markets)"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Phase 4: Economics sidecar rebuild"
python3 "$BY/build_economics_sidecar.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 5: Pending triage report"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 6: Reseal"
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
root = Path(".")
econ = json.loads((root / "data-clean/economics_by_route_id.json").read_text())
meta = econ["_meta"]
pending = len(econ.get("_pending_route_pin", []))
rec = meta["records"]
print(f"economics: records={rec} pending={pending} pin_rate={100*rec/(rec+pending):.1f}%")
triage = json.loads((root / "data-clean/PENDING-ECONOMICS-TRIAGE.json").read_text())
print("actionable pin rate:", triage["_meta"].get("pin_rate_actionable"))
print("sub_buckets:", triage.get("sub_buckets"))
routes = json.loads((root / "data-clean/ROUTES.json").read_text())
n = len(routes) if isinstance(routes, list) else len(routes.get("features", []))
print("routes:", n)
PY

if [[ "${BOLT_YANGO_PUSH:-}" == "1" ]]; then
  git add data-clean/ scripts/grok-bolt-yango/ scripts/grok-econ-reseal/ grok-routing-output/
  git commit -m "Gold $SEAL_TAG — bp-seal + gcn mint + pending economics triage"
  RELEASE=1 ./scripts/deploy.sh
fi

echo "✓ lane complete: $SEAL_TAG"