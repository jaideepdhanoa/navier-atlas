#!/usr/bin/env bash
# Aegean-Med geometry lane — mint inter-city corridors from Tasklet handoff.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
python3 scripts/grok-aegean/route_aegean.py --dc data-clean --out grok-routing-output
echo "→ Aegean routes minted. Run qa_land_crossing + deploy when bundled with partner reseal."