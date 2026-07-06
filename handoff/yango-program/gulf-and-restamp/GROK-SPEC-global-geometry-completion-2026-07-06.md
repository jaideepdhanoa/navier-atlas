# GROK SPEC — Global Geometry Completion + Gulf Cross-Border (2026-07-06)

**Author:** Tasklet · **Executor:** Grok · **Greenlight:** Jaideep (merge to main + deploy Vercel)
**Operating model:** Tasklet flags/authors + provides deterministic artifacts; Grok applies heavy geometry (cluster_id restamps, marquee rebinds, seal), runs gates, deploys. Null beats confidently-wrong throughout. ID-based matching only.

Artifacts (in `yango-program/gulf-and-restamp/`, commit to repo):
- `GLOBAL-UNSTAMP-RESTAMP.json` — 3,299 route→cluster restamps (deterministic)
- `GULF-AND-GROUPS.json` — Careem Gulf anchors, Eastern Province route ids, cluster renames, market groups

---

## WS-1 — Pass-4 wins + UAE market group (GREENLIT: merge + deploy)
Package the already-applied Pass-4 view-parity changes (rapido 2→9, lyft 34, bolt/uber junk dropped) into a PR, **plus** the UAE market-group fix:
- **UAE market = {`uae`, `uae-east-coast`}.** Apply to ALL five UAE partners (careem, noon, bolt, uber, yango) so all resolve to the identical set. East coast is UAE — it must never be excluded.
- Merge to main → push Vercel prod. Post prod URL + gate receipts + confirm all 5 UAE partners show identical uae + east-coast geometry.

## WS-2 — Maghreb PR #185 merge (GREENLIT)
Merge #185; seal Baku/Aktau + Tunisia + Algeria + Morocco geometry (35 BPs / 23 corridors, hand-waypoints per market). yassir + indrive auto-light Morocco/Algeria/Tunisia on merge. Confirm lit.

## WS-3 — Careem Gulf cross-border (author: Tasklet; seal: Grok)
**Jaideep framing (authoritative):** Careem's *market is UAE only* — SAME scope as Noon: `{uae, uae-east-coast}`. The ONLY difference: Careem additionally **surfaces outbound Q-LR aspirational edges** FROM UAE to Doha / Bahrain / Eastern Province. Mental model: *UAE residents traveling out to other Gulf cities.* Doha / Bahrain / Eastern Province are **NOT Careem markets** — they are only far-endpoint destinations of the outbound edges. Noon surfaces NO Q-LR edges.

1. **Careem scope = `{uae, uae-east-coast}`. Noon scope = `{uae, uae-east-coast}`.** Identical. No foreign clusters added to either.
2. **Q-LR edges are a partner-surfaced aspirational class, NOT auto-inherited operational geometry.** Careem opts in; Noon does not. Do NOT stamp them into the `uae` cluster as ordinary corridors (that would make Noon inherit them under global corridor inheritance). Carry them as a distinct Q-LR/aspirational overlay attached to Careem's view only. Grok picks the mechanism (aspirational edge list / class tag) — the invariant is: **Careem shows them, Noon does not, and they are excluded from operational inherited-corridor gates.**
3. **Re-mint the Q-LR cross-Gulf edges** (0 remain — were dropped). Class = **Q-LR** (amber-dashed, aspirational — NOT operational N30; range concern resolved by class). Origin always UAE. Offshore **hand-waypoints, no land crossing** (route around the Qatar peninsula through open Gulf):
   - Dubai (Al Ghubaiba 55.291/25.265) → Doha/Lusail (51.526/25.422)
   - Abu Dhabi (Irshad 54.359/24.536) → Doha/Lusail
   - Dubai → Bahrain/Manama (50.585/26.248)
   - Abu Dhabi → Bahrain/Manama
   - Dubai → Eastern Province/Dammam (50.202/26.474)
   - (RAK 55.963/25.723 optional origin if geometry clean)
   Anchors in `careem_gulf_anchors`. Do NOT invent BPs beyond these anchors.
