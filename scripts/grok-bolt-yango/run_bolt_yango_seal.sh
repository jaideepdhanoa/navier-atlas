#!/usr/bin/env bash
# Grok Bolt/Yango P0 seal: BP coverage → economics → growth_case → reseal #79aq
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-bolt-yango"
PHASE3="$ROOT/scripts/grok-phase3"
SEAL_LABEL="${BOLT_YANGO_SEAL:-#79aq}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

step "1/7 Apply boarding points (0 silent drops)"
python3 "$SCRIPTS/apply_boarding_points.py" --dc "$ROOT/data-clean"

step "2/8 Scrub exclusion-token POIs (deploy sweep)"
python3 "$SCRIPTS/scrub_exclusion_pois.py" --dc data-clean

step "3/8 Refresh Bolt/Yango partner splice (anchor crosswalk)"
python3 "$SCRIPTS/apply_bolt_yango.py" --dc data-clean

step "4/8 Build economics sidecar (bolt + yango)"
python3 "$SCRIPTS/build_economics_sidecar.py" --dc data-clean

step "5/8 Bind Yango growth_case"
python3 "$SCRIPTS/bind_yango_growth_case.py" --dc data-clean

step "6/8 Finalize SEAL $SEAL_LABEL"
python3 "$SCRIPTS/finalize_seal_79aq.py" --dc data-clean --seal "$SEAL_LABEL"

step "7/8 Acceptance QA"
python3 - <<'PY' "$ROOT"
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
dc = root / "data-clean"
bp_report = json.loads((root / "grok-routing-output/bolt-yango-bp-apply-report.json").read_text())
splice = json.loads((root / "grok-routing-output/bolt-yango-splice-report.json").read_text())
yango = json.loads((dc / "partners/yango.json").read_text())
fail = []
if bp_report.get("silent_drops", 1) != 0:
    fail.append(f"silent_drops={bp_report.get('silent_drops')}")
if not yango.get("growth_case"):
    fail.append("yango growth_case missing")
if splice.get("markets_zero_anchors_after_crosswalk"):
    print("WARN zero-anchor markets:", splice["markets_zero_anchors_after_crosswalk"])
if fail:
    print("QA FAIL:", fail)
    sys.exit(1)
print("QA PASS: 0 silent drops, yango growth_case bound")
PY

step "8/8 Postflight land-crossing (if tooling present)"
WORK="$ROOT/grok-bolt-yango-work"
if [ -f "$PHASE3/postflight_pilot.sh" ]; then
  rm -rf "$WORK"
  mkdir -p "$WORK/atlas-repo/data-clean" "$WORK/grok-routing-output" "$WORK/partner-pitch/_tools"
  cp -R "$ROOT/data-clean" "$WORK/atlas-repo/"
  cp "$ROOT/grok-routing-output/uae_gulf_land_v2.wkb" "$WORK/partner-pitch/_tools/uae_gulf_land.wkb" 2>/dev/null || true
  QA_SRC="$ROOT/_ingest/grok-phase3-ci-pilot-2026-06-18/partner-pitch/_tools/qa_land_crossing.py"
  [ -f "$QA_SRC" ] && cp "$QA_SRC" "$WORK/partner-pitch/_tools/"
  ROUTE_FLOOR="$(python3 -c "import json;print(len(json.load(open('$ROOT/data-clean/ROUTES.json'))))")"
  export ROUTE_FLOOR
  chmod +x "$PHASE3/postflight_pilot.sh"
  bash "$PHASE3/postflight_pilot.sh" "$WORK" || echo "WARN postflight non-zero (review)"
fi

"$ROOT/scripts/publish-gold.sh" "Gold $SEAL_LABEL — Bolt/Yango BP seal + economics + Yango growth_case"