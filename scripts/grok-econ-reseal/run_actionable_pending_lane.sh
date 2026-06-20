#!/usr/bin/env bash
# Actionable pending economics — mint gcn + bp-pair routes, rebuild sidecar, reseal.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
FINANCE="$ROOT/finance"
ACTIVE_CORR="$FINANCE/model/corridors.json"
SEAL_TAG="${SEAL_TAG:-#79bc-actionable-pending}"

echo "→ Mint declared gcn-* routes not yet in gold"
python3 "$ECON/mint_gcn_corridor_routes.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Mint pending corridor bp-pair binds (yango-turkey cross-border, etc.)"
python3 "$ECON/mint_pending_corridor_routes.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Rebuild economics sidecar + triage"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$FINANCE/recal" \
  --url-map "$FINANCE/economics_url_map.json"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Scrub + reseal"
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

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — actionable pending economics mint (gcn + yango-turkey rn)" \
  "finance/model/corridors.json" "grok-routing-output/"

echo "✓ actionable pending lane: $SEAL_TAG"