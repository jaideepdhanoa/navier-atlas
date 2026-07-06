# Master handoff — Tasklet → Grok (corridor inheritance program)
**Date:** 2026-07-05 · **From:** Tasklet · **Re:** UAE spaghetti fix → global corridor inheritance across geometry, finance, and presentation layers.

---

## 0. The sequence (Tasklet ↔ Grok)
Clean division of labor, per phase:

| Step | Owner | What |
|---|---|---|
| 1. Diagnose + discover | **Tasklet** | ✅ Done — root causes, cross-partner audits, contracts (below). |
| 2. Author contracts + canonical sets | **Tasklet** | ✅ Contracts done. Curating canonical corridor/marquee sets per market (UAE in progress). |
| 3. Merge PRs | **Jaideep** | PRs #181, #183–#188 open. Your reseal waits on these. |
| 4. Reseal geometry (global `ROUTES.json`) | **Grok** | Consolidate to significant deduped clean set; route survivors from scratch; land-flag → 0. |
| 5. Wire inheritance gates | **Grok** | `validate_partner_inheritance.py` (geometry+featured/wow) + `validate_finance_inheritance.py` (finance spine). |
| 6. Derive partner views + cascade | **Grok** | `partner_corridors = global_canonical ∩ partner.clusters`; finance overlay; deck economics. |
| 7. Stage membership scopes + tag global sets | **Tasklet** | Post-reseal: tag `cluster_id` on global corridors, stage `_map_scope`. |
| 8. Roll out next market | **Both** | UAE → Thailand → Indonesia → India → Colombia → Singapore. |

**Rule of thumb:** Tasklet owns *what corridors exist and which are canonical* (sourcing, curation, contracts). Grok owns *deterministic derivation, geometry sealing, gates, and cascade*. Neither invents route_ids or L3 numbers — null beats wrong.

---

## 1. What we discovered (three layers, same disease)
Corridors were being **hand-curated per partner** at every layer, so partners sharing a market diverged. Corridors belong to **geography, not partners.**

### Layer A — Geometry (map corridors) — `ROUTES.json`
- **UAE:** 666 routes on 348 BPs; 202 land-flagged. Root cause = all-pairs over-meshing + waypoints applied but **insufficient** (233 still clip land after bending; 64 have no waypoint; 23 over-range). *Correction to earlier claim:* 788 hand-waypoints WERE applied (246/266 flagged carry `_geometry_fix` stamp) — they're just not enough. Fix = cut to significant deduped set, route survivors cleanly from scratch.
- **Cross-partner:** 116 clusters shared by 2+ partners; 2,039 hand-curated corridor entries. `partner-scope.mjs` already derives `_map_scope.cluster_city_ids` from CLUSTERS.json (healthy) — but `featured_routes`/`wow_corridors`/`route_ids` are hand-curated = the divergence source.

### Layer B — Finance (TAM-ladder corridors) — `finance/model/corridors.json`
- 84 market keys; 13 geographies shared by 2+ partners **diverge**.
- **UAE's 4 partners (careem 39 · bolt 37 · yango 37 · noon 12) share ZERO of 122 route_ids** — four different TAM ladders on the same water.
- Qatar 3/21 common; Egypt/Morocco/Tunisia 0 common; gulf-authority 3/51.
- **India (ola/rapido/uber-india) already identical** = proof standardization works and is the target.
- Registry hygiene: duplicate `mumbai` vs `india-mumbai` keys; 5 UAE keys must draw one spine.

