# Changelog for Claude — 2026-05-31 (pm) — Waves 11/12 + Macau + Manila fix + deck ingest

This is a **consolidated sealed rebuild**. New sealed bundle in `atlas-repo/data-clean/`
(SEAL.json refreshed). Build: **cities=108, pois=10,364, routes=4,046 (land-clean), stories=12,
briefs=112, partners=10**. All gates PASS (integrity, conformance, externalization, land-crossing).

---

## 1. Manila over-bundle — FIXED (your note, PR #9)
- `manila-philippines` map label now = **"Manila"** (was the 5-name rollup). Applied via
  `CITY_SHORTNAME_OVERRIDE` in build.py. Full rollup retained in node `name` + brief narrative.
- Brief `display`/`display_name` reconciled to **"Manila"** so panel title == map label.
- **Legit 2-/3-part market bundles LEFT AS-IS** per your guidance: Boracay/Caticlan, Cebu/Mactan,
  Da Nang/Hoi An/Lăng Cô, Busan/Geoje.
- **Dupe collapse**: added a permanent **dedupe-by-id guard** at feature assembly in build.py
  (`_seen_node_feat_ids`) — any node id now emits at most ONE feature. Verified: **0 duplicate
  city pins** in sealed FEATURES_BY_TYPE (manila/cebu/palawan/hong-kong all single).
- grab.json already uses canonical split ids (`manila-philippines`/`cebu-philippines`/
  `palawan-philippines`) — no stale composite id present. ✓

## 2. Macau — NEW East Asia node
- `macau-china` — full 5-layer wiring (brief, stub, anchor, BP_CITY_MAP, 29 BPs). HK↔Macau
  cross-border + Cotai resort transfers + PRD grid.

## 3. Wave 11 — Norway fjords + Stockholm + Monaco (Europe)
New nodes (all 5-layer wired, densified, briefs leak+cap clean):
- `bergen-norway` (92 BP), `geiranger-norway` (66 BP), `stavanger-norway` (73 BP) — **2026
  zero-emission fjord mandate** is the headline tailwind.
- `stockholm-sweden` (150 BP) — Waxholmsbolaget 7M pax, electric-ferry procurement.
- `monaco-monaco` (60 BP) — de-bundled from Côte d'Azur into its own sovereign node; GP/Yacht
  Show event-surge fleet. (Côte d'Azur INDEX label trimmed to "Nice / Cannes / St-Tropez".)

## 4. Wave 12 — French Polynesia + Fiji (Oceania)
- `bora-bora-french-polynesia` (48 BP) — greenfield luxury island-hop; Tahiti↔Bora Bora 140 nm
  = Quanta-LR line-haul.
- `nadi-fiji` (73 BP) — Mamanuca/Yasawa reef-water shuttle market.
- HK/PRD volume play covered via the new Macau node + existing `hong-kong`.

## 5. Decks ingested (KB only; weave guidance)
- `reference/navier-decks-2026.md` — iPad deck (demand sizing, traffic-vs-flight event-surge
  matrix, unit-economics **DECK-ONLY**) + TEDX deck (maritime-stack platform thesis).
- **Event-surge journeys woven** into Miami (Art Basel), Venice (Film Festival), Côte d'Azur
  (Monaco GP / Cannes) briefs — website-safe framing only; $/mile economics stay deck-only.

## 6. Routing note
- Routes scrubbed land-clean by `scrub_land_routes.py` (dropped 318 land-crossers).
- **Still pending re-application** (lost in earlier /tmp wipe; NOT in this build):
  harbour-overrides open-water coords (Miami/Palm Beach/Sharjah/RAK/Muscat/Salalah),
  `_sea_snap()`, span-proportional grid pad, and the 6 synthetic spoke aliases (now tracked
  in `integrity/known-gaps.json` as WARN). These light up ~11 extra inter-corridor edges; not
  blocking. Your frontend items from the route-hardening changelog still stand
  (curve-clamp + visual QA).

## Ship surface
- Bake from `atlas-repo/data-clean/` (NOT raw partner-pitch/). SEAL.json carries hashes +
  all four gate verdicts.
