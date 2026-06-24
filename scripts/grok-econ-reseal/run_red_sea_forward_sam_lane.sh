#!/usr/bin/env bash
# LB-259 — red-sea-global forward-SAM cascade + growth splice (clears bogus $162M grounded floor)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

FINANCE_MODEL="$ROOT/finance/model"
FINANCE="$ROOT/finance"
RECAL="$FINANCE/recal"
BY="$ROOT/scripts/grok-bolt-yango"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#79bf-red-sea-forward-sam}"
GROWTH_DRAFT="$ROOT/partner-pitch/partners/_growth-draft"
ACTIVE_CORR="$FINANCE_MODEL/corridors.json"

mkdir -p "$GROWTH_DRAFT" "$RECAL"

P=red-sea-global
AGG="$RECAL/agg-$P.json"
GROWTH="$RECAL/growth-$P.json"
FRONT="$GROWTH_DRAFT/$P.growth.json"
PARTNER="$ROOT/data-clean/partners/$P.json"

echo "→ [$P] aggregate"
python3 "$FINANCE_MODEL/aggregate.py" --partner "$P" --json "$AGG" --corridors "$ACTIVE_CORR"

echo "→ [$P] growth (greenfield off, forward-SAM anchor)"
python3 "$FINANCE_MODEL/growth.py" --partner "$P" --agg "$AGG" --greenfield off --json "$GROWTH"

echo "→ [$P] frontend_block + splice"
python3 "$FINANCE_MODEL/growth_frontend_block.py" --partner "$P" \
  --partner-json "$PARTNER" \
  --growth "$GROWTH" --rollup "$AGG" --out "$FRONT"
cp "$PARTNER" "$ROOT/partner-pitch/partners/$P.json" 2>/dev/null || true
python3 "$FINANCE/splice_growth_into_partner.py" --partner "$P" \
  --growth "$GROWTH" --frontend "$FRONT" --partner-json "$PARTNER"
cp "$PARTNER" "$ROOT/partner-pitch/partners/$P.json"

echo "→ economics sidecar + triage"
python3 "$BY/build_economics_sidecar.py" \
  --dc data-clean --corridors "$ACTIVE_CORR" --aggdir "$RECAL" \
  --url-map "$FINANCE/economics_url_map.json"
python3 "$ECON/triage_pending_economics.py" --dc data-clean --corridors "$ACTIVE_CORR"

python3 - <<'PY'
import json
from pathlib import Path
p = Path("data-clean/partners/red-sea-global.json")
d = json.loads(p.read_text())
agg = json.loads(Path("finance/recal/agg-red-sea-global.json").read_text())["rollup"]
fwd = agg["forward_sam"]
som = next(r["display"]["mid"] for r in d["growth_case"]["revenue_potential"]["rungs"] if r["id"] == "som_floor")
print(f"red-sea-global: som_floor={som} grounded=${agg['grounded_floor']['market_rev_yr']/1e6:.1f}M "
      f"forward_sam=${fwd['market_rev_yr']/1e6:.1f}M anchor={d['growth_case'].get('_headline_anchor')}")
PY

echo "✓ red-sea forward-SAM lane: $SEAL_TAG"