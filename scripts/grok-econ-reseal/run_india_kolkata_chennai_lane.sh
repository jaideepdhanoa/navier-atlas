#!/usr/bin/env bash
# Kolkata/Chennai geometry mint → partner seal → regional inherit → relink → QA → build
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== India Kolkata/Chennai lane ==="
echo "  1/5 mint geometry (cities, BPs, routes, spine)"
python3 "$ROOT/scripts/grok-econ-reseal/mint_india_kolkata_chennai_geometry.py"

echo "  2/5 seal India partners (anchor_cities + route bind)"
python3 "$ROOT/scripts/grok-econ-reseal/seal_india_kolkata_chennai_partners.py"

echo "  3/5 partner page lane (inherit + relink + QA + build)"
PARTNERS="rapido ola uber-india-derivative adani-ports reliance-industries uber" \
  "$ROOT/scripts/grok-econ-reseal/run_partner_page_lane.sh"

echo "✓ India Kolkata/Chennai lane complete"