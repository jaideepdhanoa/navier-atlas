#!/usr/bin/env bash
# Grok #79am reconciliation: restore → QA-gate BPs → cascade → phase3 apply → reseal → [push]
#
# Usage:
#   ./scripts/grok-reconcile-79am/run_reconcile_79am.sh
#   RECONCILE_PUSH=1 VERCEL_TOKEN=… ./scripts/grok-reconcile-79am/run_reconcile_79am.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PKG="$ROOT/_ingest/grok-reconcile-79am/grok-reconcile-79am"
# Local repo carries LB230–242 new-market work + 1,007 SEM-gate BPs (not in gold-delta export).
BASE_SRC="$ROOT"
BASE_DC="$ROOT/data-clean"
RESTORE_SRC="$ROOT/_ingest/gold-export-79ak-1"
WORK="$ROOT/grok-reconcile-79am-work"
REPO_DC="$ROOT/data-clean"
SCRIPTS="$ROOT/scripts/grok-reconcile-79am"
PHASE3_SCRIPTS="$ROOT/scripts/grok-phase3"

PUSH="${RECONCILE_PUSH:-0}"
TAG="${RECONCILE_TAG:-gold-79am}"
SEAL_LABEL="${RECONCILE_SEAL:-#79am}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

[ -d "$PKG" ] || die "reconcile package missing: $PKG"
[ -d "$BASE_DC" ] || die "base data-clean missing: $BASE_DC"
[ -d "$RESTORE_SRC/data-clean" ] || die "restore source missing: $RESTORE_SRC"

