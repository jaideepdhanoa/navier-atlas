#!/usr/bin/env bash
# Promote sealed pilot work-tree blobs into repo data-clean/.
set -euo pipefail

WORK="${1:?work root}"
REPO_DC="${2:?repo data-clean path}"

SRC="$WORK/atlas-repo/data-clean"

for f in ROUTES.json FEATURES_BY_TYPE.json SEAL.json \
         qa_baseline.json SEAL.prior.json route_water_allowlist.json \
         qa_land_crossing_report.json; do
  if [ -f "$SRC/$f" ]; then
    cp "$SRC/$f" "$REPO_DC/$f"
    echo "  synced $f"
  fi
done

if [ -f "$WORK/grok-routing-output/phase3-apply-report.json" ]; then
  cp "$WORK/grok-routing-output/phase3-apply-report.json" \
     "$(dirname "$REPO_DC")/grok-routing-output/phase3-apply-report.json" 2>/dev/null || true
fi

CHANGELOG="$REPO_DC/CHANGELOG-FOR-CLAUDE-2026-06-18-uae-phase3-79al.md"
if [ ! -f "$CHANGELOG" ]; then
  cat > "$CHANGELOG" <<EOF
# CHANGELOG — Gold #79al — Grok Phase 3 UAE geometry pilot (2026-06-18)

**Base:** #79ak (5411 routes, pilot substrate)  
**Method:** Grok CI — APPLY-LEDGER.json → apply → LB-224 v2 postflight → reseal

## Applied
- 10 synthesize routes (8 clean + 2 Khalifa-after-mint)
- 14 resolve/rn/ics geometry patches
- 1 BP mint: Khalifa Port (working_harbour, hide)
- 3 synthesize rows HELD (Lulu/Reem phantom — see NOTE-FOR-TASKLET-LULU-REEM-REMINT.md)

## Gates
- LB-224 two-tier land-crossing (v2 WKB overlay precedence)
- route_water_allowlist.json subtract
EOF
  echo "  wrote $CHANGELOG"
fi