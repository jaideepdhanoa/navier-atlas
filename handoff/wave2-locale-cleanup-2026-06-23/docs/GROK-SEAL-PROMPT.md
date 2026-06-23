# Grok seal mandate — Wave 2 ("the rest") locale + POI cleanup

**Pass:** `wave2-locale-poi-cleanup-2026-06-23` · Fourth in the program: **UAE (PR #82) → Thailand (PR #89) →
Bolt markets (PR #90) → the rest (this).** Directive: **"rather not have them than have them wrong."**
Tasklet supplies a country-agnostic spec/ledger (no hand-curated place aliases — no guessing); Grok applies
deterministically, runs the geometric residual gate, and reseals. Input package only; `main` is source of truth.

## Scope
Every market **outside** UAE / Thailand / the Bolt-20 (already done): **151 sealed cities, 9,195 POIs** across
SEA (Grab), French Polynesia, Maldives, India, LatAm, US, Japan, Korea, etc. Sovereign Saudi-PIF cities
(NEOM / Red Sea / AMAALA / Sindalah / Qiddiya / Diriyah) are **excluded** (guard active).

## Apply (from `inputs/WAVE2-CLEANUP-LEDGER.json`)
**POIs (9,195):**
- `dedup_exact_drops` (**54**) — identical parent+name+coords double-ingestion. Drop the non-canonical copy.
- `retag_identity` (**120**) — POI name carries a **different in-scope city's** sealed name, geometry strongly
  corroborating (target ≪ parent distance). Re-parent to the named city. Examples: Lombok ports under Bali →
  Lombok; Bintan resort jetties under **Jakarta** → Riau (19 nm vs 463 nm); Phu Quoc under Koh Rong → Vietnam;
  Manila/Singapore/Tokyo hub terminals scattered under neighbor cities → back to their hub. **Re-route any
  corridor whose endpoint moves** (route key `{city_id}__{bp_id}` changes).
- `junk_drops` (**115**) — retail / cafe / clinic / cargo-logistics / boat-rental / tour-operator / harbour-master,
  plus **cross-border corridor pointers/endpoints** (strategy annotations, not parent-city boarding points).
- `review_name_only` (**16**) — name carries another city but geometry not corroborating → **your residual gate**.
- `kept_in_place` (**8,890**).

**Locales:** `keep` (**11**) · `drop` (**17**, high-confidence only: names a different country/territory, or
>150 nm from parent = a different cluster) · `review_residual` (**47**, same-country far/combined labels —
**your gate** decides keep-as-own-geography vs retag/split; do NOT mass-delete the cluster's own archipelago).

## Coverage gap — `coverage_gap_no_centroid` (11)
Cities in scope with **no sealed centroid** (Algarve, Porto, Baku/Aktau Caspian, Haifa, Gwadar, Halifax/Gulf-
Islands/San-Juan/Bar-Harbor, Nosy Be). Tasklet could not geometrically test these. **Seal/centroid them, then
run the residual gate over them.** 0 silent drops.

## Permanent guardrail (fold into the seal gate)
A row is a `locale` pin only if (1) same country as parent, (2) single placeable waterfront place, (3) not a
routing artifact. A POI's `parent_city_id` = the nearest in-country city whose name it carries — never the
regional flagship by default.

## Acceptance (QA report)
- 0 silent drops: every dropped/retagged POI in the ledger or a drop-ledger with a reason.
- All 120 retags re-parented + any moved corridor re-routed; 0 orphan routes; 0 land-crossings post-allowlist.
- Locale `review_residual` + POI `review_name_only` resolved via geometry/water-adjacency, not deletion-by-default.
- 11 no-centroid cities sealed + gated.
- before→after POI totals per city; counts of dedup/retag/junk/keep.