### Layer C — Presentation (featured/wow) — partner JSONs
- **1,293 marquee entries** (945 featured + 348 wow) in **3 competing schemas** (822 from/to dicts, 348 strings, 123 named).
- No canonical per-cluster set — every partner spotlights a different subset of the same city.
- **Confirmed strange/out-of-range featured routes:** Careem (+Noon) feature `Abu Dhabi→Muscat` & `Fujairah→Muscat` (UAE→Oman, ~200nm); Bolt features `Barcelona→Palma` (~130nm open sea). These are the "strange routes" Jaideep saw.
- **RESOLVED — canonical marquee sets built (`CANONICAL-MARQUEES.json`, v2.1):** Curated **city-level** (not country-cluster) so every partner in a city inherits the SAME set — all UAE partners see one Dubai set, one Abu Dhabi set, etc. **217 cities**, wow ≤5 / featured ≤8. Ranking = **hero (water-beats-road)**: distance sweet-spot (~12nm) + island + cross-city; traffic/crowd = tiebreaker only. **Firm 3nm floor** kills trivial resort hops. **978 current entries retired** → `MARQUEE-RETIRE-LIST.json` (archive, not delete). Junk-endpoint filter + out-of-range gate exclude the Muscat/Palma junk by construction.
  - **Label scrub (`LABEL-SCRUB.json`):** 6 aggregate endpoint labels trimmed to primary place name ("Cartagena & The Rosario Islands"→"Cartagena", "Mahé & Inner Islands"→"Mahé", etc.) with `node_id`→`{orig,clean}` for you to fix the **source BP label**; 2 territory-aggregates ("Andaman & Nicobar Islands", "US & British Virgin Islands") flagged `needs_bp_sourcing` — **do not invent a pier; source a real one** (null beats wrong).
  - **Bangkok river exception:** `RIVER_CITIES={bangkok-thailand}` exempt from the 3nm floor down to 0.4nm with a river score (traffic + iconic-destination). Restores Chao Phraya Express marquees (Sathorn↔Khao San/Grand Palace/ICONSIAM; Tha Tien↔Wang Lang/Wat Arun). Only clean-geometry hops selected; land-flagged river false-positives left for you to channel-route.

