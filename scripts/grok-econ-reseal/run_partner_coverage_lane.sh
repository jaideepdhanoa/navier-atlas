#!/usr/bin/env bash
# Full partner coverage lane — class-aware audits + geometry bind waves.
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

PARTNERS="${PARTNERS:-}"
EXTRA=()
if [ -n "$PARTNERS" ]; then
  # shellcheck disable=SC2206
  EXTRA=(--partner $PARTNERS)
fi

echo "=== Wave E: hero narrative patches ==="
python3 scripts/grok-econ-reseal/fill_missing_hero_narratives.py 2>/dev/null || true

echo "=== Wave 3D: hub phase featured promote ==="
python3 scripts/grok-econ-reseal/promote_journeys_to_phase_featured.py \
  grab bolt uber yango gojek line didi indrive freenow cabify lyft \
  kakao-mobility noon careem rapido ola saudi-pif four-seasons

echo "=== Wave 1: inherit + relink (hub/corp only — authorities skip mirror) ==="
if [ -n "$PARTNERS" ]; then
  python3 scripts/grok-econ-reseal/inherit_regional_spine.py --normalize-mirror --bind "${EXTRA[@]}"
  python3 scripts/relink_partner_journeys.py --apply "${EXTRA[@]}"
else
  python3 scripts/grok-econ-reseal/inherit_regional_spine.py --normalize-mirror --bind --all
  python3 scripts/relink_partner_journeys.py --apply
fi

echo "=== Wave 0–2: authority archetype + narratives (after hub inherit) ==="
python3 scripts/grok-econ-reseal/apply_public_transit_authority_phases.py \
  dubai-rta abu-dhabi-itc rakta bahrain-motc qatar singapore-mpa \
  hong-kong transport-nsw thames-clippers nyc-ferry
python3 scripts/grok-econ-reseal/fill_authority_phase_narratives.py

echo "=== Wave 2: authority journey bind ==="
python3 scripts/grok-econ-reseal/upgrade_uae_authority_from_noon.py
python3 scripts/grok-econ-reseal/promote_hk_edge_routes_to_gold.py
python3 scripts/grok-econ-reseal/promote_authority_featured_route_ids.py \
  dubai-rta abu-dhabi-itc qatar
python3 scripts/grok-econ-reseal/bind_authority_journeys_from_phases.py \
  dubai-rta abu-dhabi-itc singapore-mpa hong-kong transport-nsw thames-clippers
python3 scripts/relink_partner_journeys.py --apply --partner \
  dubai-rta abu-dhabi-itc singapore-mpa hong-kong transport-nsw thames-clippers

echo "=== Wave 3: hospitality + ferry flagship bind ==="
python3 scripts/grok-econ-reseal/bind_velana_hospitality_corridors.py
python3 scripts/grok-econ-reseal/bind_hospitality_flagship_corridors.py
python3 scripts/grok-econ-reseal/repair_ferry_flagship_corridors.py \
  norway-fjords fullers360
python3 scripts/relink_partner_journeys.py --apply --partner \
  hong-kong transport-nsw thames-clippers maldives-government
python3 scripts/grok-econ-reseal/repair_ferry_flagship_corridors.py \
  norway-fjords fullers360

echo "=== Wave 3E: economics cascade (registry inherit) ==="
python3 scripts/grok-econ-reseal/wire_economics_cascade_by_route_id.py

echo "=== Wave 7: ferry decontamination + authority featured promote ==="
python3 scripts/grok-econ-reseal/repair_ferry_flagship_corridors.py \
  transport-nsw thames-clippers shun-tak maldives-government
python3 scripts/grok-econ-reseal/promote_authority_featured_route_ids.py \
  dubai-rta abu-dhabi-itc qatar
python3 scripts/grok-econ-reseal/bind_authority_journeys_from_phases.py \
  dubai-rta abu-dhabi-itc transport-nsw thames-clippers shun-tak maldives-government

echo "=== Wave 8: hub market featured relink + India Goa bind ==="
python3 scripts/grok-econ-reseal/relink_hub_market_featured.py \
  gojek line didi lyft kakao-mobility
python3 scripts/grok-econ-reseal/bind_india_goa_hub_journeys.py
python3 scripts/relink_partner_journeys.py --apply --partner \
  gojek line didi lyft kakao-mobility adani-ports reliance-industries

echo "=== Wave 9A: quick geometry wins ==="
python3 scripts/grok-econ-reseal/promote_authority_featured_route_ids.py \
  hong-kong norway-fjords
python3 scripts/grok-econ-reseal/relink_hub_market_featured.py \
  indrive kakao-mobility lyft uber
python3 scripts/grok-econ-reseal/bind_velana_hospitality_corridors.py soneva
python3 scripts/relink_partner_journeys.py --apply --partner \
  indrive kakao-mobility lyft uber hong-kong norway-fjords

echo "=== Wave 9B: North America ferry journey repair ==="
python3 scripts/grok-econ-reseal/repair_ferry_flagship_corridors.py \
  bc-ferries wsf hawaii nyc-ferry norway-fjords
python3 scripts/grok-econ-reseal/bind_authority_journeys_from_phases.py \
  bc-ferries wsf hawaii nyc-ferry norway-fjords hong-kong
python3 scripts/relink_partner_journeys.py --apply --partner \
  bc-ferries wsf hawaii nyc-ferry
python3 scripts/grok-econ-reseal/repair_ferry_flagship_corridors.py norway-fjords
python3 scripts/grok-econ-reseal/promote_authority_featured_route_ids.py \
  hong-kong norway-fjords
python3 scripts/relink_partner_journeys.py --apply --partner hong-kong

echo "=== Wave 9D: narrative + phase stubs ==="
python3 scripts/grok-econ-reseal/fill_hub_phase_narratives.py didi cabify
python3 scripts/grok-econ-reseal/stub_authority_empty_phase_featured.py \
  bahrain-motc nyc-ferry norway-fjords

echo "=== Wave 4: map scope expand ==="
python3 scripts/grok-econ-reseal/expand_partner_map_scope.py

echo "=== Wave 5–6: India corp overlay ==="
python3 scripts/grok-econ-reseal/execute_pr61_adani_reliance.py || true

echo "=== Audits + rollup ==="
python3 scripts/audit_partner_spine_parity.py --all
python3 scripts/audit_partner_page_qa.py
python3 scripts/grok-econ-reseal/audit_partner_coverage_rollup.py

echo "=== Build smoke ==="
node scripts/build-site.mjs 2>&1 | tail -5

echo "=== Done ==="