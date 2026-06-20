#!/usr/bin/env bash
# BP snap lane — seal Tasklet PR #45 missing endpoint BPs + mint remaining pin-ready routes
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
BP_SNAP="$ROOT/_ingest/bp-snap-tasklet-2026-06-20"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
ACTIVE_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
OPEX="$ROOT/_ingest/sidecar-opex-refresh-2026-06-20"
SEAL_TAG="${SEAL_TAG:-#79aw-tasklet-bp-snap}"

echo "→ Seal 6 Tasklet endpoint BPs (Delos, Phra Arthit, Bidadari, Putri, Epe, Badagry)"
python3 "$BY/snap_bp_coverage_new.py" --ingest "$BP_SNAP" || true
python3 "$BY/apply_boarding_points.py" --dc data-clean --ingest "$BP_SNAP"

echo "→ Mint remaining pin-ready corridor routes"
python3 "$ECON/mint_pending_corridor_routes.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Partner rebind + economics sidecar"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$OPEX" \
  --url-map "$OPEX/economics_url_map.json"

echo "→ Triage + reseal"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'scripts/grok-bolt-yango')
from bolt_yango_routing_shared import build_bp_index, resolve_corridor_endpoints, load_json

fbt = load_json(Path('data-clean/FEATURES_BY_TYPE.json'))
bp_idx = build_bp_index(fbt)
corridors_doc = load_json(Path('_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json'))
unresolved = 0
for mkey, mval in (corridors_doc.get('markets') or {}).items():
    for c in mval.get('corridors') or []:
        if c.get('_bp_source') != 'tasklet-bp-research-2026-06-20' or c.get('aspirational'):
            continue
        fb, tb, _, _ = resolve_corridor_endpoints(c, bp_idx)
        if not (fb and tb):
            unresolved += 1
            print(f"  STILL UNRESOLVED: {mkey}: {c.get('from')} -> {c.get('to')}")

econ = json.loads(Path('data-clean/economics_by_route_id.json').read_text())
m = econ['_meta']
p = len(econ['_pending_route_pin'])
r = m['records']
mint = json.loads(Path('grok-routing-output/mint-pending-corridor-report.json').read_text())
print(f"tasklet-bp unresolved pin-ready: {unresolved}")
print(f"economics: {r} pinned, {p} pending, pin_rate={100*r/(r+p):.1f}%")
print(f"minted this run: {len(mint.get('minted', []))}")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — Tasklet BP snap (11 pin-ready routes)" \
  "$BP_SNAP/"

echo "✓ tasklet bp snap lane: $SEAL_TAG"