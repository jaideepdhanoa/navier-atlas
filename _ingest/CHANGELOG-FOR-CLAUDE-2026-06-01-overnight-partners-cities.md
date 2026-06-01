# Changelog for Claude — 2026-06-01 overnight run (partners + new cities)

This run added 9 partner proposals, 12 net-new city nodes, and resolved both items you logged. Everything is data-layer only — no frontend changes required beyond routing the new partner/city slugs (your existing hub/spoke + flat patterns already cover them).

## 1. New partner proposals (9 → roster now 19, all schema-valid)

**Hubs (layout:"hub", markets[]):**
- `bolt` — European demand platform hub. 6 markets: Greece (`greece`), Croatia (`croatia`), Italy (`italy`), France-Riviera (`france-riviera`), UAE (`uae`), Saudi (`saudi`). `recommended_entry` set. Route them like uber/grab: `/bolt` index + `/bolt/{market}`.

**Flat single-territory (no markets[]):**
- `maldives` — standalone flagship island-hopping page (the $100M / ~100-vessel public deal as the live proof case). NOTE: the old curated `maldives-hospitality` supplemental story is **retired** — Maldives is now a projected story from the partner page (single source of truth).
- `cote-dazur` — French Riviera (Monaco/Nice/Cannes/St-Tropez/Îles de Lérins).
- `hong-kong` — Shun Tak/TurboJET framing; HK↔Macau↔PRD crossing modernization.
- `norway-fjords` — Bergen/Geiranger/Stavanger fjord network.
- `indian-ocean-luxury` — Seychelles + Mauritius + Zanzibar luxury transfer network.
- `transport-nsw` — Sydney Harbour + Parramatta River zero-emission ferry.
- `d-marin` — pan-Mediterranean marina/berthing network (Croatia/Greece/Turkey/Montenegro/UAE) as a charging-and-demand backbone.
- `fullers360` — Auckland / Hauraki Gulf zero-emission ferry.

Stories regenerated: **15 projected supplemental** (+ hand-authored base stories for grab/careem/mpa/rsg unchanged).

## 2. RESOLVED — your two logged items

### (a) Per-market `end_state` authored (your "5 of 130" TAM fallback)
Added an authored `end_state` to **every market** in the hub partners (uber 9, grab 5, bolt 6 = **20 markets**). Each carries `headline`, `addressable_market_count` (= count of that market's lit end_state_cities), `addressable_footprint`, `end_state_cities`, `narrative`. The deep-dive "The network" TAM line can now read the per-market `end_state` instead of falling back to a derived count. `markets[].end_state` is a free-form object (schema allows additional props on market items).

### (b) `sumba-indonesia` node — BUILT
Full 5-layer wiring: `.md` stub (`world-map/regions/sea/sumba-indonesia.md`), anchor (`city-anchors.json`, coords `[119.32,-9.62]`), 14 BPs (`boarding-points/sumba-indonesia.json`), starter brief (`city_briefs/sumba-indonesia.json`), and `BP_CITY_MAP` entry in `build.py`. It is the terminus of the Bali→Lombok→Komodo→Sumba hero chain (NIHI Sumba anchor). Previously only existed as sub-pins inside `komodo-flores-indonesia` and `bali-indonesia`.

## 3. Net-new city nodes (12 total incl. Sumba) — all 5 layers wired
`seattle-puget-sound-usa`, `new-york-harbor-usa`, `boston-new-england-usa`, `vancouver-canada`, `mumbai-india`, `goa-india`, `kerala-backwaters-india`, `zanzibar-tanzania`, `cape-town-south-africa`, `lake-como-italy`, `lake-geneva-switzerland`, `sumba-indonesia`.

- ~1,275 new boarding points densified (Seattle 149, NYC 121, Boston 150, Vancouver 150, Mumbai 102, Goa 109, Kerala 150, Zanzibar 47, Cape Town 73, Como 109, Geneva 101, Sumba 14).
- Each has: `.md` node stub, `city-anchors.json` anchor, densified BPs, starter `city_briefs/*.json`, `BP_CITY_MAP` entry.
- NYC and Boston/New England are **separate** nodes (not combined).
- India coastal cities = **South Asia** region (consistent with Colombo/Maldives convention).
- Africa coast (`zanzibar-tanzania`, `cape-town-south-africa`) → new `world-map/regions/africa/` folder.

## 4. SCHEMA CHANGE — Africa region enum
Added `"Africa"` to the `region` enum in `partner-pitch/schema/city_brief.schema.json` (needed for Zanzibar + Cape Town briefs). The data-spine region map already resolves `africa` folder → "Africa". No frontend change needed beyond accepting the new region facet in any region filter UI.

## 5. Build state
Anchors now **116**. Pipeline re-run + reseal performed this session (see latest export zip + SEAL.json). All partner JSON validate against `partner_proposal.schema.json`; all new briefs validate against `city_brief.schema.json`.
