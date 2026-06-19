#!/usr/bin/env bash
# Grok taxonomy migration — global 4-tier nav (Region → Cluster → City → Locale)
#
# Usage:
#   ./scripts/grok-taxonomy/run_taxonomy.sh
#   TAXONOMY_PUSH=1 ./scripts/grok-taxonomy/run_taxonomy.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-taxonomy"
PHASE3_SCRIPTS="$ROOT/scripts/grok-phase3"
REPO_DC="$ROOT/data-clean"

PUSH="${TAXONOMY_PUSH:-0}"
TAG="${TAXONOMY_TAG:-gold-79ao}"
SEAL_LABEL="${TAXONOMY_SEAL:-#79ao}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

step "1/6 Apply taxonomy migration"
node "$SCRIPTS/apply_taxonomy.mjs"

step "2/6 Taxonomy QA"
python3 - <<'PY' "$REPO_DC"
import json, sys
from pathlib import Path
dc = Path(sys.argv[1])
clusters = json.loads((dc / "CLUSTERS.json").read_text())["clusters"]
fbt = json.loads((dc / "FEATURES_BY_TYPE.json").read_text())
fail = []
if any(c["cluster_id"] == "palm-jumeirah-dubai" for c in clusters):
    fail.append("palm-jumeirah-dubai still a peer cluster")
ctc = {}
for c in clusters:
    if c.get("parent_cluster_id") or c.get("nav_hidden"):
        continue
    for mid in c.get("member_city_ids") or []:
        if "__" not in mid:
            ctc[mid] = c["cluster_id"]
if ctc.get("dubai-uae") != "uae":
    fail.append(f"dubai-uae cluster is {ctc.get('dubai-uae')}, expected uae")
if ctc.get("abu-dhabi-uae") != "uae":
    fail.append(f"abu-dhabi-uae cluster is {ctc.get('abu-dhabi-uae')}, expected uae")
loc = len(fbt.get("locale") or [])
if loc < 100:
    fail.append(f"too few locales: {loc}")
if fail:
    print("TAXONOMY QA FAIL:", fail)
    sys.exit(1)
print(f"TAXONOMY QA PASS: {len(clusters)} clusters, {loc} locales, dubai/abu-dhabi→uae")
PY

step "3/6 Finalize seal $SEAL_LABEL"
python3 "$SCRIPTS/finalize_seal_taxonomy.py" --dc "$REPO_DC" --seal "$SEAL_LABEL"

step "4/6 Postflight (routes unchanged)"
WORK="$ROOT/grok-taxonomy-work"
rm -rf "$WORK"
mkdir -p "$WORK/atlas-repo" "$WORK/partner-pitch/_tools"
cp -R "$REPO_DC" "$WORK/atlas-repo/"
cp "$ROOT/grok-routing-output/uae_gulf_land_v2.wkb" "$WORK/partner-pitch/_tools/uae_gulf_land.wkb" 2>/dev/null || true
QA_SRC="$ROOT/_ingest/grok-phase3-ci-pilot-2026-06-18/partner-pitch/_tools/qa_land_crossing.py"
[ -f "$QA_SRC" ] && cp "$QA_SRC" "$WORK/partner-pitch/_tools/"
export ROUTE_FLOOR=5876
chmod +x "$PHASE3_SCRIPTS/postflight_pilot.sh"
bash "$PHASE3_SCRIPTS/postflight_pilot.sh" "$WORK"

step "5/6 Build"
node "$ROOT/scripts/build.mjs"

CHANGELOG="$REPO_DC/CHANGELOG-FOR-CLAUDE-2026-06-19-taxonomy-79ao.md"
cat > "$CHANGELOG" <<EOF
# CHANGELOG — Gold #79ao — Global taxonomy migration (2026-06-19)

**Base:** #79an (5876 routes)

## Summary
- 4-tier geography: Region → Cluster → City → Locale → Boarding points
- CLUSTERS: 117 → 99 (−18 demoted/duplicate twins)
- FEATURES_BY_TYPE.locale: 0 → 127
- LatAm-Caribbean split → Latin-America + Caribbean
- Sub-clusters: parent_cluster_id (8 nav-hidden) or demoted to locales
- CITY_TO_CLUSTER fix: dubai-uae / abu-dhabi-uae → uae
- 6 UAE locale brief stubs + tier-4 nav in index.html

**Handoff:** grok-routing-output/TAXONOMY-HANDOFF-FOR-TASKLET.md
EOF

if [ "$PUSH" != "1" ]; then
  echo ""
  echo "┌─────────────────────────────────────────────────────────────┐"
  echo "│ Grok taxonomy — DRY RUN COMPLETE                          │"
  echo "├─────────────────────────────────────────────────────────────┤"
  echo "│ seal:      $SEAL_LABEL"
  echo "│ next:      TAXONOMY_PUSH=1 $SCRIPTS/run_taxonomy.sh"
  echo "└─────────────────────────────────────────────────────────────┘"
  exit 0
fi

step "6/6 Commit + push + deploy"
cd "$ROOT"
git add \
  data-clean/CLUSTERS.json \
  data-clean/FEATURES_BY_TYPE.json \
  data-clean/SEAL.json \
  data-clean/city_briefs/dubai-uae__*.json \
  data-clean/city_briefs/abu-dhabi-uae__*.json \
  data-clean/CHANGELOG-FOR-CLAUDE-2026-06-19-taxonomy-79ao.md \
  index.html \
  docs/NOTES-FOR-TASKLET.md \
  scripts/grok-taxonomy/ \
  grok-routing-output/TAXONOMY-HANDOFF-FOR-TASKLET.md \
  grok-routing-output/TAXONOMY-MIGRATION-2026-06-19.json \
  grok-routing-output/QA-TAXONOMY-79ao.md 2>/dev/null || true

git commit -m "$(cat <<EOF
Gold #79ao — global taxonomy: 4-tier nav + 127 locales

- CLUSTERS 117→99: demote UAE sub-clusters to locales, dedupe Caribbean twins
- Split Latin-America / Caribbean; parent_cluster_id on 8 sub-regions
- Emit FEATURES_BY_TYPE.locale; tier-4 nav + locale map layer in index.html
- 6 UAE locale brief stubs; fix CITY_TO_CLUSTER (dubai/abu-dhabi→uae)
- Handoff: grok-routing-output/TAXONOMY-HANDOFF-FOR-TASKLET.md
EOF
)"
git tag -a "$TAG" -m "Gold #79ao — global taxonomy migration (4-tier nav + locales)"
git push origin main
git push origin "$TAG"
if [ -n "${VERCEL_TOKEN:-}" ] && [ -f "$ROOT/scripts/deploy.sh" ]; then
  "$ROOT/scripts/deploy.sh"
fi
echo "SHIPPED: $SEAL_LABEL tag=$TAG"