#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== Authority + India follow-up lane ==="
echo "  1/6 authority coverage audit"
python3 "$ROOT/scripts/grok-econ-reseal/audit_authority_coverage.py"

echo "  2/6 expand RAKTA/Bahrain spine featured + re-seal"
python3 "$ROOT/scripts/grok-econ-reseal/expand_authority_spine_seal.py"

echo "  3/6 mint India extension routes"
python3 "$ROOT/scripts/grok-econ-reseal/mint_india_extension_routes.py"

echo "  4/6 bind India extension journeys"
python3 "$ROOT/scripts/grok-econ-reseal/bind_india_extension_journeys.py"

echo "  5/6 wire India KCC economics stubs"
python3 "$ROOT/scripts/grok-econ-reseal/wire_india_kcc_economics.py"

echo "  6/6 partner page lane"
PARTNERS="rakta bahrain-motc rapido ola uber-india-derivative adani-ports reliance-industries uber" \
  "$ROOT/scripts/grok-econ-reseal/run_partner_page_lane.sh"

echo "✓ Follow-up lane complete"