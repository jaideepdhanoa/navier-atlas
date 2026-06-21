#!/usr/bin/env bash
# PR #58 — India + GCC partner proposal deterministic execution lane
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

LANE_TAG="${LANE_TAG:-pr58-india-gcc-execution}"
echo "→ PR #58 India + GCC execution ($LANE_TAG)"

python3 "$ROOT/scripts/grok-econ-reseal/fix_india_route_surface.py"
python3 "$ROOT/scripts/grok-econ-reseal/execute_pr58_india_gcc.py"
python3 "$ROOT/scripts/relink_partner_journeys.py" --apply --partner rapido ola noon careem
python3 "$ROOT/scripts/grok-econ-reseal/refresh_india_partner_chips.py"
python3 "$ROOT/scripts/grok-econ-reseal/upgrade_careem_from_noon.py"
python3 "$ROOT/scripts/audit_partner_page_qa.py" --partner rapido ola noon careem --write-tasklet-note

echo "→ Partner proposal schema validation (post-lane)"
python3 "$ROOT/scripts/validate_partner_proposals.py"

echo "→ Build-site smoke (post-lane)"
node "$ROOT/scripts/build-site.mjs" 2>&1 | tail -8

echo "✓ PR #58 India + GCC lane complete: $LANE_TAG"