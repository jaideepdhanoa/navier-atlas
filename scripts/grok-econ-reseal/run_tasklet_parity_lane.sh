#!/usr/bin/env bash
# Ingest Tasklet PR #46 — Grab use-cases + SE-Asia bucket de-contamination + TAM refresh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

HANDOFF="${TASKLET_HANDOFF:-$ROOT/_ingest/tasklet-parity-2026-06-20}"
FINANCE="$ROOT/_ingest/gold-delta-LB230-LB241/finance/model"
RECAL="$ROOT/_ingest/sidecar-opex-refresh-2026-06-20"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
ACTIVE_CORR="$ROOT/_ingest/econ-reseal-2026-06-19/econ-reseal/inputs/corridors.json"
SEAL_TAG="${SEAL_TAG:-#79ax-tasklet-parity}"

if [[ ! -f "$HANDOFF/grab.json" ]]; then
  echo "✗ missing $HANDOFF/grab.json" >&2
  exit 1
fi

echo "→ Promote Tasklet parity handoff"
cp "$HANDOFF/grab.json" "$ROOT/data-clean/partners/grab.json"
cp "$HANDOFF/corridors.json" "$FINANCE/corridors.json"
cp "$HANDOFF/corridors.json" "$ACTIVE_CORR"

echo "→ Re-aggregate Grab/Bolt/Yango on de-duplicated registry"
if [[ -f "$FINANCE/vessel-constants.json" && -f "$FINANCE/atom.py" && -f "$FINANCE/country-reference.json" ]]; then
  for p in grab bolt yango; do
    python3 "$FINANCE/aggregate.py" --partner "$p" --json "$RECAL/agg-$p.json"
  done
else
  echo "  WARN finance/model incomplete (missing vessel-constants/atom/country-reference) — skipping aggregate; using existing agg-*.json"
fi

echo "→ Bind growth_case ladders"
for p in grab bolt yango; do
  python3 "$BY/bind_partner_growth_case.py" --partner "$p" --dc data-clean --aggdir "$RECAL"
done

echo "→ Economics sidecar + triage"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$RECAL" \
  --url-map "$RECAL/economics_url_map.json"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path
grab = json.loads(Path('data-clean/partners/grab.json').read_text())
uc = 0
empty = 0
for m in grab.get('markets', []):
    for ph in m.get('phases', []):
        for u in ph.get('use_cases', []) or []:
            uc += 1
            if not (u.get('summary') or '').strip():
                empty += 1
agg = json.loads(Path('_ingest/sidecar-opex-refresh-2026-06-20/agg-grab.json').read_text())
gf = agg.get('rollup', {}).get('grounded_floor', {})
print(f"grab use_cases: {uc} total, {empty} empty")
print(f"grab grounded_floor: ${gf.get('market_rev_yr', 0)/1e6:.1f}M")
for p in ('bolt', 'yango', 'grab'):
    part = json.loads(Path(f'data-clean/partners/{p}.json').read_text())
    gc = part.get('growth_case', {})
    rungs = (gc.get('revenue_potential') or {}).get('rungs') or []
    lt = len(gc.get('ladder_transitions') or [])
    print(f"{p}: growth_case rungs={len(rungs)} ladder_transitions={lt}")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — Tasklet PR #46 Grab parity + TAM refresh" \
  "$HANDOFF/"

echo "✓ tasklet parity lane: $SEAL_TAG"