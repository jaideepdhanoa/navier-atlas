# Gold #47 — Singapore marquee corridors + economics pins/breakdown + city_briefs

**Base:** Gold #46 (extracted full zip, overlay-only per LB-67). **Routes 5258 → 5260.** Economics 78 → 80 resolved / 23 → 21 pending. city_briefs (ship) 164 → 171. **Grab grounded floor UNCHANGED: 128 boats / $38,966,306.** Geometry of all 5,258 prior routes byte-identical; +2 appended.

This export closes the remaining P2/P3 items from your post-#44/#46 punch-list and answers your two open confirmations.

## P2 — Singapore marquee corridors (were 0 routes)
Built **geometry-first** via the LB-59/66 water-solver (real gold POI endpoints; byte-level ROUTES append per LB-56):
- `rn-82453f6cb33e` — **East Coast (Lagoon) → Marina South**, 5.8 nm routed, Pioneer II. Land-gate CLEAR.
- `rn-e94c308a28e3` — **Marina South → Changi Point**, 14.2 nm routed, Pioneer II. Land-gate CLEAR.
- **Deferred (honest):** *Marina → Pulau Ubin direct* — the coarse land-mask cannot thread the Serangoon/Johor Strait at the A* resolution available here. The recreational-cluster intent is met by Marina→Changi (Changi↔Ubin is the existing bumboat hop). Sent to the fine-OSM water-solver queue rather than minting a line that fails the unbuffered-coastline check. Null beats confidently-wrong.

## P2 — economics pin (East Coast → CBD "drop")
**Confirmed:** the prior-export econ drop was an *intentional* defer-until-built — these two corridors were the exact `_pending_route_pin` entries with reason `endpoints_city_level_not_pinned`. Now that the lines exist, both are bound in `finance/model/corridors.json` to the minted `route_id`s + real endpoint nodes (geometry-first) and resolve in the sidecar. Singapore pending cleared. **Floor unchanged** (these are estimated tourism/commuter legs, not grounded-floor corridors).

## P2 — per-boat economics breakdown payload
The modal payload is live. `atom.py` now exposes **additive** `cost_components` (energy / captain / overhead / maintenance) + `revenue_inputs`; `build_economics_sidecar.py` assembles `breakdown:{revenue_build, run_cost, result}` on every record.
- **Cascade safety (LB-51):** additive-only — every existing value and the Grab grounded floor are **byte-identical** after regeneration. Verified.

## P3 — city_briefs (7 added; ship 164 → 171)
`caye-caulker-belize`, `cozumel-mexico`, `playa-del-carmen-mexico`, `floreana-galapagos-ecuador`, `mafia-tanzania`, `cape-cod-islands-usa`, `tioman-island`. Each `signature_routes` entry carries a **geometry-first-resolved gold route_id**; sources are real official orgs (tourism boards / ferry operators / marine parks). **~27 endpoint briefs still owed** → tracked queue, continuing.

## Confirmations (see CONFIRM-FOR-CLAUDE-g47.md at repo root if syncing source)
1. **89 single-token weak matches** — re-ran the #33/#44 `geo_audit_dump.py` on the full #47 surface (113 linked items): 60 OK / 34 weak-single-token / 19 mismatch / 0 dangling. **Committed partners (Grab, Careem, JIH, Saudi/Red Sea) are clean** — the 6 remaining weak binds are legitimate city/island anchor tokens (Dubai, Sharjah, Jeddah, Manama, Gaya) and the 2 JIH "mismatches" are legitimate Velana-airport↔Malé concept labels over correct geometry. **All 17 hard mismatches + 28 weak binds sit in speculative BD-studio dossiers** (aman/hawaii/lyft/uber/line/ola/rapido/kakao/gojek) — label-first fuzzy binds, exactly the class geometry-first now bans. Relink backlog banked.
2. **East Coast → CBD econ drop** — confirmed intentional (defer-until-built); now resolved (above).

## ⚠️ Source/ship brief drift (pre-existing, flagged — not introduced here)
The source tree (`partner-pitch/city_briefs`) carries 2 briefs the shipped gold base did not: `okinawa-yaeyama-japan`, `the-hamptons-east-end-usa`; the zip ships `okinawa-main-japan` (the `_gold37_okinawa_reconcile` naming). Per LB-67 I shipped the authoritative zip base + my reviewed delta and did **not** import un-vetted source drift into gold. These two need geometry-first route resolution before they ship — queued.

## Gates / audit (all green on #47)
`gate_city_ids` PASS (198 nodes, 5260 routes, 75 clusters) · `gate_endpoint_labels` 0 hard flags · `gate_chips` 0 nulled · `gate_route_id` exit 0 · `datastore_audit` **0 fail / 0 warn**.
