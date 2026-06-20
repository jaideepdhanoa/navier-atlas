#!/usr/bin/env bash
# Ingest Tasklet PR #49 — Yango Turkey coast node split + route re-bind
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

HANDOFF="${TASKLET_HANDOFF:-$ROOT/_ingest/tasklet-turkey-split-2026-06-20}"
ACTIVE_CORR="$ROOT/finance/model/corridors.json"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#79az-tasklet-finance-cascade}"

if [[ ! -f "$ROOT/data-clean/partners/yango.json" ]]; then
  echo "✗ missing data-clean/partners/yango.json" >&2
  exit 1
fi

echo "→ Promote Turkey-split corridors.json"
mkdir -p "$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs"
cp "$ACTIVE_CORR" "$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"

echo "→ Retag coastal routes + mint Konak/Karşıyaka + Çeşme/Chios + Kuşadası/Samos"
python3 "$ECON/retag_turkey_coast.py" --dc data-clean

echo "→ Splice Yango Turkey market + re-bind featured routes"
if [[ -f "$HANDOFF/yango.json" ]]; then
  python3 "$ECON/splice_tasklet_turkey.py" --handoff "$HANDOFF" --corridors "$ACTIVE_CORR"
else
  git show origin/turkey-coast-split-2026-06-20:data-clean/partners/yango.json > /tmp/yango-turkey-handoff.json
  mkdir -p "$HANDOFF"
  cp /tmp/yango-turkey-handoff.json "$HANDOFF/yango.json"
  python3 "$ECON/splice_tasklet_turkey.py" --handoff "$HANDOFF" --corridors "$ACTIVE_CORR"
fi

echo "→ Economics sidecar (geometry refresh; no re-cascade)"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$ROOT/finance/recal" \
  --url-map "$ROOT/finance/economics_url_map.json"

python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
y = json.loads(Path("data-clean/partners/yango.json").read_text())
t = next(m for m in y["markets"] if m["id"] == "turkey")
print("anchors:", t.get("anchor_cities"))
pending = []
for ph in t.get("phases", []):
    for fr in ph.get("featured_routes", []):
        if fr.get("_prev_route_id") or fr.get("_node_retag"):
            pending.append(fr)
            print(f"  {fr.get('from_label')} → {fr.get('to_label')}: {fr.get('route_id')} ({fr.get('_link_status')}) render={fr.get('render')}")
print(f"re-tagged routes: {len(pending)}")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #49 Yango Turkey coast split + route re-bind" \
  "$HANDOFF/"

echo "✓ tasklet turkey lane: $SEAL_TAG"