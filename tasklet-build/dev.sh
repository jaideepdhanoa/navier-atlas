#!/usr/bin/env bash
# DEV MODE — fast render iteration (seconds). Use this 95% of the time while building.
#
# Safe by construction: build.py reads ONLY from output-external/ (already-partitioned
# clean data) — it NEVER touches the internal spine. So a render iteration cannot leak
# spine data. The only new leak surface in dev is the partner-facing pitch JSON you author,
# so we do a cheap targeted grep on just those files (milliseconds), and skip the heavy
# pipeline entirely: NO partition, NO full externalization scan, NO seal, NO leak sweep, NO push.
#
# Run release.sh (weekly, or before actually sharing the URL) for the full gate + seal + push.
set -e
cd "$(dirname "$0")"
DIST="../_dist"

echo "1/4 enrich (restore partner_view + vessel_specs into output-external; cheap)..."
python3 partition/enrich_external.py >/dev/null 2>&1 || echo "  (enrich skipped — output-external not yet partitioned; run release.sh once)"

echo "2/4 build index.html (warm route cache → seconds)..."
uv run --with global_land_mask --with numpy python build.py | tail -1

echo "3/4 cheap content check (pitch JSON only — the dev leak surface)..."
bash check_pitch_content.sh

echo "4/4 deploy to navier-atlas.vercel.app..."
mkdir -p "$DIST/.vercel"
find "$DIST" -maxdepth 1 -type f ! -name '.*' -delete
cp index.html "$DIST/index.html"; cp vercel.json "$DIST/vercel.json"
[ -f .vercel/project.json ] && cp .vercel/project.json "$DIST/.vercel/project.json"
if [ -z "$VERCEL_TOKEN" ]; then echo "VERCEL_TOKEN not set — built but not deployed."; exit 0; fi
( cd "$DIST" && npx --yes vercel --prod --yes --token "$VERCEL_TOKEN" )
echo "DEV BUILD ✅ — fast path, no heavy gates (run release.sh weekly)."
