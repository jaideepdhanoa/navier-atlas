#!/usr/bin/env bash
# Grok-led journey + featured_route re-link (city-brief-grade binding).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

echo "→ Audit (before)"
python3 "$ROOT/scripts/relink_partner_journeys.py" --audit | tail -5

echo "→ Apply re-link (all partners)"
python3 "$ROOT/scripts/relink_partner_journeys.py" --apply

echo "→ Build smoke (bolt + yango)"
node "$ROOT/scripts/build-site.mjs" 2>&1 | grep -E "bolt|yango|ABORT|FATAL" | head -15

echo "✓ journey relink lane complete"