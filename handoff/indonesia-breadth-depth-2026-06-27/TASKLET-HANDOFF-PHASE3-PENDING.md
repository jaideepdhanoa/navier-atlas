# Tasklet handoff — Indonesia breadth & depth (post-merge)

**Merged:** 2026-06-27 · `main` @ `f39c996d`  
**PRs:** #129 (Gojek prose + deck) · #130 (Indonesia 10+10 sub-proposals)  
**Live:** https://navier-atlas.vercel.app (deploy in flight)

---

## What Tasklet shipped (Phase 1 — DONE)

- **Gojek:** 10 Indonesia sub-proposals (jakarta, bali-nusa-gili, lombok, komodo-flores, sumba, riau-singapore, singapore, raja-ampat, likupang, lake-toba) + 60-journey prose depth
- **Grab:** Mirrored 10 Indonesia markets with Grab regional-super-app framing (not Gojek birthplace copy)
- **Footprint:** All 13 Indonesia geos + Singapore on both partners; Derawan added; komodo/riau render bug fixed
- **data-clean + partner-pitch synced** for both partners (render path fix)
- **3 Sabah journeys parked** → `handoff/indonesia-breadth-depth-2026-06-27/_PARKED-sabah-journeys.json`

## Grok owns next (Phase 2 — IN PROGRESS)

See `GROK-SPEC-indonesia-frontier-seal.md`:
- Mint frontier geometry (Raja Ampat, Likupang, Lake Toba flagships; 4 roll-up dots)
- Close seal gaps: Singapore 14, Jakarta 2, Bali 1
- Range-gate, render-QA both maps, economics cascade, handback with SHA/receipt

## Tasklet Phase 3 — WAIT for Grok handback

When Grok returns branch/PR/SHA + route_ids:
1. Bind returned `route_id`s into `data-clean/partners/gojek.json` + `grab.json` (frontier featured_routes + journeys)
2. Run economics cascade → sheet/tracker/sidecar per market
3. Re-run `partner_copy_lint.py` + linkage audit
4. Optional: deck refresh (currently untouched per Jaideep)

## Also merged on main (Grok)

- **P0c partner scope live inheritance** (`scripts/partner-scope.mjs`) — hub maps auto-inherit `CLUSTERS.json` at build; no frozen `_map_scope` staleness

## Build receipts (post-merge)

| Page | Cities | Routes |
|------|--------|--------|
| `/gojek` hub | 18 | 96 |
| `/grab` hub | 41 | 165 |
| `/gojek/raja-ampat` | 1 | 0 (pending seal) |
| `/grab/jakarta` | 13 | 90 |

---

*No Tasklet action until Grok frontier seal handback.*