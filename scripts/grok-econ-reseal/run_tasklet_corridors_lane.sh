#!/usr/bin/env bash
# Ingest Tasklet corridors handoff (GitHub PR → _ingest/tasklet-handoff-*/)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
HANDOFF="${TASKLET_HANDOFF:-$ROOT/_ingest/tasklet-handoff-2026-06-20}"
ACTIVE_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
OPEX="$ROOT/_ingest/sidecar-opex-refresh-2026-06-20"
BP_INGEST="$ROOT/_ingest/bp-seal-2026-06-20"
SEAL_TAG="${SEAL_TAG:-#79au-tasklet-corridors}"

if [[ ! -f "$HANDOFF/corridors.json" ]]; then
  echo "✗ missing $HANDOFF/corridors.json" >&2
  exit 1
fi

echo "→ Promote Tasklet corridors.json → active ingest path"
cp "$HANDOFF/corridors.json" "$ACTIVE_CORR"

echo "→ GCN remainder (Qatar + any declared gcn-* rows)"
python3 "$ECON/mint_gcn_corridor_routes.py" --dc data-clean --corridors "$ACTIVE_CORR" || true

echo "→ Partner rebind"
python3 "$BY/apply_bolt_yango.py" --dc data-clean --ingest "$BP_INGEST"

echo "→ Economics sidecar rebuild"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$OPEX" \
  --url-map "$OPEX/economics_url_map.json"

echo "→ Triage"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Reseal"
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
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — Tasklet corridors ingest (Egypt + Qatar)" \
  "$HANDOFF/"

echo "✓ tasklet corridors lane: $SEAL_TAG"