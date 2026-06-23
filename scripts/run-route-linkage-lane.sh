#!/usr/bin/env bash
# Route linkage lane — bind featured_routes + journeys, audit, optional geometry check.
#
#   ./scripts/run-route-linkage-lane.sh --partner grab-thailand --apply
#   ./scripts/run-route-linkage-lane.sh --partner bolt yango --dry-run
#   ./scripts/run-route-linkage-lane.sh --apply   # all partners (slow)
#
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

APPLY=0
PARTNERS=()
GLOBAL_AUDIT=0
while [[ $# -gt 0 ]]; do
  case "$1" in
    --apply) APPLY=1; shift ;;
    --dry-run) APPLY=0; shift ;;
    --global-audit) GLOBAL_AUDIT=1; shift ;;
    --partner)
      shift
      while [[ $# -gt 0 && "$1" != --* ]]; do
        PARTNERS+=("$1")
        shift
      done
      ;;
    *) shift ;;
  esac
done

PY_PARTNER=()
if ((${#PARTNERS[@]})); then
  PY_PARTNER=(--partner "${PARTNERS[@]}")
  AUDIT_PARTNER=(--partner "${PARTNERS[@]}")
  FIX_PARTNER=(--apply --partner "${PARTNERS[@]}")
else
  AUDIT_PARTNER=()
  FIX_PARTNER=(--apply)
fi

echo "→ route linkage audit (before)"
node scripts/audit-partner-route-linkage.mjs "${AUDIT_PARTNER[@]}" || true

if ((APPLY)); then
  echo "→ relink_partner_journeys.py --apply"
  python3 scripts/relink_partner_journeys.py --apply "${PY_PARTNER[@]}"

  echo "→ fix_market_route_bindings.py --apply"
  python3 scripts/fix_market_route_bindings.py --apply "${PY_PARTNER[@]}" 2>/dev/null || true

  echo "→ backfill_phase_featured_routes.py --apply"
  python3 scripts/backfill_phase_featured_routes.py --apply "${PY_PARTNER[@]}"

  echo "→ promote_model_link_route_ids.py --apply"
  python3 scripts/promote_model_link_route_ids.py --apply "${PY_PARTNER[@]}"

  if ((${#PARTNERS[@]})); then
    echo "→ mark_unlinked_aspirational.py --apply"
    python3 scripts/mark_unlinked_aspirational.py --apply "${PY_PARTNER[@]}"
  fi

  if ((${#PARTNERS[@]})) && [[ " ${PARTNERS[*]} " == *" minor-hotels "* ]]; then
    echo "→ seed_property_route_linkage.py --apply"
    python3 scripts/grok-minor-hotels/seed_property_route_linkage.py --apply
  fi

  if ((${#PARTNERS[@]})) && [[ " ${PARTNERS[*]} " == *" dubai-rta "* || " ${PARTNERS[*]} " == *" abu-dhabi-itc "* || " ${PARTNERS[*]} " == *" qatar "* ]]; then
    echo "→ promote_authority_featured_route_ids.py"
    python3 scripts/grok-econ-reseal/promote_authority_featured_route_ids.py "${PARTNERS[@]}" 2>/dev/null || true
  fi
else
  echo "→ relink_partner_journeys.py --audit (dry-run)"
  python3 scripts/relink_partner_journeys.py --audit "${PY_PARTNER[@]}"
fi

echo "→ route linkage audit (after)"
STRICT_ARGS=(--strict)
if ((GLOBAL_AUDIT)); then STRICT_ARGS+=(--global); fi
node scripts/audit-partner-route-linkage.mjs "${STRICT_ARGS[@]}" "${AUDIT_PARTNER[@]}"

if ((APPLY)) && ((${#PARTNERS[@]})); then
  echo "→ build-site spot-check"
  BUILD_PROFILE=public node scripts/build-site.mjs --profile=public 2>&1 | grep -E "$(IFS='|'; echo "${PARTNERS[*]}")" || true
fi

echo "✓ route linkage lane complete"