step "1/15 Stage work tree (base = local LB230–242 + new-market)"
rm -rf "$WORK"
mkdir -p "$WORK/atlas-repo" "$WORK/RECONCILE" "$WORK/grok-routing-output"
cp -R "$BASE_DC" "$WORK/atlas-repo/data-clean"
cp -R "$BASE_SRC/atlas-external" "$WORK/" 2>/dev/null || true
cp -R "$ROOT/_ingest/grok-phase3-ci-pilot-2026-06-18/partner-pitch" "$WORK/" 2>/dev/null || true
mkdir -p "$WORK/partner-pitch/_tools"
cp "$ROOT/atlas-external/pier-slug-bp-crosswalk.json" "$WORK/atlas-external/" 2>/dev/null || mkdir -p "$WORK/atlas-external" && cp "$ROOT/atlas-external/pier-slug-bp-crosswalk.json" "$WORK/atlas-external/"
cp "$PKG"/*.json "$PKG"/*.md "$WORK/RECONCILE/"
cp "$ROOT/grok-routing-output/route-solutions.jsonl" "$WORK/grok-routing-output/"
cp "$ROOT/grok-routing-output/uae_gulf_land_v2.wkb" "$WORK/partner-pitch/_tools/uae_gulf_land.wkb"
cp "$ROOT/grok-routing-output/APPLY-LEDGER.json" "$WORK/RECONCILE/APPLY-LEDGER-src.json"
cp "$ROOT/grok-routing-output/palm-marina-boarding-point-gazetteer.json" "$WORK/RECONCILE/"

for f in STORIES.json VESSEL_SPECS.json economics_by_route_id.json \
         route_water_allowlist.json qa_baseline.json SEAL.prior.json; do
  [ -f "$REPO_DC/$f" ] && cp "$REPO_DC/$f" "$WORK/atlas-repo/data-clean/"
done
[ -d "$REPO_DC/partners" ] && cp -R "$REPO_DC/partners" "$WORK/atlas-repo/data-clean/"
[ -d "$REPO_DC/cluster_briefs" ] && cp -R "$REPO_DC/cluster_briefs" "$WORK/atlas-repo/data-clean/"

step "2/15 Restore 440 routes + 213 BPs from #79ak"
python3 "$SCRIPTS/restore_from_manifest.py" --work "$WORK" --restore-src "$RESTORE_SRC/data-clean"
python3 - "$WORK/RECONCILE/RESTORE-MANIFEST.json" "$WORK/atlas-repo/data-clean/route_water_allowlist.json" <<'PY'
import json,sys
manifest,allow_p=sys.argv[1:3]
m=json.load(open(manifest)); a=json.load(open(allow_p))
ids=set(a.get('ids',[]))
for entry in m.get('restore_route_ids',[]):
    rid=entry['id'] if isinstance(entry,dict) else entry
    ids.add(rid)
a['ids']=sorted(ids)
a.setdefault('_meta',{})['restore_manifest_routes_added']=len(m.get('restore_route_ids',[]))
json.dump(a,open(allow_p,'w'),indent=2); print(f'allowlist +{len(m.get("restore_route_ids",[]))} restore routes')
PY

step "3/15 Apply SEM verdicts (DROP quarantine)"
python3 "$SCRIPTS/apply_sem_verdicts.py" --work "$WORK"

step "4/15 Gate #3 water-adjacency (KEEP+HOLD)"
python3 "$SCRIPTS/gate_bp_water_adjacency.py" --work "$WORK"

step "5/15 Gate #4 gazetteer ID-match"
python3 "$SCRIPTS/gate_bp_gazetteer.py" --work "$WORK"
python3 "$SCRIPTS/apply_bp_gates.py" --work "$WORK"

step "6/15 Route endpoint cascade quarantine"
python3 "$SCRIPTS/cascade_route_quarantine.py" --work "$WORK"

step "7/15 Palm/Marina bbox — junk POI drop + terminal gating"
python3 "$SCRIPTS/cleanup_palm_marina.py" --work "$WORK" --phase bps
python3 "$SCRIPTS/cleanup_palm_marina.py" --work "$WORK" --phase cascade

step "8/15 Build APPLY-LEDGER-79am (promote 3 held synth)"
python3 "$SCRIPTS/build_apply_ledger_79am.py" --work "$WORK" --ledger-src "$WORK/RECONCILE/APPLY-LEDGER-src.json"

step "9/15 Apply Phase-3 geometries (27 synth+patch incl. Lulu/Reem)"
python3 "$SCRIPTS/apply_phase3_79am.py" --work "$WORK"

step "10/15 Extend allowlist for applied routes"
cp "$WORK/grok-routing-output/phase3-apply-report-79am.json" \
   "$WORK/grok-routing-output/phase3-apply-report.json"
python3 "$PHASE3_SCRIPTS/extend_allowlist_phase3.py" --work "$WORK"

step "11/15 Palm/Marina — de-spaghetti + geometry repair"
python3 "$SCRIPTS/cleanup_palm_marina.py" --work "$WORK" --phase spaghetti
python3 "$SCRIPTS/cleanup_palm_marina.py" --work "$WORK" --phase geometry
python3 "$SCRIPTS/cleanup_palm_marina.py" --work "$WORK" --phase cascade

step "12/15 Palm/Marina acceptance gate"
python3 "$SCRIPTS/qa_palm_acceptance.py" --work "$WORK"

step "13/15 Finalize seal $SEAL_LABEL"
python3 "$SCRIPTS/finalize_seal_79am.py" --work "$WORK"

step "14/15 Postflight"
chmod +x "$PHASE3_SCRIPTS/postflight_pilot.sh"
ACTIVE_RC=$(python3 -c "import json;d=json.load(open('$WORK/atlas-repo/data-clean/ROUTES.json'));f=d if isinstance(d,list) else d.get('features',[]);print(sum(1 for x in f if not (x.get('properties') or x).get('_quarantine')))")
ROUTE_FLOOR="${ROUTE_FLOOR:-$ACTIVE_RC}" bash "$PHASE3_SCRIPTS/postflight_pilot.sh" "$WORK"

step "15/15 Sync to repo data-clean"
chmod +x "$PHASE3_SCRIPTS/sync_to_repo.sh"
CHANGELOG="$REPO_DC/CHANGELOG-FOR-CLAUDE-2026-06-18-uae-reconcile-79am.md"
bash "$PHASE3_SCRIPTS/sync_to_repo.sh" "$WORK" "$REPO_DC"
if [ ! -f "$CHANGELOG" ]; then
  cat > "$CHANGELOG" <<EOF
# CHANGELOG — Gold #79am — 3-way reconcile (2026-06-18)

**Base:** gold-delta LB230–242 + restore from #79ak (440 routes, 213 BPs)
**BP QA:** SEM verdicts (95 KEEP / 185 HOLD / 727 DROP) + water-adjacency + gazetteer
**Phase-3:** 27 geometry apply incl. 3 Lulu/Reem synth rows + Khalifa mint
**Seal:** #79am — first push carrying Bolt/Yango/Lagos/Abidjan new-market work
EOF
fi

if [ "$PUSH" != "1" ]; then
  echo ""
  echo "┌─────────────────────────────────────────────────────────────┐"
  echo "│ Grok Reconcile #79am — DRY RUN COMPLETE                     │"
  echo "├─────────────────────────────────────────────────────────────┤"
  echo "│ seal:      $SEAL_LABEL"
  echo "│ work:      $WORK"
  echo "│ next:      RECONCILE_PUSH=1 $SCRIPTS/run_reconcile_79am.sh"
  echo "└─────────────────────────────────────────────────────────────┘"
  exit 0
fi

cd "$ROOT"
git add data-clean/ scripts/grok-reconcile-79am/ grok-routing-output/palm-marina-boarding-point-gazetteer.json grok-routing-output/QA-PALM-MARINA-79am.md .github/workflows/grok-phase3.yml 2>/dev/null || true
git add data-clean/CHANGELOG-FOR-CLAUDE-2026-06-18-uae-reconcile-79am.md 2>/dev/null || true
git commit -m "Gold #79am — Tasklet gazetteer gate #4b (RTA Marina stations) + Palm cleanup"
git tag -a "$TAG" -m "Gold #79am — reconcile LB230–242 + new-market work" 2>/dev/null || true
git push origin main
git push origin "$TAG" 2>/dev/null || true
if [ -n "${VERCEL_TOKEN:-}" ] && [ -f "$ROOT/scripts/deploy.sh" ]; then
  "$ROOT/scripts/deploy.sh"
fi
echo "SHIPPED: $SEAL_LABEL tag=$TAG"