### Layer D — Singapore (diagnosed this session — same pattern as UAE)
- 342 Singapore-region routes; 25 land-flagged; **23 clip >0.2km land**; 2 have no geometry fix; 13 over 30nm (cross-border Batam/Bintan/Riau — range-check, don't auto-kill legit cross-border).
- Root cause identical to UAE: **Marina Bay Cruise Centre (MBCCS) hub over-meshing** (37 routes originate there) + fixes applied but insufficient.
- Worst clippers: MBCCS→South Islands **39.8km** land, Punggol Marina **32km**, MBCCS→Raffles 13.7km, MBCCS→Marina 12.3km.

---

## 2. The contracts (permanent — all in `handoff/uae-consolidation/` + Skill)
1. **`CORRIDOR-INHERITANCE-CONTRACT.md`** (geometry): `partner_corridors = global_canonical ∩ partner.clusters`. No `featured_routes`/`wow_corridors` outside inherited set.
2. **`FINANCE-CORRIDOR-INHERITANCE-CONTRACT.md`** (finance): **shared corridor spine** (route_id set identical across partners in a market) + **partner-specific economics overlay** (`L3_locals`/`capture_rate`/`archetype`/`fleet_basis` MAY differ).
3. **`FEATURED-WOW-STANDARDIZATION.md`** (presentation): one canonical `cluster.marquee_corridors[]` per cluster (top ~3–6 wow / ≤8 featured, quality-gated), inherited identically; uniform schema `{route_id,from_label,to_label,cluster_id}`; retire the rest to `handoff/archive/`.
4. **Skill:** `/tasklet/workspace/home/corridor-inheritance/SKILL.md` — extended to cover all three layers + both gates (validated).

---

## 3. Open PRs Grok needs to process (after Jaideep merges)
| PR | Title | What Grok does post-merge |
|---|---|---|
| **#188** | UAE consolidation + global inheritance (geometry+finance+featured/wow contracts + all audits) | **Primary.** Reseal UAE global `ROUTES.json` (dedupe → clean set, route from scratch, land-flag→0); wire both gates; derive partner views. |
| **#184** | Yango finance correction (restores AZ+TN; 17-market roster) | Rebuild model sheet + cascade growth_case + ladder (stale sheet inflating rungs 4–18×). Spec: `GROK-SPEC-yango-model-rebuild-and-ladder-2026-07-05.md`. |
| **#185** | Caspian+Maghreb enrichment (35 BPs, 23 corridors, hand-waypoints) | Seal geometry for Baku/Aktau, Tunisia, Algeria, Morocco. |
| **#187** | Peru+Senegal BP density (~18 BPs, 12 corridors) | Seal geometry (4-market density spec: Peru+Senegal+Caspian+Maghreb). |
| **#186** | Yango deck backgrounds + asset registry | Registry only — no Grok action beyond ack. |
| **#183** | Yango front-end fix (restores AZ+TN to `_map_scope`) | Ack; feeds inheritance derivation. |
| **#181** | Yango deck.config sync | Re-sync to 15-slide manifest (deck grew 12→15). |

**Merge order matters:** #184 (finance) and #188 (contracts+gates) before any reseal, so the gates exist when geometry re-derives.

---

## 4. What Grok does from here — ordered
1. **UAE geometry reseal** (`ROUTES.json`, global not partner view): consolidate 666→significant deduped set (every genuine distinct on-water OD pair; no cap; kill dupes, <2nm hops, parallel edges, land-crossers); route survivors cleanly from scratch using `data-clean/uae_hand_waypoints.json` where valid, re-route where insufficient; **land-flag → 0**; tag every corridor with `cluster_id`.
2. **Wire gates:** `validate_partner_inheritance.py` (geometry subset + featured/wow subset + schema + cleanliness) and `validate_finance_inheritance.py` (finance spine identity per shared geography, overlay may differ). FAIL seal/model-build on divergence.
3. **Derive partner views deterministically:** `partner_corridors = global_canonical ∩ partner.clusters`; finance spine = same, overlay per partner; featured/wow = `cluster.marquee_corridors ∩ partner.clusters`.
4. **Yango finance rebuild + cascade** (#184): rebuild sheet `1fvB_tc8…`, cascade growth_case, refresh deck slide 4 KPIs + slide 9 ladder.
5. **Seal enrichment geometry** (#185, #187): Caspian/Maghreb/Peru/Senegal.
6. **Roll out next markets** same pattern: Thailand (highest contention — 6 partners × 14 clusters) → Indonesia → India → Colombia → **Singapore** (diagnosis ready in `SINGAPORE-DIAGNOSIS.json`; MBCCS hub de-mesh + reroute the 23 land-clippers).

**Permanent guardrails (do not violate):** Never run `regen_pta_economics.py --all` on batch-5. Never rewrite WSF growth_case numbers. Never invent route_ids or L3 demand — null beats wrong. Keep defensive Set dedupes until upstream fixes ship. No `rollup` finance market keys.

---

## 5. Artifacts (all in `handoff/uae-consolidation/` on PR #188)
- `UAE-SPAGHETTI-DIAGNOSIS-AND-PLAN.md` · `GROK-SPEC-uae-corridor-consolidation.md`
- `CORRIDOR-INHERITANCE-CONTRACT.md` · `CROSS-PARTNER-INHERITANCE-AUDIT.json`
- `FINANCE-CORRIDOR-INHERITANCE-CONTRACT.md` · `FINANCE-CORRIDOR-AUDIT.json`
- `FEATURED-WOW-STANDARDIZATION.md` · `FEATURED-WOW-AUDIT.json`
- `CANONICAL-MARQUEES.json` (city-level sets) · `MARQUEE-RETIRE-LIST.json` · `CANONICAL-MARQUEES-REVIEW.md` · `CANONICAL-MARQUEES-ADDENDUM.md` · `LABEL-SCRUB.json` · `gen_canonical_marquees.py`
- `SINGAPORE-DIAGNOSIS.json` · `GROK-MASTER-HANDOFF-2026-07-05.md` (this note)
- Skill: `/tasklet/workspace/home/corridor-inheritance/SKILL.md`
