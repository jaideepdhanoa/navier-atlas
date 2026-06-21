#!/usr/bin/env bash
# RAK corridor lane: Musandam mint, inter-emirate spines, phase fixes, authority twins, re-seal.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
GROK="$ROOT/scripts/grok-econ-reseal"
cd "$ROOT"

echo "=== RAK / UAE corridor lane ==="

echo "  1/7 Mint khasab-oman + Musandam BP registry"
python3 "$GROK/mint_rak_musandam_khasab_geometry.py"

echo "  2/7 Mint RAK↔Abu Dhabi / Sharjah / Fujairah spines"
python3 "$GROK/mint_rak_other_uae_inter_emirate.py"

echo "  3/7 Authority spine expand + seal"
python3 "$GROK/expand_authority_spine_seal.py"

echo "  4/7 Fix RAKTA phase-2 inter-emirate + Quanta-LR display promote (post-expand)"
python3 "$GROK/fix_rak_partner_corridors.py"

echo "  5/7 Partner relink"
python3 "$ROOT/scripts/relink_partner_journeys.py" --apply --partner rakta dubai-rta abu-dhabi-itc

echo "  6/7 Upgrade dubai-rta + abu-dhabi-itc geometry binds (post-relink)"
python3 "$GROK/upgrade_uae_authority_from_noon.py"

echo "  7/8 Apply public_transit_authority phase taxonomy"
python3 "$GROK/apply_public_transit_authority_phases.py"

echo "  8/8 Partner QA spot-check"
python3 "$ROOT/scripts/audit_partner_page_qa.py" --partner rakta dubai-rta abu-dhabi-itc

echo "✓ RAK / UAE corridor lane complete"