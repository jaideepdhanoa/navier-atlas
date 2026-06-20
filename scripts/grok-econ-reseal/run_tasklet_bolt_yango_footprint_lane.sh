#!/usr/bin/env bash
# PR #53 — Bolt/Yango UAE-first ordering + full operating-footprint roster
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#79be-bolt-yango-footprint}"

echo "→ Sync partner-pitch mirrors"
cp data-clean/partners/bolt.json partner-pitch/partners/bolt.json
cp data-clean/partners/yango.json partner-pitch/partners/yango.json

echo "→ Gate checks (UAE-first + Turkey anchor IDs + footprint honesty)"
python3 - <<'PY'
import json
from pathlib import Path

brief_ids = {f.stem for f in Path("data-clean/city_briefs").iterdir() if f.suffix == ".json"}

def check_partner(pid):
    d = json.loads(Path(f"data-clean/partners/{pid}.json").read_text())
    assert d["markets"][0]["id"] == "uae", f"{pid}: markets[0] must be uae, got {d['markets'][0]['id']}"
    uae = d["markets"][0]
    assert uae.get("recommended_entry") is True, f"{pid}: uae must carry recommended_entry"
    fp = d.get("network_footprint") or []
    tiers = {}
    for row in fp:
        tiers[row["tier"]] = tiers.get(row["tier"], 0) + 1
    assert tiers.get("flagship") == 1, f"{pid}: expected 1 flagship"
    nm = d.get("non_marine_footprint") or []
    print(f"  {pid}: uae-first ✅ | footprint tiers={tiers} | non_marine={len(nm)}")
    if pid == "yango":
        t = next(m for m in d["markets"] if m["id"] == "turkey")
        for a in t.get("anchor_cities", []):
            cid = a if isinstance(a, str) else (a.get("city_id") or a.get("id"))
            assert cid in brief_ids, f"yango/turkey anchor {cid} missing city brief"
        print(f"  yango/turkey anchors: all briefs present ✅")

check_partner("bolt")
check_partner("yango")

xw = Path("partner-pitch/BOLT-YANGO-BRIEF-PARITY-CROSSWALK.json")
assert xw.exists(), "missing brief-parity crosswalk"
print("  crosswalk:", xw.name, "✅")
PY

echo "→ Reseal (partner JSON only — no corridor/econ cascade)"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — PR #53 Bolt/Yango UAE-first footprint roster" \
  "partner-pitch/BOLT-YANGO-BRIEF-PARITY-CROSSWALK.json"

echo "✓ bolt-yango footprint lane: $SEAL_TAG"