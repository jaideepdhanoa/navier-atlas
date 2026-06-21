#!/usr/bin/env bash
# PR #58 — India + GCC partner proposal deterministic execution lane
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

LANE_TAG="${LANE_TAG:-pr58-india-gcc-execution}"
echo "→ PR #58 India + GCC execution ($LANE_TAG)"

python3 "$ROOT/scripts/grok-econ-reseal/fix_india_route_surface.py"
python3 "$ROOT/scripts/grok-econ-reseal/execute_pr58_india_gcc.py"
python3 "$ROOT/scripts/grok-econ-reseal/refresh_india_partner_chips.py"
python3 "$ROOT/scripts/grok-econ-reseal/upgrade_careem_from_noon.py"

# Sync pitch → data-clean before canonical partner-page lane
for p in rapido ola noon careem uber-india-derivative; do
  src="$ROOT/partner-pitch/partners/${p}.json"
  [ -f "$src" ] || src="$ROOT/partner-pitch/partners/_draft/${p}.json"
  [ -f "$src" ] && cp "$src" "$ROOT/data-clean/partners/${p}.json"
done

PARTNERS="rapido ola noon careem" "$ROOT/scripts/grok-econ-reseal/run_partner_page_lane.sh" --write-tasklet-note

echo "✓ PR #58 India + GCC lane complete: $LANE_TAG"