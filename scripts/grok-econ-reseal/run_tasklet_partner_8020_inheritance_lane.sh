#!/usr/bin/env bash
# Apply 80-20 inheritance candidate binds + Grab map_scope materialization
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

BY="$ROOT/scripts/grok-bolt-yango"
SEAL_TAG="${SEAL_TAG:-#79bk-partner-8020-inheritance}"

echo "→ Apply 80-20 inheritance candidate binds (195 net-new + LATAM backlog)"
python3 "$ROOT/scripts/apply_partner_8020_inheritance_bindings.py"

echo "→ Re-apply economics-backed route bindings (grab/bolt/yango/uber/indrive/didi)"
python3 "$ROOT/scripts/fix_market_route_bindings.py" --apply --partner grab bolt yango uber indrive didi 2>/dev/null || \
python3 "$ROOT/scripts/fix_market_route_bindings.py" --apply --partner grab bolt yango

echo "→ Gate checks"
python3 - <<'PY'
import json
from pathlib import Path

review = json.loads(Path("handoff/partner-map-model/partner-coverage-80-20-inheritance-review-2026-06-20.json").read_text())
net_new = [r for r in review["candidate_inherited_binds"] if not r["already_in_partner_baseline"]]
target_by_partner = {}
for r in net_new:
    pid = r["partner_id"]
    target_by_partner[pid] = target_by_partner.get(pid, 0) + 1

report = json.loads(Path("handoff/partner-map-model/partner-8020-inheritance-apply-report-2026-06-20.json").read_text())

for pid in ["grab", "bolt", "uber", "yango", "indrive", "didi", "lyft", "gojek"]:
    pj = Path(f"data-clean/partners/{pid}.json")
    if not pj.exists():
        continue
    d = json.loads(pj.read_text())
    bound = sum(1 for x in d.get("network_footprint") or [] if x.get("registry_key"))
    ms = "yes" if d.get("_map_scope") else "no"
    applied = report.get("partners", {}).get(pid, {}).get("rows_applied", 0)
    print(f"  {pid}: bound={bound} map_scope={ms} applied_this_lane={applied}")

grab = json.loads(Path("data-clean/partners/grab.json").read_text())
assert grab.get("_map_scope"), "grab missing _map_scope after materialization"
assert grab["_map_scope"].get("cluster_city_ids"), "grab _map_scope missing cluster_city_ids"
print("  grab _map_scope materialized ✅")

didi = json.loads(Path("data-clean/partners/didi.json").read_text())
didi_bound = sum(1 for x in didi.get("network_footprint") or [] if x.get("registry_key"))
assert didi_bound >= 11, f"didi expected >=11 bound LATAM+China cities, got {didi_bound}"
print(f"  didi LATAM footprint binds: {didi_bound} ✅")

indrive = json.loads(Path("data-clean/partners/indrive.json").read_text())
indrive_bound = sum(1 for x in indrive.get("network_footprint") or [] if x.get("registry_key"))
assert indrive_bound >= 50, f"indrive expected >=50 bound, got {indrive_bound}"
print(f"  indrive footprint binds: {indrive_bound} ✅")
PY

echo "→ Market binding audit"
python3 "$ROOT/scripts/audit_market_route_bindings.py" --partner grab bolt yango 2>&1 | head -15

echo "→ Build-site smoke"
node "$ROOT/scripts/build-site.mjs" 2>&1 | grep -E "ABORT|FATAL|Error" | head -10 || true

echo "→ Reseal"
python3 "$BY/scrub_exclusion_pois.py" --dc data-clean
python3 "$BY/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_TAG"

"$ROOT/scripts/publish-gold.sh" \
  "Gold $SEAL_TAG — 80-20 inheritance binds + Grab map_scope" \
  "handoff/partner-map-model/"

echo "✓ partner 8020 inheritance lane: $SEAL_TAG"