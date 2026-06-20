#!/usr/bin/env bash
# Grok Phase-3 CI: apply → seal → postflight → [sync → git tag → deploy]
#
# Usage:
#   ./scripts/grok-phase3/run_phase3.sh              # dry-run (no git/deploy)
#   PHASE3_PUSH=1 ./scripts/grok-phase3/run_phase3.sh   # commit tag gold-79al + deploy
#
# Requires: python3, shapely, global-land-mask (uv or pip)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
PILOT_SRC="$ROOT/_ingest/grok-phase3-ci-pilot-2026-06-18"
WORK="$ROOT/grok-phase3-work"
REPO_DC="$ROOT/data-clean"
SCRIPTS="$ROOT/scripts/grok-phase3"

PUSH="${PHASE3_PUSH:-0}"
TAG="${PHASE3_TAG:-gold-79al}"
SEAL_LABEL="${PHASE3_SEAL:-#79al}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

[ -d "$PILOT_SRC" ] || die "pilot bundle missing: $PILOT_SRC"

step "1/8 Stage work tree"
rm -rf "$WORK"
mkdir -p "$WORK/atlas-repo"
cp -R "$PILOT_SRC/atlas-external" "$PILOT_SRC/partner-pitch" "$PILOT_SRC/grok-routing-output" "$WORK/"
cp -R "$PILOT_SRC/atlas-repo/data-clean" "$WORK/atlas-repo/"
cp "$PILOT_SRC/APPLY-LEDGER.json" "$WORK/"
cp "$ROOT/grok-routing-output/route-solutions.jsonl" "$WORK/grok-routing-output/" 2>/dev/null || true

step "2/8 Seed deploy blobs from repo data-clean"
for f in STORIES.json VESSEL_SPECS.json economics_by_route_id.json; do
  [ -f "$REPO_DC/$f" ] && cp "$REPO_DC/$f" "$WORK/atlas-repo/data-clean/"
done
[ -d "$REPO_DC/partners" ] && cp -R "$REPO_DC/partners" "$WORK/atlas-repo/data-clean/"
[ -d "$REPO_DC/city_briefs" ] && cp -R "$REPO_DC/city_briefs" "$WORK/atlas-repo/data-clean/"
[ -d "$REPO_DC/cluster_briefs" ] && cp -R "$REPO_DC/cluster_briefs" "$WORK/atlas-repo/data-clean/"

cp "$ROOT/grok-routing-output/uae_gulf_land_v2.wkb" \
   "$WORK/partner-pitch/_tools/uae_gulf_land.wkb"

step "3/8 Apply (APPLY-LEDGER.json)"
python3 "$SCRIPTS/apply_phase3.py" --work "$WORK"

step "4/8 Extend allowlist (Phase-3 applied ids)"
python3 "$SCRIPTS/extend_allowlist_phase3.py" --work "$WORK"

step "5/8 Finalize seal ($SEAL_LABEL)"
python3 "$SCRIPTS/finalize_seal.py" --work "$WORK"

step "6/8 Postflight (LB-224 v2)"
chmod +x "$SCRIPTS/postflight_pilot.sh"
bash "$SCRIPTS/postflight_pilot.sh" "$WORK"

step "7/8 Sync to repo data-clean"
chmod +x "$SCRIPTS/sync_to_repo.sh"
bash "$SCRIPTS/sync_to_repo.sh" "$WORK" "$REPO_DC"

APPLY_REPORT="$WORK/grok-routing-output/phase3-apply-report.json"
COMMIT_SHA="local-dry-run"
if [ -f "$ROOT/.git/HEAD" ]; then
  COMMIT_SHA="$(git -C "$ROOT" rev-parse HEAD 2>/dev/null || echo local-dry-run)"
fi

if [ "$PUSH" != "1" ]; then
  step "8/8 Skipped git/deploy (set PHASE3_PUSH=1 to ship)"
  echo ""
  echo "┌─────────────────────────────────────────────────────────────┐"
  echo "│ Grok Phase-3 CI — DRY RUN COMPLETE                          │"
  echo "├─────────────────────────────────────────────────────────────┤"
  echo "│ seal:      $SEAL_LABEL"
  echo "│ work:      $WORK"
  echo "│ report:    $APPLY_REPORT"
  echo "│ next:      PHASE3_PUSH=1 $SCRIPTS/run_phase3.sh"
  echo "└─────────────────────────────────────────────────────────────┘"
  exit 0
fi

step "8/8 Git commit + tag + Vercel deploy"
cd "$ROOT"
git add data-clean/ROUTES.json data-clean/FEATURES_BY_TYPE.json data-clean/SEAL.json \
        data-clean/qa_land_crossing_report.json data-clean/route_water_allowlist.json \
        data-clean/CHANGELOG-FOR-CLAUDE-2026-06-18-uae-phase3-79al.md 2>/dev/null || true
git add grok-routing-output/phase3-apply-report.json 2>/dev/null || true

if git diff --cached --quiet; then
  die "nothing to commit — data-clean unchanged?"
fi

git commit -m "Gold #79al — Grok Phase 3 UAE geometry apply (24 routes, 3 held)"

if git rev-parse "$TAG" >/dev/null 2>&1; then
  echo "  tag $TAG exists — skipping annotate"
else
  git tag -a "$TAG" -m "Gold #79al — Phase 3 UAE geometry pilot (Grok CI)"
fi

COMMIT_SHA="$(git rev-parse HEAD)"
git push origin main
git push origin "$TAG" 2>/dev/null || git push origin "$TAG"

if [ -n "${VERCEL_TOKEN:-}" ] && [ -f "$ROOT/scripts/deploy.sh" ]; then
  echo "  deploying Vercel on $COMMIT_SHA …"
  "$ROOT/scripts/deploy.sh"
else
  echo "  VERCEL_TOKEN unset or deploy.sh missing — skip Vercel (commit pushed)"
fi

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Grok Phase-3 CI — SHIPPED                                   │"
echo "├─────────────────────────────────────────────────────────────┤"
echo "│ seal:      $SEAL_LABEL"
echo "│ tag:       $TAG"
echo "│ commit:    $COMMIT_SHA"
echo "│ branch:    main"
echo "│ report:    grok-routing-output/phase3-apply-report.json"
echo "└─────────────────────────────────────────────────────────────┘"