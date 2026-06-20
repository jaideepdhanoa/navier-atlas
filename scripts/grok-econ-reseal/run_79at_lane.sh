#!/usr/bin/env bash
# #79at — mesh trim + Egypt mint + sidecar opex refresh + partner rebind
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
OPEX_INGEST="$ROOT/_ingest/sidecar-opex-refresh-2026-06-20"
ECON_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
SEAL_TAG="${SEAL_TAG:-#79at-mesh-trim-opex-egypt}"

echo "→ Phase 1: Trim excess _pending_mesh (dedupe + cap 35/city)"
python3 "$ECON/trim_excess_mesh.py" --dc data-clean --cap-per-city 35

echo "→ Phase 2: Egypt corridor route mint"
python3 "$ECON/mint_egypt_corridor_routes.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 3: Partner rebind"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Phase 4: Economics sidecar (6-line opex, post-recal aggs)"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ECON_CORR" \
  --aggdir "$OPEX_INGEST" \
  --url-map "$OPEX_INGEST/economics_url_map.json"

echo "→ Phase 5: Yango growth_case bind"
python3 "$BY/bind_yango_growth_case.py" --dc data-clean --aggdir "$OPEX_INGEST" || true

echo "→ Phase 6: Pending economics triage"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ECON_CORR"

echo "→ Phase 7: Scrub + reseal"
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
print("by partner:", {k: v for k, v in __import__('collections').Counter(x['partner'] for x in econ['records']).most_common()})

# opex line check on one bolt record
bolt = next((x for x in econ["records"] if x["partner"] == "bolt"), None)
if bolt:
    rc = bolt.get("breakdown", {}).get("run_cost", {})
    print("bolt sample opex:", {k: rc.get(k) for k in (
        "insurance_usd_yr", "charging_berth_usd_yr", "annual_opex_usd_yr"
    )})

routes = json.loads(Path("data-clean/ROUTES.json").read_text())
n = len(routes) if isinstance(routes, list) else len(routes.get("features", []))
mesh = sum(
    1 for f in (routes if isinstance(routes, list) else routes.get("features", []))
    if (f.get("properties", f) or {}).get("_pending_mesh")
)
print(f"routes: {n} | _pending_mesh: {mesh}")

for partner in ("bolt", "yango"):
    doc = json.loads(Path(f"data-clean/partners/{partner}.json").read_text())
    linked = unlinked = 0
    def w(o):
        global linked, unlinked
        if isinstance(o, dict):
            st = o.get("_link_status", "")
            if st == "linked":
                linked += 1
            elif st.startswith("unlinked"):
                unlinked += 1
            for v in o.values():
                if isinstance(v, (dict, list)):
                    w(v)
        elif isinstance(o, list):
            for i in o:
                w(i)
    w(doc)
    print(f"{partner} bind: {linked} linked / {unlinked} unlinked")
PY

if [[ "${BOLT_YANGO_PUSH:-}" == "1" ]]; then
  git add data-clean/ scripts/ grok-routing-output/ _ingest/sidecar-opex-refresh-2026-06-20/
  git commit -m "Gold $SEAL_TAG — mesh trim, Egypt mint, sidecar opex refresh"
  RELEASE=1 ./scripts/deploy.sh
fi

echo "✓ lane complete: $SEAL_TAG"