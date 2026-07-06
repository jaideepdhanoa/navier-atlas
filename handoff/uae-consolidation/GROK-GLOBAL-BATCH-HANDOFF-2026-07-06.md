# Grok Global Batch Handoff — Corridor Inheritance rollout (ALL markets, one lane)

**Date:** 2026-07-06 · **From:** Tasklet · **To:** Grok · **Re:** follow-on to PR #188 UAE lane (complete on `main`)

---

## TL;DR

UAE proved the pattern end-to-end (140 routes · 0 land flags · 3 gates green · finance spine identity). **Do not roll out market-by-market.** Run the *same* lane across **all 116 contested clusters in one orchestrated batch**. Total remaining work = **two Tasklet↔Grok passes**, then the atlas is inheritance-clean everywhere.

This corrects an earlier drift toward sequential per-market cycles. Our locked rule stands: **no market-by-market cycles.**

---

## Scope (the real number — not 5 markets)

From `CROSS-PARTNER-INHERITANCE-AUDIT.json`:

| Metric | Value |
|---|---|
| Commercial partners analysed | 21 |
| Clusters referenced across scopes | 275 |
| **Clusters shared by 2+ partners (contested)** | **116** |
| Clusters shared by 4+ partners (reseal first) | 17 |
| Hand-curated corridor entries to collapse | 2,039 |

**The 17 four-plus clusters (reseal first)** — ordered list in `CONTENTION-ORDER.json`:
- **14 × Thailand** (bangkok, cha-am, hua-hin, koh-chang, koh-lanta, koh-larn, koh-phangan, koh-phi-phi, koh-samet, koh-samui, koh-tao, krabi, pattaya, phuket-phang-nga) — each shared by all 6 SEA super-apps (airasia-move, bolt, grab, grab-thailand, line, line-man-wongnai)
- **cartagena-colombia** (cabify, didi, uber, yango)
- **chennai-ecr-cuddalore-puducherry-coast** (ola, rapido, uber, uber-india)
- **kolkata-hooghly-waterfront** (ola, rapido, uber, uber-india)

Then the remaining 99 two-plus clusters in the same batch.

---

## Cadence — 3 passes total (locked)

| Pass | Owner | Work |
|---|---|---|
| **1** | **Grok** | Global geometry reseal + inheritance derivation for all 116 clusters, one run |
| **2** | **Tasklet** | Global marquee re-curation vs sealed geometry (route_ids bind directly) |
| **3** | **Grok** | Apply marquees to partner featured/wow + finance cascade + derive + seal + deploy |

---

## Pass 1 — Grok global reseal (detailed)

1. **Parametrize** `seal_uae_corridor_consolidation.py` over **every cluster** (cluster loop; remove UAE hardcoding). Per cluster: drop dirty BPs, de-mesh over-connected hubs, waypoint-route survivors, stamp `cluster_id`, **0 land-flag acceptance gate**, dedupe at seal time.
2. **Run the 3 gates globally** — `validate_partner_inheritance.py` + `validate_finance_inheritance.py` (already wired for UAE; run for all 116).
3. **Finance spine:** generalize `unify_uae_finance_spine.py` — one shared `route_id` spine per **multi-partner geography**; preserve per-partner overlay only (`L3_locals`, `capture_rate`, `archetype`, `fleet_basis`).
4. **Derive partner scopes:** `partner_corridors = global_canonical ∩ partner.clusters`; strip all hand-curated per-partner corridor arrays.
5. **Emit a slim sealed-corridor manifest per market** → `grok-routing-output/sealed-corridors/{cluster_id}.json` with `{route_id, from, to, from_city_id, to_city_id, distance_nm, cluster_id, _geometry_land_km, from_label, to_label, traffic_weight, trip_scope}`. **This is Tasklet's Pass-2 curation input** — avoids shipping the 21 MB `ROUTES.json` around.

---

