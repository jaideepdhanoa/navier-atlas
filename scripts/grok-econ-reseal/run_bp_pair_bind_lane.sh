#!/usr/bin/env bash
# #79as-bp-pair-bind — mint bp_pair_ready + Turkey/UAE mesh + gcn remainder
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
ECON_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
SEAL_TAG="${SEAL_TAG:-#79as-bp-pair-bind}"

echo "→ Phase 1: Mint bp_pair_ready + pending corridor binds"
python3 "$ECON/mint_pending_corridor_routes.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 2: GCN remainder (grab/bali/phuket/qatar)"
python3 "$ECON/mint_gcn_corridor_routes.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 3: Rebind partners + economics"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"
python3 "$BY/build_economics_sidecar.py" --dc data-clean --corridors "$ECON_CORR"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 4: Scrub + reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
econ = json.loads(Path("data-clean/economics_by_route_id.json").read_text())
m = econ["_meta"]
p = len(econ["_pending_route_pin"])
r = m["records"]
print(f"economics: {r} pinned, {p} pending, pin_rate={100*r/(r+p):.1f}%")
t = json.loads(Path("data-clean/PENDING-ECONOMICS-TRIAGE.json").read_text())["_meta"]
print(f"actionable pending: {t.get('actionable_pending')} structural: {t.get('structural_holds')}")
routes = json.loads(Path("data-clean/ROUTES.json").read_text())
print("routes:", len(routes) if isinstance(routes, list) else len(routes.get("features", [])))
PY

if [[ "${BOLT_YANGO_PUSH:-}" == "1" ]]; then
  git add data-clean/ scripts/ grok-routing-output/
  git commit -m "Gold $SEAL_TAG — bp_pair_ready mint + Turkey mesh + gcn remainder"
  RELEASE=1 ./scripts/deploy.sh
fi

echo "✓ lane complete: $SEAL_TAG"