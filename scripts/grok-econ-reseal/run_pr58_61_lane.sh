#!/usr/bin/env bash
# PR #58–#61 — pull-through execution: India/GCC lane + Adani/Reliance seal + economics refresh
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== PR #58 India + GCC execution ==="
"$ROOT/scripts/grok-econ-reseal/run_pr58_india_gcc_lane.sh"

echo "=== PR #61 Adani / Reliance exact-bind ==="
python3 "$ROOT/scripts/grok-econ-reseal/execute_pr61_adani_reliance.py"

echo "=== Finance: India/Noon economics + master tracker ==="
"$ROOT/scripts/grok-econ-reseal/run_india_noon_economics_lane.sh"

echo "=== Re-seal hashes ==="
python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py"

echo "✓ PR #58–#61 lane complete"