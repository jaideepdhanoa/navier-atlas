#!/usr/bin/env bash
# Ingest Tasklet PR #47 — Phase-3 backbone routes + penang/borneo corridors + narrative polish
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

HANDOFF="${TASKLET_HANDOFF:-$ROOT/_ingest/tasklet-subpage-parity-2026-06-20b}"
ACTIVE_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
FINANCE="$ROOT/_ingest/gold-delta-LB230-LB241/finance/model"
RECAL="$ROOT/_ingest/sidecar-opex-refresh-2026-06-20"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#79ay-tasklet-subpage-parity}"

if [[ ! -f "$HANDOFF/bolt.json" ]]; then
  echo "✗ missing $HANDOFF/bolt.json" >&2
  exit 1
fi

echo "→ Promote penang/borneo de-contaminated corridors.json"
cp "$HANDOFF/corridors.json" "$ACTIVE_CORR"
cp "$HANDOFF/corridors.json" "$FINANCE/corridors.json"

echo "→ Mint any pending corridor routes (Italy Portofino, Lagos Badagry, …)"
python3 "$ECON/mint_pending_corridor_routes.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Splice bolt/yango sub-pages + bind Phase-3 featured_routes"
python3 "$ECON/splice_tasklet_subpage.py" --handoff "$HANDOFF" --corridors "$ACTIVE_CORR"

echo "→ Economics sidecar"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$RECAL" \
  --url-map "$RECAL/economics_url_map.json"

if [[ -f "$FINANCE/vessel-constants.json" ]]; then
  echo "→ Re-aggregate Grab (penang/borneo correction)"
  python3 "$FINANCE/aggregate.py" --partner grab --json "$RECAL/agg-grab.json" || true
  python3 "$BY/bind_partner_growth_case.py" --partner grab --dc data-clean --aggdir "$RECAL" || true
fi

echo "→ Triage + reseal"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
r = json.loads(Path("grok-routing-output/tasklet-subpage-splice-report.json").read_text())
pending = [x for x in r["phase3_backbone"] if not x.get("route_id")]
linked = [x for x in r["phase3_backbone"] if x.get("route_id")]
print(f"phase3_backbone: {len(linked)} linked, {len(pending)} still pending")
for x in pending:
    print(f"  PENDING {x['partner']}/{x['market']}: {x['from']} → {x['to']} ({x['status']})")
econ = json.loads(Path("data-clean/economics_by_route_id.json").read_text())
m = econ["_meta"]
p = len(econ["_pending_route_pin"])
print(f"economics: {m['records']} pinned, {p} pending")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — Tasklet PR #47 sub-page parity + Phase-3 binds" \
  "$HANDOFF/"

echo "✓ tasklet subpage lane: $SEAL_TAG"