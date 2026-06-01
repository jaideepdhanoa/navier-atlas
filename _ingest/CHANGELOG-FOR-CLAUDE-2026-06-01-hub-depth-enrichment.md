# Changelog for Claude — Hub-Market Depth Enrichment (2026-06-01)

## Why
Jaideep flagged that the meta/platform partners (Uber, Grab, Bolt) had per-market
deep-dives **far shallower** than the single-territory pages (e.g. Dubai-RTA, MPA).
Miami and Hawaii Uber pages were called out specifically — and **Quanta-LR was missing**
from the meta proposals entirely in markets where it's the whole point (inter-island Hawaii,
Miami offshore, etc.).

## What changed
**All 20 hub markets** (Uber 9, Grab 5, Bolt 6) brought up to standalone-page depth.
Every market now carries:
- `partner_context` { their_ambition · their_pressure · where_navier_fits }  ← **NEW, was absent on all 20**
- `why_navier_now` { step_change · no_new_infrastructure · the_moment · wow_corridors }  ← **NEW, was absent on all 20**
- ≥4 `journeys_unlocked` (each market now includes a **Quanta-LR long-range crossing** where geography supports it)
- 4 `proof_points` (was 3 in many)
- 3 `objections` (was 2 in many)
- 3–4 `phases` incl. a dedicated **Quanta-LR long-range phase** (was 2 in many)
- a properly authored 5-key `end_state` (replaced the truncated auto-generated narratives)

`step_change` and `no_new_infrastructure` reuse the canonical platform strings (identical to
the standalone pages); `the_moment` + `wow_corridors` are market-specific.

### Quanta-LR long-range crossings now woven in (highlights)
- **Uber/Miami**: Miami↔Nassau (180nm), Miami↔Key West (120nm) + offshore phase
- **Uber/Hawaii**: Honolulu↔Lahaina, Maui↔Kona, Honolulu↔Kaua'i (inter-island channel crossings — the hero case)
- **Uber/Med**: Mykonos↔Santorini (Cyclades), Split↔Dubrovnik
- **Uber/Italy-luxury & Côte d'Azur**: Amalfi/Riviera ↔ Costa Smeralda (Tyrrhenian crossing)
- **Uber/Brazil**: Rio↔Búzios, Rio↔Ilha Grande
- **Grab/Bali**: the hero chain Bali→Lombok→Komodo→Sumba (Quanta-LR phase 3)
- **Grab/Philippines**: Manila↔Coron/El Nido, Cebu↔Boracay line-hauls
- **Grab/Phuket**: Phuket↔Similan, cross-border reach to Langkawi
- **Bolt/Croatia**: Split↔Dubrovnik; **Bolt/Italy**: Venice↔Dalmatia cross-Adriatic
- **Bolt/UAE**: Dubai↔Abu Dhabi coastal trunk; **Bolt/Saudi**: Jeddah↔Red Sea↔NEOM line-hauls

### route_scope
All new Quanta-LR phases that span ≥2 cities use `route_scope:'all'`; single-city phases stay `'intra'`.

## Files touched
- `partner-pitch/partners/uber.json` (now ~116KB)
- `partner-pitch/partners/grab.json` (now ~80KB)
- `partner-pitch/partners/bolt.json` (now ~78KB)
- `data-clean/partners/*` will be resealed by `seal_bundle.py`
- Stories regenerated (`gen_partner_stories.py`) — hubs project deeper now (markets-aware walk already handled it)

## Validation
- All three hubs validate clean against `partner_proposal.schema.json` (0 errors)
- Leak-gate scan CLEAN on all three (no banned tokens)
- All journey/phase node ids verified against `output/nodes.json`

## Frontend note
No schema-breaking changes — `partner_context` and `why_navier_now` already permitted inside
`markets[]`. The hub deep-dive route (`/uber/{market}`, `/grab/{market}`, `/bolt/{market}`)
should now render these blocks the same way the flat partner pages do. Per-market `end_state`
present on every market (fixes the earlier "5 of 130" TAM line).
