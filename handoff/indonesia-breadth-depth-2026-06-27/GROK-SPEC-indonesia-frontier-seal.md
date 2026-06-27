# GROK SPEC — Indonesia breadth & depth: frontier seal + economics cascade

**Owner of this file:** Tasklet → Grok handoff. **Partners:** Gojek (`partner-pitch/partners/gojek.json`) + Grab (`partner-pitch/partners/grab.json`).
**Rule reminders:** ID-based matching only · null beats confidently-wrong · inherit every real corridor 1:1, never invent · do not rebuild the live Gojek/Grab decks · plain-English partner copy (run `partner_copy_lint.py`).

Tasklet has completed the **map + proposal** layer (Phase 1). Grok owns the deterministic **geometry + economics** seal (Phase 2). After Grok hands back, Tasklet runs the **cascade** (Phase 3). Nothing here asks Grok to touch decks or rewrite Tasklet-authored prose.

---

## What Tasklet already did (Phase 1 — done, in this PR)
- **Full map representation:** both partners' `network_footprint[]` now carry all **13 Atlas Indonesia geos + Singapore**, with the komodo/riau `coastal_aspirational` render bug fixed and **Derawan added** (it was missing from both).
- **10 complete Gojek sub-proposals** (no stubs): jakarta, bali-nusa-gili, lombok, komodo-flores, sumba, riau-singapore, singapore, raja-ampat, likupang, lake-toba — each with full field set + 3 phases (Prove→Scale→Mature) + `featured_routes`.
- **10 Grab Indonesia sub-proposals** mirrored (singapore, cross-border, bali, jakarta, lombok, komodo-flores, sumba, raja-ampat, likupang, lake-toba). Bali anchors narrowed to `bali-indonesia` now that lombok/komodo are standalone.
- **4 roll-up dots** on both (karimunjawa, banda, derawan, wakatobi) — map presence, explicitly not full pages.
- `eastern-indonesia` bundle retired; **Sabah/Kota Kinabalu (Malaysia) journeys removed** (parked in `_PARKED-sabah-journeys.json` for a future Borneo market — do not seal them into an Indonesia geo).
- Anchor-city crosswalks: `gojek-ANCHOR-CITY-CROSSWALK.json`, `grab-ANCHOR-CITY-CROSSWALK.json` — every Indonesia anchor resolves to an Atlas `city_id` (Gate A green).

## Geometry/economics ground truth (so Grok knows the exact lane per geo)
| Geo | Geometry today | Economics | Grok action |
|---|---|---|---|
| bali / lombok / komodo-flores / sumba | bali bucket corridors sealed (9/10 route_ids) | present (most) | Close the 1 missing route_id (Lombok↔Komodo 237nm); confirm sumba Komodo-link econ |
| jakarta | 3/5 route_ids sealed | present | Mint the 2 missing (self-loop Ancol/Batavia corridors) |
| riau-islands / cross-border | sealed | present | none (verify) |
| **singapore** | **2/16 route_ids — SEAL GAP** | partial | **Mint the 14 unsealed SG corridors' route_ids + economics** |
| **raja-ampat** | `ics-` geometry refs exist on journeys but **NOT in corridor registry** | pending | **Register corridors into `corridors.json`, run economics, bind route_ids** |
| **likupang** | `ics-` geometry refs exist, not in registry | pending | **Register corridors, run economics, bind route_ids** |
| **lake-toba** | none (brief-only) | none | **Mint BPs + corridors + route_ids + economics** |
| karimunjawa / banda / derawan / wakatobi (dots) | none | none | **Mint ≥1 node + 1–2 representative corridors each** so dot+line render |

## Per-geo seal needs (from `_seal-needs.json`, generated from the partner JSON)
- **raja-ampat** — register corridors; economics cascade; bind `featured_routes`. Existing geometry refs to reconcile: `ics-da5220fd24, ics-5840f85047, ics-71281cdfb5, ics-90f2ce57d8`.
- **likupang** — register corridors; economics cascade; bind `featured_routes`. Refs: `ics-ab1b7a224c, ics-c142307006`.
- **lake-toba** — mint BPs + corridors + route_ids; economics cascade; bind `featured_routes`. No refs (greenfield mint).

---

## Phase 2 — Grok build sequence (deterministic)
1. **Mint frontier geometry** from the city briefs' `signature_routes` prose as spec (do not invent beyond the briefs):
   - Priority A (full sub-proposals): **raja-ampat, likupang, lake-toba** — seal the featured corridors first.
   - Priority B (roll-up dots): **karimunjawa, banda, derawan, wakatobi** — ≥1 node + 1–2 representative corridors each.
2. **Close existing seal gaps:** singapore (14 corridors), jakarta (2), bali (Lombok↔Komodo 1), cross-border (verify).
3. **Range-gate every corridor by hull:** ≤70nm → N30/Pioneer II; 75–150nm → Quanta-LR (render `amber-dashed`); >150nm → Quanta-LR flagged for review (e.g. Lombok↔Komodo 237nm, Bali↔Sumba ~300nm). Emit a `VESSEL-REGATE-LEDGER`.
4. **Economics:** run `aggregate.py → growth.py → splice_growth_into_partner.py` over the newly-corridored Indonesia markets for **both** partners; produce per-market economics + `{partner}-aggregate.json`. Anchor on sourced demand, never the 30k placeholder.
5. **Render QA:** confirm all 13 Indonesia geos + Singapore render on **both** Gojek and Grab maps (anchor-city ID match; dots now, lines where minted). Run `partner_copy_lint.py` (blocking) + the land-crossing gate.
6. **Reseal + commit.**

## Phase 2 → Phase 3 handback (what Grok returns to Tasklet)
Per the Grok-handback rule, return: **branch name, PR link, commit SHA, exact files changed, validation receipt, and explicit nulls/held items.** Specifically:
- the minted `route_id`s per geo (so Tasklet binds `featured_routes` null→id),
- the per-market economics + aggregate paths,
- render-QA receipt (both maps, both partners),
- any geo that could not be sealed (held, with reason) — null beats a fake corridor.

## Phase 3 — Tasklet (after handback, not in this PR)
1. Bind returned `route_id`s into raja-ampat/likupang/lake-toba `featured_routes` (replace null).
2. Cascade economics → transparent sheet (in place, preserve URL) + master tracker + economics sidecar.
3. Parity QA Gates A–F both partners; magnitudes sanity-check.
4. Decks remain untouched until explicitly chosen.

---

## Guardrails
- Do **not** seal the parked Sabah/Kota Kinabalu journeys into any Indonesia geo.
- Do **not** rebuild or overwrite the live Gojek (`13nn...`) or Grab Thailand (`11WC...`) decks.
- Do **not** invent corridors beyond the city-brief `signature_routes`; 1:1 inheritance only.
- Keep `super_app` archetype/category (gold convention — do not normalize).
- `_mirrored_from` tags on Grab markets are provenance; safe to keep.
