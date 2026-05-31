# Changelog for Claude — Wave 9-B (NET-NEW: Indian Ocean / Mexico Pacific / Brazil / Oceania)

Greenlit net-new white-space scan. **11 new anchor cities created end-to-end**, fully wired across all four layers (same pattern as Wave 9-A Mediterranean). Rebuild + reseal to render.

## Cities (3 new regions)
- **Indian Ocean** (`regions/indian-ocean/`): `mahe-seychelles`, `port-louis-mauritius`
- **Latin America – Pacific/Atlantic** (`regions/latam-pacific/`): `los-cabos-mexico`, `puerto-vallarta-mexico`, `rio-de-janeiro-brazil`, `florianopolis-brazil`
- **Oceania** (`regions/oceania/`): `sydney-australia`, `whitsundays-australia`, `gold-coast-australia`, `auckland-new-zealand`, `bay-of-islands-new-zealand`

## Four-layer wiring (all complete + verified)
1. **Boarding points** — seeded + densified via conveyor. Counts: Rio 139 · Auckland 110 · Gold Coast 102 · Sydney 84 · Florianópolis 64 · Whitsundays 53 · Bay of Islands 47 · Port Louis (Mauritius) 46 · Puerto Vallarta 45 · Los Cabos 42 · Mahé/Seychelles 36 (honest geographic ceiling — Seychelles inner islands; starter floor cleared). Files in `atlas-external/boarding-points/{city_id}.json`.
2. **Anchors** — 11 added to `app/data-spine/manual-coords/city-anchors.json` (now 92 anchors; keyed by city_id = .md stem = BP_CITY_MAP value).
3. **Nodes** — `regions/{indian-ocean|latam-pacific|oceania}/{city_id}.md` stubs. **Verified: all 11 parse via parse_city_files.py — coords resolved, sub-nodes created, zero warnings.**
4. **BP_CITY_MAP** — 11 identity entries added to `build.py` (each resolves to its real node → dangling-join gate passes).
5. **Briefs** — 11 starter-tier briefs in `partner-pitch/city_briefs/` (sealed on next seal). All carry v2 analytical fields + `brief_tier:"starter"`; **0 Pioneer II cap violations; 0 leak hits; valid JSON.**

## Marquee theses
- **Sydney Harbour** (P1) — one of the world's great mass ferry-commute harbours (Circular Quay↔Manly); flagship public-transport upgrade; globally visible.
- **Whitsundays / GBR** (P1) — Australia's premier reef island-hopping market; quiet low-wake foiler is a strong fit for a sensitive marine park.
- **Rio + Costa Verde** (P1) — rare combination: mass Guanabara Bay commute (Rio↔Niterói) + the 360-island Ilha Grande/Angra/Paraty island paradise.
- **Auckland + Hauraki Gulf** (P1) — busy commuter harbour + island-rich gulf (Waiheke corridor); both upgrade and island-hopping in one market.
- **Seychelles** (P1) — flagship Indian Ocean luxury island-hopping; Maldives-like resort-transfer economics.

## Notes
- `display`/`display_name` both carried on all 11 (frontend-safe).
- No cross-cluster corridors declared between Wave 9-B cities yet; intra-cluster mesh auto-forms from dense BPs on rebuild. Candidate trunks for next pass: Mauritius↔Réunion (~115 nm, Quanta-LR), Cabo↔La Paz (~75 nm, Quanta-LR), Auckland↔Bay of Islands (~110 nm, Quanta-LR).
- **Studio manifest** regenerated (now includes all 11; visible in Mobility BD Studio Cities workspace).
