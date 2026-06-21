#!/usr/bin/env bash
# PR #58–#61 — India/GCC + Adani/Reliance + economics + canonical partner-page lane
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== PR #58 India + GCC execution ==="
"$ROOT/scripts/grok-econ-reseal/run_pr58_india_gcc_lane.sh"

echo "=== PR #61 Adani / Reliance exact-bind ==="
python3 "$ROOT/scripts/grok-econ-reseal/execute_pr61_adani_reliance.py"

# Sync India platform + overlay partners to data-clean
for p in rapido ola noon careem adani-ports reliance-industries uber-india-derivative; do
  src="$ROOT/partner-pitch/partners/${p}.json"
  [ -f "$src" ] || src="$ROOT/partner-pitch/partners/_draft/${p}.json"
  if [ -f "$src" ]; then
    cp "$src" "$ROOT/data-clean/partners/${p}.json"
  fi
done

python3 "$ROOT/scripts/grok-econ-reseal/refresh_india_partner_chips.py"

PARTNERS="rapido ola noon careem adani-ports reliance-industries" \
  "$ROOT/scripts/grok-econ-reseal/run_partner_page_lane.sh" --write-tasklet-note

echo "=== Finance: India/Noon economics + master tracker ==="
"$ROOT/scripts/grok-econ-reseal/run_india_noon_economics_lane.sh"

echo "=== Re-seal hashes ==="
python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py"

echo "✓ PR #58–#61 lane complete"