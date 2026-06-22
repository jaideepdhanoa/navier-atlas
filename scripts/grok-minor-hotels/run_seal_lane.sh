#!/usr/bin/env bash
# Minor Hotels deterministic seal lane (Phase 1)
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
SCRIPTS="$ROOT/scripts/grok-minor-hotels"

step() { echo ""; echo "=== $* ==="; }

step "1/3 Seal Minor Hotels (binds, POIs, crosswalk, country-reference, QA G1–G8)"
python3 "$SCRIPTS/seal_minor_hotels.py" --apply

step "2/4 Ground Palm Jumeirah crescent BPs (gazetteer snap → solid render)"
python3 "$SCRIPTS/ground_palm_crescent.py" --apply

step "3/4 Build scoped captive corridors view"
python3 "$SCRIPTS/build_corridors_minor_hotels.py"

step "4/4 Validate partner JSON"
python3 "$ROOT/scripts/validate_partner_proposals.py" 2>&1 | tail -8

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ Minor Hotels seal lane — COMPLETE                             │"
echo "│ crosswalk: grok-routing-output/MINOR-ANCHOR-CITY-CROSSWALK  │"
echo "│ report:    grok-routing-output/minor-hotels-seal-report.json│"
echo "│ corridors: finance/recal/corridors-minor-hotels.json        │"
echo "└─────────────────────────────────────────────────────────────┘"