## Pass 2 — Tasklet global marquee curation (my lane — no Grok action)

`gen_canonical_marquees.py` **v2.2** (attached, updated this pass) runs against sealed geometry and outputs:
- `CANONICAL-MARQUEES.json` — per **`cluster_id::city_id`** group: `marquee_wow` (≤5) + `marquee_featured` (≤8)
- `MARQUEE-RETIRE-LIST.json`, `LABEL-SCRUB.json`, `SUSPECT-ENDPOINTS.json`

**Route_ids bind DIRECTLY** from sealed `properties.id` (e.g. `rn-b7ac6238165d`) — **no re-stamp step for Grok.** This is the single biggest efficiency: curating *after* reseal means the OD-pairs already carry their sealed route_ids.

---

## Pass 3 — Grok apply

- `apply_canonical_marquees.py`: partner `featured_routes`/`wow_corridors` = **union of the city sets for the partner's clusters**; route_id already real; apply `LABEL-SCRUB.json` to the *source* BP labels in `data-clean`; archive retired to `handoff/archive/`.
- Finance cascade → derive → seal → deploy.

---

## Process lessons (apply to EVERY market — these are why UAE went clean)

1. **Curate marquees AFTER reseal, never before.** v2.1 was curated pre-reseal → **0 of 52** OD-pairs survived the geometry change. v2.2 curated post-reseal → route_ids bind directly. Sequencing is not optional.
2. **Composite `(cluster_id, city_id)` grouping.** Shared city_ids (e.g. `sharjah-uae` spans both the Gulf coast *and* east-coast enclaves) will cross-contaminate a plain city_id grouping. Cluster-scoping the city sub-set fixes it and stays city-level.
3. **Reseal fixes geometry, not locale hygiene.** Post-reseal markets still carry **mis-tagged city_ids** and **mis-geocoded business-POI endpoints**. These are a locale-cleanup item (#119 lane), *not* marquee bugs:
   - `SUSPECT-ENDPOINTS.json` — **41 flagged globally** (watersports clubs, boatyards, seaplane bases, slipways, LLC business POIs, "…for construction"). Fix or drop the source BP; **do not invent a pier**.
   - **city_id mis-tags** — e.g. UAE `RAK[uae]` still shows Dubai pairs ("Marina Promenade", "Marasi Bay") mis-tagged `ras-al-khaimah-uae`. Reconcile the source `from_city_id`/`to_city_id`. **null beats wrong.**

---

## BP-hygiene precondition (`BP-CLEANUP-REGISTER.json` — NEW, attached)

The UAE reseal fixed geometry but left dirty boarding points behind. Rather than keep discovering these one-off through marquee curation, I ran a **global BP-hygiene scan** over every BP that participates in a corridor (sealed `ROUTES.json`, **4,038 BPs**). Grok consumes this register **during Pass 1** — cleaning the BP *before* it meshes, not after. Deterministic dispositions only; **Tasklet flags, Grok applies, nobody invents a pier**:

| Disposition | Count | Meaning | Grok action |
|---|---|---|---|
| `DROP_junk` | 43 | Not a passenger pier (seaplane bases, watersports clubs, boatyards, LLC offices, "…construction", medical) | Drop BP + its corridors |
| `RETAG_city_mismatch` | 209 | BP coordinate >60 km from assigned city centroid **and** ≥2× closer to another city's | Retag `city_id` to `nearest` (register gives the candidate + km proof) |
| `DUP_coord` | 154 | Same rounded coordinate, different labels — geocode collision | Merge/repoint (register lists the colliding BP ids) |
| `RELABEL_aggregate` | 1 | Aggregate territory label as single endpoint | Trim to primary place (`suggest` field) |

Spread is **global, not UAE-specific**: Thailand 35 · Indonesia 29 · Egypt 28 · Qatar 21 · UAE 19 · USA 12 · Turkey 12 · CalMac 11 … Worst offenders: *Salalah tagged `muscat-oman`* (874 km off), *Hua Hin tagged `krabi-thailand`* (536 km), the entire *Turkish Aegean (Bodrum/Antalya/Kos) mis-tagged `istanbul-turkey`*.

**This is the corridor-participating subset of the #119 mis-geocode debt** (1,297 total true mis-geocodes) — the highest-priority slice because these BPs actually render on the map. Fold the register into the reseal's dirty-BP drop step per cluster. `RETAG_city_mismatch` gives a candidate but **retag only where the register's `nearest` is unambiguous**; anything doubtful → leave assigned + flag, null beats wrong. Regenerate the register after reseal to confirm 0 residual.

---

## Per-market geometry fragments (embedded — not sequential merges)

- **Hand-waypoints:** `data-clean/uae_hand_waypoints.json` + all `data-clean/pta_hand_waypoints_*.json` (Bangkok Chao Phraya, Singapore MPA, Hong Kong, Istanbul, Venice, etc.). Load per market.
- **Bangkok Chao Phraya river exception:** `RIVER_CITIES` floor **0.4 nm** (iconic express-boat hops < 3 nm are legit). Channel-route the river land false-positives; do **not** feature land-flagged river hops.
- **Legit cross-border long routes** (do NOT cull as over-range): Singapore ↔ Batam/Bintan/Riau; UAE east-coast ↔ Musandam (`bp-5066171541` ↔ `bp-6d11f0f74c`).
- **Contention order:** `CONTENTION-ORDER.json` — 14 Thailand clusters first, then Cartagena / Chennai / Kolkata, then the 99 two-plus.

---

## UAE worked example (the reference pattern — already on `main` + this PR)

**8 UAE groups** (`cluster::city`): Dubai · Abu Dhabi · Sharjah[uae] · RAK[uae] + Sharjah / RAK / Khasab / Fujairah [uae-east-coast].

**Dubai heroes:** Atlantis The Palm ↔ Mina Rashid (12.9 nm) · Bluewaters ↔ The World Islands (9.9) · Dubai Harbour ↔ The World Islands (8.9) · Atlantis ↔ Festival City Marina (15.2)
**Abu Dhabi heroes:** Yas Marina ↔ Saadiyat (11.4) · Rabdan ↔ Saadiyat (9.5) · Emirates Palace ↔ Saadiyat (8.9) · Emirates Palace ↔ Yas (18.0)

All bound to real sealed `rn-*` route_ids. Trivial < 3 nm hops, junk endpoints, and out-of-range junk excluded by construction.

---

## Guardrails (permanent)

- **Never invent route_ids or L3 demand** — null beats wrong.
- **Caspian Baku ↔ Aktau never mint** (~250 nm, outside N30 range).
- Do **not** run `regen_pta_economics.py --all` on batch-5; do **not** rewrite WSF `growth_case`.
- `archetype` chips use the canonical set (tourism / essential_mobility / luxury / super_app / ride_hail).
- Dedupe at seal time; `cluster_id` sync; keep defensive Set dedupes until upstream fixes ship.

---

## Deliverables checklist

**Grok Pass 1:** sealed `ROUTES.json` (all 116 clusters) · 3 gates green · finance spine identity per multi-partner geography · partner scopes derived · slim per-market manifests emitted.
**Tasklet Pass 2:** `CANONICAL-MARQUEES.json` global (all `cluster::city` groups).
**Grok Pass 3:** partner featured/wow applied · label scrub to source BPs · finance cascade · deploy.

**Attached in this PR:** `gen_canonical_marquees.py` (v2.2) · `CANONICAL-MARQUEES.json` (UAE worked example) · `MARQUEE-RETIRE-LIST.json` · `LABEL-SCRUB.json` · `SUSPECT-ENDPOINTS.json` · `CONTENTION-ORDER.json` · `CROSS-PARTNER-INHERITANCE-AUDIT.json`.
