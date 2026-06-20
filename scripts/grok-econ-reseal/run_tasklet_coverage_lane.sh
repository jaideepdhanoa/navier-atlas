#!/usr/bin/env bash
# PR #51 + PR #52 — saudi-pif forward-SAM cascade, uber scoped inheritance, french-polynesia page
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FINANCE_MODEL="$ROOT/finance/model"
FINANCE="$ROOT/finance"
RECAL="$FINANCE/recal"
ACTIVE_CORR="$FINANCE_MODEL/corridors.json"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#79bd-tasklet-coverage}"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"

mkdir -p "$GROWTH_DRAFT" "$RECAL"

cascade_partner() {
  local p="$1" agg="$2" corridors="$3"
  shift 3
  local engine_p="$p"
  local extra_growth=()
  while [[ $# -gt 0 ]]; do
    if [[ "$1" == "--engine" ]]; then engine_p="$2"; shift 2
    else extra_growth+=("$1"); shift; fi
  done
  echo "  [$p] aggregate (engine=$engine_p)"
  python3 "$FINANCE_MODEL/aggregate.py" --partner "$engine_p" --json "$agg" --corridors "$corridors"
  echo "  [$p] growth"
  if ((${#extra_growth[@]})); then
    python3 "$FINANCE_MODEL/growth.py" --partner "$p" --agg "$agg" \
      --json "$RECAL/growth-$p.json" "${extra_growth[@]}"
  else
    python3 "$FINANCE_MODEL/growth.py" --partner "$p" --agg "$agg" \
      --json "$RECAL/growth-$p.json"
  fi
  echo "  [$p] frontend_block"
  python3 "$FINANCE_MODEL/growth_frontend_block.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" --rollup "$agg" \
    --out "$GROWTH_DRAFT/$p.growth.json"
  echo "  [$p] splice → data-clean"
  local pj="$ROOT/data-clean/partners/$p.json"
  if [[ ! -f "$pj" ]]; then
    echo "✗ missing $pj" >&2
    exit 1
  fi
  cp "$pj" "$ROOT/partner-pitch/partners/$p.json" 2>/dev/null || true
  python3 "$FINANCE/splice_growth_into_partner.py" --partner "$p" \
    --growth "$RECAL/growth-$p.json" --frontend "$GROWTH_DRAFT/$p.growth.json" \
    --partner-json "$pj"
  cp "$pj" "$ROOT/partner-pitch/partners/$p.json"
}

echo "→ PR #51: saudi-pif forward-SAM cascade (engine slug saudi-redsea-pif)"
cascade_partner saudi-pif "$RECAL/agg-saudi-pif.json" "$ACTIVE_CORR" --engine saudi-redsea-pif --greenfield off
cp "$RECAL/agg-saudi-pif.json" "$RECAL/agg-saudi-redsea-pif.json"

echo "→ PR #51: uber scoped inheritance (LB-257)"
python3 "$FINANCE/build_scoped_corridors.py" --partner uber --out "$RECAL/corridors-uber.json"
cascade_partner uber "$RECAL/agg-uber.json" "$RECAL/corridors-uber.json"

echo "→ PR #52: french-polynesia full cascade (captive-aware)"
cascade_partner french-polynesia "$RECAL/agg-french-polynesia.json" "$ACTIVE_CORR" --greenfield off

echo "→ Clear french-polynesia pending flag"
python3 - <<'PY'
import json
from pathlib import Path
p = Path("data-clean/partners/french-polynesia.json")
d = json.loads(p.read_text())
d.pop("_pending_cascade_reconciliation", None)
p.write_text(json.dumps(d, indent=2) + "\n")
Path("partner-pitch/partners/french-polynesia.json").write_text(p.read_text())
print("cleared _pending_cascade_reconciliation")
PY

echo "→ Economics sidecar (add uber + french-polynesia)"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean \
  --corridors "$ACTIVE_CORR" \
  --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"

python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

python3 - <<'PY'
import json
from pathlib import Path

def summarize(p):
    part = json.loads(Path(f"data-clean/partners/{p}.json").read_text())
    gc = part.get("growth_case", {})
    rungs = (gc.get("revenue_potential") or {}).get("rungs") or []
    som = next((r for r in rungs if r.get("id") == "som_floor"), {})
    print(f"{p}: rungs={len(rungs)} som_floor_mid={som.get('display',{}).get('mid','—')} "
          f"anchor={gc.get('_headline_anchor','grounded')} forward_sam={gc.get('_forward_sam_only', False)}")

for p in ("saudi-pif", "uber", "french-polynesia"):
    summarize(p)

for p in ("saudi-pif", "uber", "french-polynesia"):
    agg = Path(f"finance/recal/agg-{p}.json")
    if agg.exists():
        r = json.loads(agg.read_text())["rollup"]
        print(f"agg-{p}: grounded=${r['grounded_floor']['market_rev_yr']/1e6:.1f}M "
              f"forward_sam=${r.get('forward_sam',{}).get('market_rev_yr',0)/1e6:.1f}M")
PY

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #51 saudi-pif/uber inheritance + PR #52 french-polynesia cascade" \
  "finance/"

echo "✓ tasklet coverage lane: $SEAL_TAG"