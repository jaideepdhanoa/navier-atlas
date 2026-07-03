# GROK SEAL — Yango coverage-density expansion (2026-07-03)

**From:** Tasklet · **To:** Grok (deterministic geometry + economics lane)
**Partner:** `yango` · **Repo:** `jaideepdhanoa/navier-atlas` · main is source of truth.
**Directive (Jaideep, active):** Coverage *density* — full breadth of regions/clusters/city briefs/BPs/minted
corridors; **no thin or orphan cities**; every touched market at the mature level we see in Grab/Bolt.
**Sub-proposals stay at 8** (do not add pitch pages). NEOM / AMAALA / Red Sea Global are **out of scope**
(sovereign / PIF lane). Tunisia + Rhodes are **not** confirmed Yango markets — held null.

---

## 0. Two-worlds reminder
Tasklet has shipped the **narrative world** in this PR (city/cluster/region briefs + partner JSON). The
**render graph** (BPs → POIs, corridors → routes, partner map scope) is **yours**. This package is your
**input**; seal it onto `data-clean/` and push to main. Do **not** hand a zip back.

---

## 1. What Tasklet already committed in this PR (do not redo)
| Path | Content |
|---|---|
| `data-clean/city_briefs/*.json` | **14 net-new** city briefs at canonical mature schema (see §6) |
| `data-clean/cluster_briefs/*.json` | **7 net-new** cluster briefs |
| `data-clean/region_briefs.json` | **2 enhanced** regions — `caspian`, `africa` (additive; `signature_routes` left null for you) |
| `partner-pitch/partners/yango.json` | +`objections`, +`why_navier_now`, +`coverage_note`, +`_coverage_expansion` manifest |

**Enhance-in-place rule already applied:** existing canonical briefs (Muscat, Cartagena, Manama, Bergen,
Lagos, Doha, Colombo, Fujairah, Salalah, Eastern Province, Helsinki, Stavanger, Geiranger, abidjan, al-wakrah)
were **not** rewritten — they win field-by-field and stay canonical. Those 15 cities are deepened **by
geometry only** (BPs + corridors below), never by brief rewrite.

---

## 2. Your inputs in this package
```
handoff/partner-map-model/yango-coverage-seal/
  GROK-PROMPT.md                      ← this file
  boarding-points/BP-DOSSIER-*.json   ← 6 files · 108 candidate BPs
  corridors/CORRIDOR-DOSSIER-*.json   ← 6 files · 82 candidate corridors (hand-waypoints embedded)
  hand_waypoints/yango_hand_waypoints_*.json  ← 6 files · market-specific [lng,lat] to route around land
  seal-manifest.json                  ← per-cluster BP/corridor/country counts
  BP-COVERAGE-GAP-yango.json          ← coverage audit (0 silent drops contract)
  README.md
```

### BP dossier schema
`{ bp_id, name, city_id, lng, lat, type, coords_confidence }` — `coords_confidence:"approx"` means
gazetteer-snap to the real quay/pier before sealing. `city_id`s are **canonical, ID-reconciled** (e.g.
`al-wakrah`, `abidjan` — no country suffix on those two; all others as-is).

### Corridor dossier schema
`{ route_key:"a|b", a, b, name, descriptor, approx_nm_straight_line, vessel_provisional,
render_provisional, hand_waypoints_needed, hand_waypoints:[[lng,lat]...], regate_on_routed_geometry,
waypoint_guidance }`. `a`/`b` are `bp_id`s from the BP dossiers (Tasklet verified **0 orphan endpoints**).

---

## 3. Your deterministic tasks (in order)
1. **Mint BPs (108).** ID-match each candidate against the existing gazetteer; **dedupe** — the 15 deepened
   cities may already carry POIs (reuse the canonical `bp-…` node, do not double-mint). New waterfronts get
   fresh canonical ids. Snap `approx` coords to the real quay. **0 silent drops** — every candidate BP is
   either sealed or in a drop-ledger with a reason.
