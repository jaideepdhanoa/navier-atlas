# CHANGELOG-FOR-CLAUDE — 2026-06-16 — Wave 6 Africa scrub+enrich (Gold #79w)

**Scope (5 metros):**
- Cape Town / V&A Waterfront / Hout Bay (scrub)
- Zanzibar / Pemba / Mafia / Tanzania (scrub + enrich)
- Mombasa / Diani / Wasini / Kilifi (enrich)
- Madagascar / Nosy Be (greenfield triple-mint, LB-188)
- Mozambique / Vilanculos / Bazaruto (greenfield triple-mint, LB-188)

## Counts delta vs Gold #79v
- POIs: 10,829 → 10,808 (Δ −21; 44 OSM-noise kills minus 23 enrich mints)
- ROUTES: 5,350 → 5,369 (Δ +19)
- CITIES: 171 → 173 (Δ +2: nosy-be-madagascar, vilanculos-bazaruto-mozambique)
- CLUSTERS: 99 → 101 (Δ +2: madagascar, mozambique country clusters)

## Kills (44 BPs, 0 route-orphans)
- Cape Town: 20 OSM-noise kills — "Harbour X" toponym chain (Harbour House / Harbour Arch / Harbour Bay Village / Harbour Park / Harbour Island / Harbour Terrace), residential/cultural overlays, beach-park mis-tags.
- Zanzibar/Pemba/Dar es Salaam: 24 OSM-noise kills — BRT terminal mis-tagged as ferry_terminal (Tanzania bus rapid transit), CHEC "China Harbour Engineering Camp" construction site, Stone Town residential/cultural overlays.

## Enrich (23 BP mints / 19 route mints)
- Mombasa/Diani/Kenya: 8 BPs (Mombasa Old Port Jetty, Likoni KFS, Wasini, Diani Beach jetty, Kilifi Old Town) + 6 south+north coast routes incl. KFS Likoni busiest passenger ferry (~300k pax/yr).
- Zanzibar/Pemba/Mafia: 5 BPs (Pemba Mkoani, Mafia Kilindoni, Nungwi Beach jetty extensions) + 5 routes (Azam Marine mesh; Stone Town↔Mafia 109nm auto-bumped P-II→Q-LR per LB-189-pre).
- Madagascar: 4 BPs (Hellville Port, Nosy Komba, Ankify, Antsiranana) + 3 routes (1 Q-LR ~90nm) + greenfield city `nosy-be-madagascar` + country cluster `madagascar` anchored at Hellville Port.
- Mozambique: 6 BPs (Vilanculos Port, Bazaruto, Benguerra, Pemba MZ, Ibo, Maputo waterfront) + 5 routes (Maputo↔Vilanculos 282nm Q-LR amber-dashed H2-2026+ aspirational) + greenfield city `vilanculos-bazaruto-mozambique` + country cluster `mozambique` anchored at Vilanculos Port.

## LB-174 re-anchors (3)
- kenya → Mombasa Old Port Jetty
- south-africa → V&A Waterfront (bp-41c1d22c88)
- tanzania → Stone Town Ferry Terminal Malindi (bp-882e7de1d0)

## Pre-build gates (LB-175a) — ALL PASS
- ROUTES ≥ floor 5,072 → PASS (5,369)
- New-BP pier-coord verify: 23/23 marine classifier ≥0.5 → PASS
- Pioneer-II 70nm hard cap → PASS (1 auto-bump Stone Town↔Mafia 109nm → Q-LR)
- Q-LR 700nm cap → PASS (max 282nm)
- New-route orphan-endpoint → PASS (0)
- LB-176f kill-BP route-orphan → PASS (0 routes reference any of 44 kills)

## Seal gates — ALL PASS
- gate_endpoint_labels: 0 FLAG
- gate_city_ids: PASS (208 nodes / 5,369 routes / 101 clusters)
- gate_partner_rationale_leak: clean
- gate_osm_noise_bp --global --check-only: PASS (0 safe kills; 33 advisory route-referenced carries unchanged from #79v)
- gate_premint_pair: PASS (0 / 5,369 flagged at threshold 0.5) — 12th consecutive 0-flag at scale

## Carry-forwards (NOT fixed this seal — scheduled follow-ups)
- Dar es Salaam ~6 BPs mis-parented to zanzibar-tanzania (needs dedicated re-parent bite)
- Cape Town missing city feature (V&A coverage exists at BP+cluster level)
- Kizimkazi Harbour (bp-ad6f1f3ff9) likely dup of Kizimkazi South (bp-9545afa402) — needs name+coord confirm

## Learnings captured (see `_scrub-enrich-learnings.md`)
- Cape Town "Harbour X" toponym chain → NOISE_STRONG bigram regex pattern
- Tanzania BRT terminal misclass → NOISE_STRONG
- CHEC "China Harbour Engineering Camp" → NOISE_STRONG
- LB-188 corollary: ferry_terminal "Gateway/Port" suffix BPs pass classifier ≥0.5 first-try without rescue
- **NEW gate proposal:** post-mint haversine recompute + platform-class re-validation pre-stage-write (Stone Town↔Mafia 65→109nm caught + auto-bumped P-II→Q-LR; minted distance_nm cannot be trusted)

## Refs
LB-67 (extract-prior-overlay), LB-104, LB-152, LB-153, LB-171, LB-174, LB-175a, LB-176a-f, LB-179, LB-180, LB-181, LB-183, LB-184, LB-187, LB-188, LB-189, LB-191.
