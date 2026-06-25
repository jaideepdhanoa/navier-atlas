# Parked-items follow-up — Tasklet → Grok (2026-06-25)

Completes the three parked buckets called out after the corridor-pin drop. **Tasklet ships research (BPs + geometry hints); Grok validates/snaps/mints + reseals.** Nothing here edits routed geometry.

## 1. `mint_gcn` intra-city loops — second-endpoint BPs
Destinations now have real boarding points (attach to the **existing** city node, no new node needed):
- **Bali** (`bali-indonesia`): Banjar Nyuh Harbour (Nusa Penida, high), Mushroom Bay pontoon (Nusa Lembongan, medium → snap).
- **Phuket/Phang Nga** (`phuket-phang-nga-thailand`): Ao Po Grand Marina (high), Khao Phing Kan / James Bond Island landing (**low** — park landing, no fixed pier; treat aspirational/snap).
- **Bangkok** (`bangkok`): ICONSIAM Pier (high; existing self-loop sightseeing terminal).

## 2. Dubrovnik → Kotor (`mint_rn`)
- **Kotor cruise & ferry port** BP supplied → **new city node `kotor-montenegro`**.
- ⚠️ **CROSS-BORDER** (HR→ME). Supplied so Grok can route the edge, but the cross-border gate is Grok's call — keep aspirational if it fails the exclusion rule.

## 3. East Africa — 8 culled corridors (`EAST-AFRICA-CULLED-CORRIDORS-V2.json`)
Two failure modes from `bolt-east-africa-seal-report.json`:
- **2 BP-missing culls → now unblocked**: `mombasa-malindi-watamu`, `malindi-lamu`. New BPs + city nodes supplied: `malindi-kenya` (high), `watamu-kenya` (medium→snap), `lamu-kenya` (high). **Grok: mint v2 once sealed.**
- **5 land-crossing culls → sea-waypoint HINTS** (single offshore waypoint each to route around land): `stonetown-pemba`, `dar-mafia`, `mombasa-kilifi` (medium confidence, likely real sea ferries); `stonetown-nungwi`, `stonetown-mafia` (low — may stay culled). **Land-crossing gate is Grok's call**; hints are advisory only.
- **1 cross-border → keep culled**: `mombasa-pemba` (KE→TZ), per exclusion rule.

## Files
- `boarding-points/*.json` — 9 BPs across 7 city nodes (6 high · 2 medium · 1 low).
- `inputs/BP-COVERAGE-PARKED-2026-06-25.json` — merged coverage, same schema as the main drop.
- `EAST-AFRICA-CULLED-CORRIDORS-V2.json` — per-corridor v2 recommendation table.

New city nodes for Grok to mint: `kotor-montenegro`, `malindi-kenya`, `watamu-kenya`, `lamu-kenya`.
Confidence flags honest throughout — medium/low BPs are flagged for Grok's snap-to-water step. Null/flag beats confidently-wrong.
