#!/usr/bin/env bash
# Grok Bucket B: Tier 1+2 routing (Lisbon, Al Wakrah, Abidjan, Dammam-Khobar)
# Tier 3 NEOM/Amaala: crosswalk only — no new POI mint (see NODE-ID-CROSSWALK)
#
# Usage:
#   ./scripts/grok-bucketB/run_bucketB.sh
#   BUCKETB_PUSH=1 ./scripts/grok-bucketB/run_bucketB.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
WORK="$ROOT/grok-bucketB-work"
REPO_DC="$ROOT/data-clean"
SCRIPTS="$ROOT/scripts/grok-bucketB"
PHASE3_SCRIPTS="$ROOT/scripts/grok-phase3"

PUSH="${BUCKETB_PUSH:-0}"
TAG="${BUCKETB_TAG:-gold-79an}"
SEAL_LABEL="${BUCKETB_SEAL:-#79an}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

step "1/8 Stage work tree"
rm -rf "$WORK"
mkdir -p "$WORK/atlas-repo/data-clean" "$WORK/grok-routing-output" "$WORK/partner-pitch/_tools"
cp -R "$REPO_DC" "$WORK/atlas-repo/"
cp "$ROOT/grok-routing-output/uae_gulf_land_v2.wkb" "$WORK/partner-pitch/_tools/uae_gulf_land.wkb" 2>/dev/null || true
QA_SRC="$ROOT/_ingest/grok-phase3-ci-pilot-2026-06-18/partner-pitch/_tools/qa_land_crossing.py"
[ -f "$QA_SRC" ] && cp "$QA_SRC" "$WORK/partner-pitch/_tools/"
cp "$ROOT/grok-routing-output/NODE-ID-CROSSWALK-2026-06-19.json" "$WORK/grok-routing-output/"

step "2/8 Apply Tier 1+2 city pins + POIs"
python3 "$SCRIPTS/apply_bucketB.py" --work "$WORK"

step "3/8 Route signature corridors + LB-242 allowlist"
python3 "$SCRIPTS/route_bucketB.py" --work "$WORK"

step "4/8 Bucket B acceptance QA"
python3 - <<'PY' "$WORK"
import json, sys
from pathlib import Path
work = Path(sys.argv[1])
fbt = json.loads((work / "atlas-repo/data-clean/FEATURES_BY_TYPE.json").read_text())
cities = {c["properties"]["id"] for c in fbt.get("city", [])}
targets = ["lisbon-tagus-portugal", "abidjan-cote-divoire", "al-wakrah-qatar", "dammam-khobar-ksa"]
fail = []
for t in targets:
    n = sum(1 for p in fbt["poi"] if p["properties"].get("parent_city_id") == t)
    if t not in cities:
        fail.append(f"missing city pin: {t}")
    if n < 3:
        fail.append(f"too few POIs for {t}: {n}")
if fail:
    print("BUCKETB QA FAIL:", fail)
    sys.exit(1)
print("BUCKETB QA PASS: tier12 cities + POIs OK")
PY

step "5/8 Finalize seal $SEAL_LABEL"
python3 "$SCRIPTS/finalize_seal_bucketB.py" --work "$WORK" --seal "$SEAL_LABEL"

step "6/8 Postflight"
ROUTE_FLOOR="$(python3 -c "import json;print(len(json.load(open('$REPO_DC/ROUTES.json'))))")"
export ROUTE_FLOOR
chmod +x "$PHASE3_SCRIPTS/postflight_pilot.sh"
bash "$PHASE3_SCRIPTS/postflight_pilot.sh" "$WORK"

step "7/8 Sync to repo data-clean"
chmod +x "$PHASE3_SCRIPTS/sync_to_repo.sh"
CHANGELOG="$REPO_DC/CHANGELOG-FOR-CLAUDE-2026-06-19-bucketB-79an.md"
bash "$PHASE3_SCRIPTS/sync_to_repo.sh" "$WORK" "$REPO_DC"
if [ ! -f "$CHANGELOG" ]; then
  cat > "$CHANGELOG" <<EOF
# CHANGELOG — Gold #79an — Bucket B routing (2026-06-19)

**Tier 1+2:** Lisbon Tagus (Transtejo/Soflusa), Al Wakrah→Doha, Abidjan Ébrié lagoon, Dammam–Khobar waterfront.
**Tier 3 hold:** NEOM/Amaala crosswalk to existing RSG POIs (no low-confidence mint).
**Method:** Tasklet BP handoff → Grok apply + route + LB-242 allowlist → reseal.
EOF
fi

if [ "$PUSH" != "1" ]; then
  echo ""
  echo "┌─────────────────────────────────────────────────────────────┐"
  echo "│ Grok Bucket B — DRY RUN COMPLETE                            │"
  echo "├─────────────────────────────────────────────────────────────┤"
  echo "│ seal:      $SEAL_LABEL"
  echo "│ work:      $WORK"
  echo "│ next:      BUCKETB_PUSH=1 $SCRIPTS/run_bucketB.sh"
  echo "└─────────────────────────────────────────────────────────────┘"
  exit 0
fi

cd "$ROOT"
git add data-clean/ scripts/grok-bucketB/ grok-routing-output/NODE-ID-CROSSWALK-2026-06-19.json \
  grok-routing-output/node-crosswalk-report.json docs/NOTES-FOR-TASKLET.md 2>/dev/null || true
git add "$CHANGELOG" 2>/dev/null || true
git commit -m "Gold #79an — Bucket B Tier 1+2 routing (Lisbon, Wakrah, Abidjan, Dammam)"
git tag -a "$TAG" -m "Gold #79an — Bucket B geometry + RSG crosswalk" 2>/dev/null || true
git push origin main
git push origin "$TAG" 2>/dev/null || true
if [ -n "${VERCEL_TOKEN:-}" ] && [ -f "$ROOT/scripts/deploy.sh" ]; then
  "$ROOT/scripts/deploy.sh"
fi
echo "SHIPPED: $SEAL_LABEL tag=$TAG"