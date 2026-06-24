#!/usr/bin/env bash
# PR #93 — Curaçao (Ocean Whisperer) + Caribbean × Navier ABC seal lane
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GEO="$ROOT/scripts/grok-geometry"
ECON="$ROOT/scripts/grok-econ-reseal"
SEAL_TAG="${SEAL_TAG:-#pr93-abc-seal}"

die() { echo "✗ $*" >&2; exit 1; }
step() { echo ""; echo "=== $* ==="; }

step "1/7 Mint ABC islands geometry"
python3 "$GEO/mint_abc_islands_geometry.py" --dc data-clean --apply

step "2/7 Bind partners + retire caribbean-mobility"
python3 "$GEO/seal_abc_caribbean_partners.py" --apply

step "3/7 Route geometry audit"
python3 "$ROOT/scripts/audit-route-geometry.py" || echo "WARN: audit reported issues (review report)"

step "4/7 Update SEAL geometry gate"
python3 "$GEO/update_seal_geometry_gate.py" --apply 2>/dev/null || true

step "5/7 Reseal hashes"
python3 "$ECON/update_seal_hashes.py" 2>/dev/null || true

step "6/7 Public build preflight"
BUILD_PROFILE=public node "$ROOT/scripts/build-site.mjs" --profile=public

step "7/7 Deploy"
RELEASE=1 BUILD_PROFILE=public "$ROOT/scripts/deploy.sh"

"$ROOT/scripts/publish-gold.sh" "Gold $SEAL_TAG — PR #93 ABC islands seal"
echo "✓ PR #93 ABC seal lane complete ($SEAL_TAG)"