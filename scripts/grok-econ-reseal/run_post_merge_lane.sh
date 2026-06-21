#!/usr/bin/env bash
# Canonical post-Tasklet / post-Grok merge lane — makes inheritance + seal + finance automatic.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
GROK="$ROOT/scripts/grok-econ-reseal"

echo "=== Post-merge lane (automatic inheritance + seal + finance) ==="

echo "  1/9 RAK spine city-ID contamination fix"
python3 "$GROK/fix_rak_spine_city_contamination.py"

echo "  2/9 India geometry (if handoff present)"
if [[ -f "$ROOT/handoff/partner-map-model/india-adani-reliance-high-value-consumer-market-scan-kolkata-chennai-2026-06-21.json" ]]; then
  if ! [[ -f "$ROOT/handoff/partner-map-model/india-kolkata-chennai-mint-report.json" ]]; then
    "$GROK/run_india_kolkata_chennai_lane.sh"
  else
    echo "    skip — mint report exists"
  fi
fi

echo "  3/9 India extension routes + bind"
python3 "$GROK/mint_india_extension_routes.py" 2>/dev/null || true
python3 "$GROK/bind_india_extension_journeys.py" 2>/dev/null || true

echo "  4/9 Authority spine expand + seal (all domestic)"
python3 "$GROK/expand_authority_spine_seal.py"

echo "  5/9 Regional inheritance bind — ALL packs"
python3 "$GROK/inherit_regional_spine.py" --bind --all

echo "  6/9 Partner page lane (parity, relink, QA, build, tracker)"
"$GROK/run_partner_page_lane.sh"

echo "  7/9 Authority finance cascade"
"$GROK/run_authority_finance_lane.sh"

echo "  8/9 India KCC finance cascade"
"$GROK/run_india_authority_finance_lane.sh"

echo "  9/9 Coverage audit"
python3 "$GROK/audit_authority_coverage.py"

echo "✓ Post-merge lane complete — see handoff/partner-map-model/regional-inheritance-auto-lanes.json"