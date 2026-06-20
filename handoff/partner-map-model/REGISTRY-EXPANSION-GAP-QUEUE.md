# Registry Expansion Gap Queue

Missing from registry means **not bindable yet** to the canonical Atlas hierarchy. These items become registry expansion/cleanup tasks — never partner-specific fake markets and never silent nulls.

## Summary
- **registry_expansion_needed_unbound_partner_markets**: 0
- **route_categories_not_market_nodes**: 1
- **route_bp_display_cleanup_bound_markets**: 13
- **economics_promotion_tracked_bound_markets**: 80
- **unique_route_cleanup_city_ids**: 14
- **unique_economics_pending_city_ids**: 108

## Binding policy
- Source of truth: existing Atlas `region → cluster → city → locale_type/archetype` hierarchy.
- Proposal display: allowed from canonical city IDs with routed geometry.
- Economics: tracked as promotion metadata; not a display gate.
- Exactness: ID/alias/provenance only; null beats confidently-wrong.

## Registry expansion needed — unbound partner markets
- None from the current partner market table.

## Route categories, not market nodes
- **grab / `cross-border`**: Synthetic cross-border route category; should bind to explicit origin/destination city routes, not become a market node. Next: Model as route/corridor category once endpoint city IDs are explicit.

## Bound markets needing route/BP display cleanup
- **aman / `philippines`**: cleanup `palawan-philippines__el-nido-bacuit-bay`; display-ready now `boracay-philippines, siargao-philippines`.
- **aman / `greece`**: cleanup `skiathos-sporades-greece`; display-ready now `athens-saronic-greece, chios-north-aegean-greece, corfu-ionian-greece, milos-western-cyclades-greece, naxos-greece, paros-greece, santorini-greece, mykonos-greece`.
- **bolt / `greece`**: cleanup `skiathos-sporades-greece`; display-ready now `athens-saronic-greece, chios-north-aegean-greece, corfu-ionian-greece, milos-western-cyclades-greece, naxos-greece, paros-greece, santorini-greece, mykonos-greece`.
- **bolt / `italy`**: cleanup `portofino-cinque-terre-italy, tuscan-archipelago-italy`; display-ready now `amalfi-coast-italy, costa-smeralda-italy, naples-capri-procida-italy, ponza-pontine-italy, sicily-aeolian-italy, venice-italy`.
- **bolt / `portugal`**: cleanup `lisbon-tagus, porto, algarve`; display-ready now `none yet`.
- **didi / `mexico-caribbean`**: cleanup `cozumel-mexico, playa-del-carmen-mexico`; display-ready now `cancun-riviera-maya-mexico`.
- **grab / `philippines`**: cleanup `palawan-philippines__el-nido-bacuit-bay`; display-ready now `boracay-philippines, siargao-philippines`.
- **indrive / `morocco-atlantic`**: cleanup `casablanca, tangier`; display-ready now `agadir-essaouira-morocco`.
- **indrive / `sub-saharan-africa`**: cleanup `abidjan, dar-es-salaam-tanzania, mafia-tanzania`; display-ready now `lagos-nigeria, mombasa-kenya, lamu-kenya, zanzibar-tanzania, pemba-tanzania, cape-town-south-africa`.
- **uber / `mena`**: cleanup `casablanca, tangier`; display-ready now `abu-dhabi-uae, dubai-uae, ras-al-khaimah-uae, sharjah-uae, fujairah-uae, doha-qatar, jeddah-ksa, red-sea-global-ksa, neom-sindalah-ksa, eastern-province-ksa, cairo-egypt, hurghada-el-gouna-egypt, sharm-el-sheikh-egypt, agadir-essaouira-morocco, djerba-tunisia`.
- **uber / `italy-luxury`**: cleanup `portofino-cinque-terre-italy, tuscan-archipelago-italy`; display-ready now `amalfi-coast-italy, costa-smeralda-italy, naples-capri-procida-italy, sicily-aeolian-italy, venice-italy, lake-como-italy`.
- **uber / `mexico`**: cleanup `cozumel-mexico, playa-del-carmen-mexico`; display-ready now `cancun-riviera-maya-mexico, los-cabos-mexico, puerto-vallarta-mexico`.
- **yango / `cote-divoire`**: cleanup `abidjan`; display-ready now `none yet`.

## Economics promotion tracked, not display-gating
- 80 bound partner-market rows include economics-pending city IDs. These can still display where route geometry exists.
