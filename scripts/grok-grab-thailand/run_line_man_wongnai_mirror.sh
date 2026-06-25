#!/usr/bin/env bash
# LINE MAN Wongnai Thailand mirror lane (PR #110 handoff)
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

step() { echo ""; echo "=== $* ==="; }

step "0/6 Ensure handoff doc on branch"
if [ ! -f handoff/GROK-HANDOFF-line-man-wongnai-thailand-mirror-2026-06-25.md ]; then
  git fetch origin tasklet/line-man-wongnai-grok-handoff-2026-06-25 2>/dev/null || true
  git show origin/tasklet/line-man-wongnai-grok-handoff-2026-06-25:handoff/GROK-HANDOFF-line-man-wongnai-thailand-mirror-2026-06-25.md \
    > handoff/GROK-HANDOFF-line-man-wongnai-thailand-mirror-2026-06-25.md 2>/dev/null || true
fi

step "1/6 Mirror partner JSON + crosswalk + finance recal"
python3 scripts/grok-grab-thailand/mirror_line_man_wongnai.py

step "2/6 Update SEAL hashes"
python3 scripts/grok-econ-reseal/update_seal_hashes.py

step "3/6 Partner proposal validation"
python3 scripts/validate_partner_proposals.py 2>&1 | tail -10

step "4/6 Build-site smoke (/line-man-wongnai)"
node scripts/build-site.mjs 2>&1 | grep -E "/line-man-wongnai|failed|ready" || true

step "5/6 Route linkage audit"
node scripts/audit-partner-route-linkage.mjs --strict 2>&1 | tail -8

echo ""
echo "┌─────────────────────────────────────────────────────────────┐"
echo "│ LINE MAN Wongnai mirror lane — receipts in                  │"
echo "│ grok-routing-output/line-man-wongnai-mirror-report.json     │"
echo "└─────────────────────────────────────────────────────────────┘"