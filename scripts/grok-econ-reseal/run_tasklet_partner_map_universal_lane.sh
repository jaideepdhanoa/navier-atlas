#!/usr/bin/env bash
# PR #55 — universal partner map model + exact-binding coastal inheritance
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#79bh-partner-map-universal}"

echo "→ Apply exact-binding + coastal inheritance (PR #55)"
python3 "$ROOT/scripts/apply_partner_coverage_bindings.py"

echo "→ Materialize _map_scope from seal-scope (bolt/yango)"
python3 "$ROOT/scripts/materialize_partner_map_scope.py" bolt yango

echo "→ Re-apply economics-backed route bindings (grab/bolt/yango)"
python3 "$ROOT/scripts/fix_market_route_bindings.py" --apply --partner grab bolt yango

echo "→ Gate checks"
python3 - <<'PY'
import json
from pathlib import Path

def check(pid, min_bound=None):
    d = json.loads(Path(f"data-clean/partners/{pid}.json").read_text())
    fp = d.get("network_footprint") or []
    bound = sum(1 for x in fp if x.get("registry_key"))
    print(f"  {pid}: footprint={len(fp)} bound={bound} map_scope={'yes' if d.get('_map_scope') else 'no'}")
    if min_bound is not None:
        assert bound >= min_bound, f"{pid}: expected >={min_bound} bound, got {bound}"

check("bolt", 18)
check("yango", 15)
check("uber", 10)
check("lyft", 1)
check("kakao-mobility", 1)
check("four-seasons", 1)
check("grab", 10)

# bolt crete/malta promotions
bolt = json.loads(Path("data-clean/partners/bolt.json").read_text())
keys = {x.get("registry_key") for x in bolt.get("network_footprint") or []}
assert "crete-greece" in keys, "bolt missing crete-greece promotion"
assert "malta-gozo" in keys, "bolt missing malta-gozo promotion"
print("  bolt P0 promotions: crete-greece + malta-gozo ✅")
PY

echo "→ Market binding audit (grab/bolt/yango)"
python3 "$ROOT/scripts/audit_market_route_bindings.py" --partner grab bolt yango 2>&1 | head -15

echo "→ Build-site smoke"
node "$ROOT/scripts/build-site.mjs" 2>&1 | grep -E "ABORT|FATAL|Error" | head -10 || true

echo "→ Reseal (partner JSON + handoff only)"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #55 partner map universal + exact bindings" \
  "handoff/partner-map-model/"

echo "✓ partner map universal lane: $SEAL_TAG"