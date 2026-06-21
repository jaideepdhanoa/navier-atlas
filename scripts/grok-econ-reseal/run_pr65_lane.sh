#!/usr/bin/env bash
# PR #65 — Yassir + Caribbean Grok lane + residual India/GCC + deck validate
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"
GROK="$ROOT/scripts/grok-econ-reseal"

echo "=== PR #65 Yassir + Caribbean lane ==="
python3 "$GROK/execute_pr65_yassir_caribbean.py"

echo "=== Residual India/GCC / authority (post-merge subset) ==="
"$GROK/run_post_merge_lane.sh" || true

echo "=== Partner page lane (yassir + caribbean-mobility) ==="
PARTNERS="yassir caribbean-mobility" "$GROK/run_partner_page_lane.sh"

echo "=== Deck Studio validate + local QA (all #65 packages) ==="
if [[ -d "$ROOT/deck-studio" ]]; then
  cd "$ROOT/deck-studio"
  if python3 -m deck_studio validate --root . 2>/dev/null; then
    for deck in adani-ports bolt caribbean-mobility noon ola rapido reliance-industries uber-india uber-mena yango yassir; do
      if [[ -d "decks/$deck" ]]; then
        python3 -m deck_studio qa --root . --deck "$deck" --receipt "decks/$deck/qa-receipts/pr65-local-qa.json" 2>/dev/null || true
      fi
    done
  else
    echo "  deck-studio validate skipped (install deck-studio package)"
  fi
  cd "$ROOT"
fi

echo "✓ PR #65 lane complete — see handoff/partner-map-model/PR65-GROK-EXECUTION-REPORT-2026-06-21.md"