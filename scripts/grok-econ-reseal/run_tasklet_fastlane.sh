#!/usr/bin/env bash
# Tasklet handoff fastlane — PR #62 India consumer + PR #63 RAKTA/Bahrain MOTC
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "=== Tasklet fastlane (Grok seal + partner page lane) ==="
python3 "$ROOT/scripts/grok-econ-reseal/execute_tasklet_fastlane.py"

echo "=== Re-seal hashes ==="
python3 "$ROOT/scripts/grok-econ-reseal/update_seal_hashes.py" 2>/dev/null || true

echo "✓ Tasklet fastlane complete"