4. **Eastern Province cluster stamping is SEPARATE global hygiene (part of WS-4), not Careem scope.** The 49 orphaned Eastern Province routes (`eastern_province_stampable_route_ids`) still get stamped by sovereign — Bahrain-side → `bahrain`; Saudi-side → new `dammam-eastern-province-ksa`; drop 17 junk endpoints (`eastern_province_junk_endpoint_route_ids`). But this lights those clusters for their own partners/geography — it does NOT put them in Careem's scope. Careem only reaches Dammam via the outbound Q-LR edge endpoint.

## WS-4 — Global unstamp restamp (THE BIG ONE — Grok seal pipeline)
**Finding: 3,620 of 4,267 routes (85%) carry `cluster_id=null`** — stamping only ever ran on the ~55 resealed clusters, leaving 85% of global geometry dark for every partner.
- `GLOBAL-UNSTAMP-RESTAMP.json` maps **3,299 (91.1%)** deterministically → 83 clusters (city-member join + spatial anchor <0.6°). Apply via seal pipeline with spatial validation.
- **321 true-null residual held** (calmac→Scotland, geirangerfjord→Norway, ishigaki/iriomote→Okinawa, papeete→French Polynesia, ajaccio→Corsica): genuine `member_city_ids` gaps in CLUSTERS.json. Either add the missing member_city_ids (source-led) then re-stamp, or hold null. **Do not force-bind.**
- After restamp: **rebind marquees** (canonical OD-pair level, bind to sealed `properties.id`), re-run inheritance, refresh partner scopes.

## WS-5 — Split-cluster market groups (canonical; derive post-WS-4)
A market may span >1 cluster. Confirmed seeds (`confirmed_market_groups`): UAE={uae, uae-east-coast}; Qatar={doha-qatar, al-wakrah-qatar} (empty `qatar` shell = alias only). **After WS-4 restamp**, derive the full market-group map (any country with ≥2 route-bearing clusters — e.g. Turkey={turkish-riviera-aegean, istanbul-*}), and add a gate so partner scope resolution always expands a market to its full cluster set. No market silently drops a cluster.

## WS-6 — Cluster renames (partner-prefixed → canonical geography)
Corridors belong to geography, not partners. Restamp route `cluster_id` + rebind marquees + update bolt/yango scope keys:
- `bolt-croatia` (130) → `dalmatia-croatia`
- `bolt-cyprus` (1) → `cyprus`
- `yango-egypt` (50) → `egypt`
- `bolt-italy` (11) → **place by geometry** (Naples/Amalfi vs generic `italy`) — Grok judges from coords; null/hold if ambiguous.

## WS-7 — Over-dense cluster de-spaghetti (UAE first; Tasklet register)
**Root cause (unifies UAE spaghetti + empty-cities):** the reseal stamped only ~55 clusters and never curated them for density, while 85% of routes stayed unstamped/dark (WS-4). So lit clusters over-render (UAE = 115-edge hairball) and everything else shows zero. This is NOT a per-cluster cap — it's per-route stamping that never ran globally + no density curation on the few lit clusters.
- Apply `UAE-DESPAGHETTI-REGISTER.json` to global `ROUTES.json`: **cut 55 of 115** — 25 exact parallel dupes, 1 Musandam land-crosser, collapse the 29-edge Dubai↔Abu Dhabi >40nm fan to **2 canonical marquee corridors**. Keep all genuine distinct intra-city on-water OD pairs.
- **Still open (finer pass):** Dubai intra 51 near-parallel edges need OD-pair-level review (keep distinct Creek/Harbour/Marina/JBR pairs, drop redundant radials). Tasklet authors second register.
- **Starved emirates** (Sharjah 0, Fujairah 0, Umm Al Quwain 0, Ajman 3, RAK 5): source-led intra-city BP pairs. Tasklet flags, Grok sources, nobody invents a pier.
- **After WS-4 restamp, re-run this density scan on every newly-lit over-dense cluster** (Jakarta, Istanbul, etc.) — same cut rules. Tasklet delivers registers per over-dense cluster.

---
## Gates (all must pass before deploy)
- `validate_scope_resolution.py --strict` (careem/noon now resolved — no longer skipped)
- `validate_partner_inheritance.py --strict`
- `validate_finance_inheritance.py`
- No cluster_id=null on stamped markets; residual-null explicitly listed
- `update_seal_hashes.py`
## Order: WS-1 + WS-2 (ship now) → WS-4 (restamp) → WS-5 (groups) → WS-3 + WS-6 (Gulf + renames) → gates → deploy.
