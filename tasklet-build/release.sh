#!/usr/bin/env bash
# RELEASE MODE — full gate pipeline. Run weekly, or before actually sharing the URL widely.
# This is the ONLY path that re-derives clean data from the internal spine and re-seals.
#
#   partition -> enrich -> build -> externalization gate -> land gate -> isolated dist ->
#   deploy -> post-deploy leak sweep -> seal data-clean -> push to main.
#
# Day-to-day, use dev.sh (seconds). Use this when you want the heavy guarantees refreshed.
set -e
cd "$(dirname "$0")"
DIST="../_dist"
DC="../_ingest/data-clean"

echo "=== RELEASE: full gate build ==="
bash build_safe.sh   # partition -> enrich -> build -> ext gate -> land gate -> dist -> deploy

echo "=== post-deploy leak sweep (live URL) ==="
sleep 4
curl -s https://navier-atlas.vercel.app/ -o /tmp/live_release.html
PAT='Sampriti|Bhattacharyya|Founders Fund|Series B|finder|go/no-go|humans\.json|internal_only'
if grep -qiE "$PAT" /tmp/live_release.html; then
  echo "❌ LIVE LEAK DETECTED — investigate before announcing."; exit 1
fi
echo "live sweep clean ($(wc -c </tmp/live_release.html) bytes)"

echo "=== reseal data-clean blobs (extract from shipped index.html, then seal) ==="
uv run python3 extract_blobs.py
python3 seal_bundle.py 2>/dev/null || echo "  (verify SEAL.json manually)"
echo "RELEASE ✅ — gated, swept, sealed. Run the GitHub push to main to finish."
