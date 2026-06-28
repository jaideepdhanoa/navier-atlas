#!/usr/bin/env bash
# Gojek 10-market deck economics: per-market aggregate → deck values
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-indonesia"
MODEL="$ROOT/finance/model"
RECAL="$ROOT/finance/recal"
MARKETS="jakarta,bali-nusa-gili,lombok,komodo-flores,sumba,riau-singapore,singapore,raja-ampat,likupang,lake-toba"

step() { echo ""; echo "=== $* ==="; }

step "1 build per-market deck corridors"
python3 "$SCRIPTS/build_gojek_deck_corridors.py"

step "2 aggregate.py (10 deck markets)"
python3 "$MODEL/aggregate.py" \
  --partner gojek \
  --markets "$MARKETS" \
  --corridors "$RECAL/corridors-gojek-deck.json" \
  --json "$RECAL/agg-gojek-deck.json"

step "3 merge deck rows + network rollup"
python3 - <<'PY' "$RECAL"
import json, sys
from pathlib import Path
recal = Path(sys.argv[1])
deck_agg = json.loads((recal / "agg-gojek-deck.json").read_text())
network_agg = json.loads((recal / "agg-gojek.json").read_text())
merged = dict(deck_agg)
rollup = dict(deck_agg.get("rollup") or {})
net_rollup = network_agg.get("rollup") or {}
rollup["grounded_floor_by_market"] = (deck_agg.get("rollup") or {}).get("grounded_floor_by_market") or {}
rollup["n_corridors_total"] = net_rollup.get("n_corridors_total")
merged["rollup"] = rollup
merged["_deck_scope"] = "10-market deck; per-market rows + network corridor count"
(recal / "agg-gojek-deck-merged.json").write_text(json.dumps(merged, indent=2) + "\n")
print(f"wrote {recal / 'agg-gojek-deck-merged.json'} rows={len(merged.get('rows', []))}")
PY

step "4 gen_deck_economics (deck values)"
python3 "$ROOT/deck-studio/decks/gen_deck_economics.py" gojek

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Gojek 10-market deck economics — COMPLETE                     │"
echo "│ agg: finance/recal/agg-gojek-deck.json                        │"
echo "│ values: deck-studio/decks/gojek/deck-economics-values-gojek.json │"
echo "└─────────────────────────────────────────────────────────────┘"