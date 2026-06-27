# AirAsia MOVE — Tasklet parity validation receipt

_Generated 2026-06-27 · proposal_status: **research-complete / seal-needed** · archetype: **super_app**_

Self-verified, machine-checked. This is the Tasklet-owned half (Gates A/C/C.1/F + copy). Gate B economics and the geometry seal are Grok/model-pass lanes by design.

## Gate A — Market render parity
- Anchor-city crosswalk: `AIRASIA-ANCHOR-CITY-CROSSWALK.json` — **{'OK': 12, 'MINT': 4, 'PARTIAL': 1, 'HELD': 3}**
- Every Phase-1 anchor city_id resolves to a sealed atlas city_id (verified in research pass; zero invention).
- Rosters reconcile: 15 full sub-pages == 15 geometry markets; 3 frontier markets held as roll-ups (honest, not stubs mistaken for parity).

## Gate C — Sub-page parity
- **15 full sub-pages** (multi-market super_app requires per-market pages, not hub-only). Each carries hero/summary/why_now/multimodal_fit/journeys_unlocked/proof_points/objections/phases/the_ask/close/end_state/use_cases.
- Phase-field gaps: **0** (every phase has n/label/boats/cities/route_scope/narrative/featured_routes/vessel/fleet_confidence).
- Roll-up holds: raja-ampat, likupang, lake-toba — explicitly `held` with reason (Indonesia frontier seal, PR #130).

## Gate C.1 — Vessel sizing / range-gating
- `vessel_sizing` block present on every sub-page (3 hull classes + range_gate_note).
- Malaysia-authored legs correctly range-gated: <=70nm Pioneer II; Langkawi<->Phuket 140nm Quanta-LR; Tioman 108.6nm Quanta-LR.
- 5 inherited Indonesia legs carry source-network (Gojek) gating preserved 1:1 for shared-registry consistency; flagged in the Grok spec (re-gate at source if desired, not divergently under AirAsia).

## Gate F — Slide-2 narrative readiness (deck-eligible super_app)
- All 5 source fields present + non-empty: partner_context, hero, why_now, network_thesis, proof_points.
- network_thesis shape OK: headline + body + stats[]{label,value,sub}. proof_points: {claim,evidence,source}[].

## Copy discipline
- Plain-English copy-lint: **0 partner-facing hits** (no 'amber-dashed'/'captive resort mesh'/'scale vision'/'greenfield' in rendered prose; render-directive fields excluded).
- growth_case rung labels are plain English (SOM/SAM/TAM never bare): "Floor today — water transfers on sealed corridors"; "Full network today (+greenfield) — the same model across every sealed gateway"; "Serviceable arriving-seat transfer market across Phase 1 gateways"; "Total airport-to-island transfer spend across the footprint".
- Old partner names (Grab/Gojek) scrubbed from inherited strings; reframed to AirAsia airport-transfer / arriving-seat voice.

## Gate B — Economics (model-pass lane, NOT fabricated)
- `growth_case._status = model-pass-pending`; all numeric bands `null` by design (null beats confidently-wrong).
- TAM anchored on arriving-seat distribution-capture; demand anchors sourced; capture band handed to the model pass (`MODEL-PASS-HANDOFF.md`).

## Footprint counts
| Country | Markets | Journeys | Bound | Needs-mint |
|---|---|---|---|---|
| thailand | 5 | 57 | 57 | 0 |
| indonesia | 5 | 39 | 26 | 13 |
| malaysia | 5 | 14 | 1 | 13 |
| **TOTAL** | **15** | **110** | **84** | **26** |

- Thailand + Indonesia inherit sealed corridors 1:1. Malaysia mint scope = 13 corridors (Tioman's Singapore leg already bound).
- Indonesia's 13 unbound inherit Gojek's own bind state (shared registry); not AirAsia mint scope.

## Honest holds / nulls
- Malaysia 13 corridors: `route_id: null` -> Grok mint (this handoff).
- Koh Lipe endpoint: no Atlas city_id -> Grok mints cross-border endpoint or flags aspirational.
- Indonesia frontier (raja-ampat/likupang/lake-toba): held to PR #130 frontier seal.
- economics_url + numeric bands: null until model pass + sheet build.
- Phase 2 (Philippines + Singapore): out of this build; city briefs exist, seal at Phase 2.