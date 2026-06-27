# Indonesia Breadth & Depth — Gojek + Grab build sequence

**Goal (Jaideep, 2026-06-27):** complete Indonesia *map representation* (all geos inherited) +
8–10 *complete* example sub-proposals (no stubs) on Gojek, **mirrored to Grab**. Deck untouched for now.

---

## 1. What the Atlas already holds (grounded)

The Indonesia cluster has **13 member geos, all with city briefs present** (`members_present: 13,
members_missing: []`). Singapore + cross-border ride alongside as the SG-anchored network.

| # | Geo | Modeled? | Sealed corridors / route_ids | Decision |
|---|-----|----------|------------------------------|----------|
| 1 | **Bali, Nusa & Gili** | ✅ bali bucket | 9/10 route_ids + economics | **Full sub-proposal** |
| 2 | **Lombok** | ✅ bali bucket | sealed | **Full sub-proposal** |
| 3 | **Komodo & Flores (Labuan Bajo)** | ✅ bali bucket | sealed | **Full sub-proposal** |
| 4 | **Sumba (Nihi)** | ✅ bali bucket | sealed | **Full sub-proposal** |
| 5 | **Jakarta & Thousand Islands** | ✅ jakarta bucket | 3/5 route_ids | **Full sub-proposal** |
| 6 | **Bintan & Riau ↔ Singapore** | ✅ cross-border+SG | 3/4 route_ids | **Full sub-proposal** |
| 7 | **Singapore** | ✅ singapore bucket | ⚠️ only 2/16 route_ids | **Full sub-proposal** + Grok closes 14-corridor seal gap |
| 8 | **Raja Ampat** | ❌ frontier | none (prose-only routes) | **Full sub-proposal, pending Grok seal** |
| 9 | **Likupang & Bunaken (N. Sulawesi)** | ❌ frontier | none | **Full sub-proposal, pending Grok seal** |
| 10 | **Lake Toba (Samosir)** | ❌ frontier | none | **Full sub-proposal, pending Grok seal** |
| 11 | Karimunjawa | ❌ frontier | none | Footprint dot + roll-up |
| 12 | Banda Islands (Maluku) | ❌ frontier | none | Footprint dot + roll-up |
| 13 | Derawan (E. Kalimantan) | ❌ frontier | none · **missing from Grab** | Footprint dot + roll-up (add to both) |
| 14 | Wakatobi (SE Sulawesi) | ❌ frontier | none | Footprint dot + roll-up |

**Curated example pick = 10 full sub-proposals** (incl. all 5 Jaideep named) + **4 footprint/roll-up** dots →
**every one of the 13+SG renders on the map** (complete representation), with depth concentrated where value is highest.

Full grounded table: `INDONESIA-COVERAGE-CLASSIFICATION.json`.

---

## 2. Why this isn't "from scratch" — and what we reuse

- **Grab already carries the structured Indonesia footprint** (12 geos as rich `network_footprint[]`
  objects: registry_key, label, evidence_tier `country_supported`, promotion_lane, `render: geometry`,
  `map_promote: true`) from Grok's `apply_partner_8020_inheritance_bindings`. **Gojek's footprint is a
  primitive flat string list** — we upgrade it to Grab's schema.
- **Grab's `bali` + `cross-border` market objects are the sub-proposal template** (~19–21 fields:
  summary, hero, why_now, multimodal_fit, journeys_unlocked, proof_points, objections, phases, close,
  end_state, partner_context, why_navier_now, corridors_note). We replicate + re-voice for Gojek.
- **City briefs are the narrative source** for every geo (rich, sourced, 5–10KB each), incl. frontier.
- **Cluster brief** (`indonesia.json`) supplies the network-level thesis + real signature route_ids.

---

## 3. Build sequence (who does what, in order)

### Phase 1 — Tasklet (now, no code/seal)
1. **Footprint parity:** rebuild Gojek `network_footprint[]` → Grab's structured-object schema; include all
   13 Indonesia geos + Singapore + cross-border, with registry_key, label, country, evidence_tier,
   promotion_lane, `render: geometry`, `map_promote: true`.
2. **Author 10 full sub-proposals** into `gojek.json` at Grab parity (all ~22 fields + `phases`
   Prove→Scale→Mature). Modeled 7 bind real `*_node_id`/`route_id`; frontier 3 author complete prose +
   phases with **`route_id: null` pending seal** (null beats fabricated — not a stub).
3. **Mirror to Grab** `grab.json`: enrich existing `bali`/`cross-border`; add new Indonesia sub-proposals
   for the shared curated set; **add Derawan** (currently absent) to footprint.
4. **Anchor-city crosswalk** (parity Gate A) for every new/edited market — id → atlas `city_id` verdicts.
5. **Roll-up entries** for the 4 footprint-only geos (id/label/region/one_liner/status — explicitly dots,
   not full pages).
6. Plain-English copy throughout; no internal taxonomy in any rendered field.

### Phase 2 — Grok (deterministic handoff)
1. **Mint frontier geometry** for the 7 frontier geos using city-brief `signature_routes` prose as spec:
   boarding points + corridors + `route_id`s + line geometry. Priority: the 3 frontier **full
   sub-proposals** (Raja Ampat, Likupang, Lake Toba) get their featured corridors minted first; the 4
   roll-up geos get ≥1 node + 1–2 representative corridors so dot+line render.
2. **Close existing seal gaps:** Singapore (14 corridors w/o route_id), Jakarta (2), Bali (1), cross-border (1).
3. **Add Derawan** binding to Grab + Gojek footprint with sealed node.
4. **Economics:** run `aggregate.py → growth.py → splice_growth_into_partner.py` over the newly-corridored
   markets; produce per-market economics + `*-aggregate.json`.
5. **Range-gate** every minted corridor by hull (≤70nm N30/Pioneer II, 75–150 Quanta-LR, >150 review).
6. **Render QA:** confirm all 13+SG render on **both** Gojek and Grab maps (anchor-city ID match), corridors
   where minted; run `partner_copy_lint.py` + land-crossing gate.
7. **Reseal + commit;** hand back with **branch, PR link, commit SHA, exact files changed, validation
   receipt, and explicit nulls/held geos**.

### Phase 3 — Tasklet (after Grok handback)
1. **Bind** the returned `route_id`s into the 3 frontier sub-proposals' `featured_routes` (replace null).
2. **Cascade economics** → transparent sheet (in place, preserve URL) + master tracker + economics sidecar.
3. **Parity QA** Gates A–F on both partners; magnitudes sanity-check.
4. Open the partner-facing PR for Jaideep's copy review (merge is Jaideep's call).

---

## 4. Handoff artifacts to produce for Grok
- `GROK-SPEC-indonesia-frontier-seal.md` — per-geo mint list (BPs, corridors, hull, demand anchors).
- Updated `gojek.json` + `grab.json` with null-route frontier sub-proposals (the bind targets).
- `gojek-ANCHOR-CITY-CROSSWALK.json` + `grab-ANCHOR-CITY-CROSSWALK.json`.
- `INDONESIA-COVERAGE-CLASSIFICATION.json` (this pass's ground truth).

## 5. Open decision for Jaideep
The **10-pick** above is my read of "top 8–10 high-potential incl. Singapore, Bintan x-border, Bali,
Jakarta, Lombok + a few more." Swap candidates if you'd rather promote a frontier flagship (e.g. Wakatobi)
into the full-proposal set or drop one of the 3 pending-seal frontier proposals to keep depth tighter.