2. **Seal corridors (82).** Mint a route per `route_key`; assign `route_id`s. Endpoints join
   `{city_id}__{bp_id}`. Carry `descriptor` onto the route label.
3. **Route around land — market-specific.** For the **65** corridors with `hand_waypoints_needed:true`, fold
   the provided `hand_waypoints` (and `waypoint_guidance`) into the routing/mask gate. These are **market-
   specific** waypoints (Musandam fjord mouths, Ébrié lagoon channels, Gulf-of-Oman headlands, Caspian bays,
   Norwegian fjord arms) — **not** the coarse global land-block. **Acceptance: 0 land crossings post-seal.**
   The 17 open-water-direct corridors have empty `hand_waypoints` by design.
4. **Re-gate distance + vessel.** `approx_nm_straight_line` is straight-line. Where
   `regate_on_routed_geometry:true` (near-boundary legs), recompute nm on the **routed** path and re-pick the
   hull by the range gate (≤70nm → N30 Pioneer II now; 75–150nm → Quanta-LR roadmap; longer → aspirational,
   never faked on a 70nm boat). Update `vessel_provisional` → sealed vessel + `render` (solid vs amber-dashed).
5. **Bind economics.** Run `build_economics_sidecar.py` against the **new Yango gold**; build
   `economics_by_route_id.json`; bind `phase_economics` + the TAM-ladder rungs; wire `economics_url` to the
   partner view + rungs; bind the remaining **null** featured-route/journey `route_id`s; then **remove
   `_growth_case_pending`**.
6. **Expand render scope — post-seal ONLY.** Tasklet intentionally did **not** add the new cities to
   `network_footprint` / `_map_scope` (render-gap trap). After the corridors seal with real geometry, expand
   both rosters to the newly-sealed cities, and populate `caspian` + `africa` region `signature_routes` with
   the new `route_id`s.
7. **Regenerate `data-clean/city_briefs/_index.json`.** It is **stale** — it currently omits bergen-norway,
   helsinki-finland, lagos-nigeria, geiranger-norway, stavanger-norway (and the 14 net-new). Regenerate from
   the on-disk brief set.

---

## 4. Acceptance gate (your QA report must show)
- BP coverage: **0 silent drops**; dedupe count for the 15 deepened cities; zero-POI / ghost-endpoint = 0.
- **0 land-crossings** post hand-waypoint gate — with proof; 0 orphan routes; every sealed BP carries a source id.
- Distance re-gated on routed geometry; vessel per range gate; long legs rendered aspirational, not faked.
- `economics_url` wired; TAM-ladder rungs deep-link to the economics Sheet; `_growth_case_pending` removed.
- `network_footprint` == `_map_scope` == (sealed city set); region `signature_routes` populated.
- Counts: BPs sealed / dropped(+reason), routes built / culled, before→after POI total, land-crossing=0 proof.

---

## 5. Guardrails (permanent)
- **ID-based matching only. Null beats confidently-wrong.** Never invent a `route_id`; a null rung/route is
  correct until sealed.
- Dedupe at seal time (defensive Set dedupe); keep `cluster_id` sync.
- Yango country/region seeds are **additive only** until validated — do not retire existing Yango geometry.
- Do not add pitch/sub-proposal pages (held at 8). Do not touch `archetype` (`ridehail`, held).

---

## 6. Canonical mature schema (for reference — briefs already conform)
- **City brief:** `city_id, display_name, cluster_id, region, tier, posture, summary, waterfront_rationale,
  demand_signals[{archetype,label,note}], use_cases, journeys[{title,today,with_navier,distance}],
  signature_routes, competitive_landscape, seasonality, regulatory_note, precedents, partner_overlays,
  transit_planning`.
- **Cluster brief:** cluster-level equivalent (`cluster_id, display_name, region, tier, summary,
  why_marine_mobility, demand_signals, use_cases, navier_fit, signature_routes, member_cities,
  competitive_landscape, seasonality, regulatory_note, precedents, transit_planning`).

Deliver the QA report to `#tasklet-jaideep`. Merges are Jaideep's call.
