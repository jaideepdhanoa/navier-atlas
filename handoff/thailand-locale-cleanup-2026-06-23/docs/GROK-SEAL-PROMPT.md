# Grok seal mandate — Thailand locale + POI cleanup (2026-06-23)

## Why
Jaideep flagged the Thailand map as "a complete mess — locales showing up under the completely
wrong cities." Directive: **rather not have them than have them wrong.** Root causes:
1. **Wrong parent_city_id on POIs.** Hand-authored pier lists were filed under the nearest *flagship*
   rather than the real city: Pattaya / Koh Larn / Hua Hin / Koh Samet / Koh Chang piers parented to
   **bangkok-thailand**; Krabi / Phi Phi / Koh Phangan / Koh Tao piers parented to
   **phuket-phang-nga-thailand** or **koh-samui-thailand**.
2. **Double-ingestion.** Phuket POIs were ingested twice (2026-05-29 and 2026-06-19) → 74 exact-duplicate
   copies (identical name + identical coordinates).
3. **Locale layer carries corridor artifacts & foreign places** rendered as origin-city pins:
   "Koh Samui (cross-Gulf)" 257 nm under Bangkok, "Langkawi (Malaysia)"/"Penang (Malaysia)" under Phuket,
   combined "Krabi (…) + Phi Phi (…)", "Pattaya / Ocean Marina" under Bangkok.

## Mandate (deterministic) — apply `inputs/THAILAND-CLEANUP-LEDGER.json` in this order
1. **Dedup (74).** Drop each `poi_layer.dedup_exact_drops` id; keep its `keep` id. (Exact same parent +
   name + coords — pure double-ingestion.)
2. **Retag (53).** Re-parent each `poi_layer.retag_identity` POI from `from` → `to`. The POI names the
   target city unambiguously and is geometrically closer to it (or carries an unambiguous primary
   city-name token). Update the POI `id` prefix + `parent_city_id` to the new city, and re-home its route
   endpoints. Targets include the new depth-pass cities **hua-hin-thailand / cha-am-thailand /
   koh-samet-thailand** (PR #88) — seal those first so the retag targets exist.
3. **Drop junk/annotation (19).** Remove each `poi_layer.junk_annotation_drops` id — McDonald's, pharmacy,
   coffee shop, guest house, boat-rental/tour-operator listings, harbour-master offices, naval bases, and
   strategy annotations ("soft-landing cluster (no formal pier)", "NE-monsoon blackout flag …").
4. **Locale layer.** DROP the 8 `locale_layer.drop` ids from `FEATURES_BY_TYPE.json` `locale[]`,
   `CLUSTERS.json`, and any matching brief stub. KEEP the 3 `locale_layer.keep` (genuine in-Phuket areas:
   Phang Nga Bay, Phuket east coast, Phuket west-coast beach belt).
5. **Residual gate (you own this).** For every *surviving* Thailand POI, run the water-adjacency +
   nearest-city gazetteer check and **fuzzy near-duplicate merge** (same place, different label — e.g.
   "Nathon Pier" vs "Nathon Pier (Samui mainland gateway)"; "Bangrak (Big Buddha) Pier" vs "Bang Rak Pier
   (Hat Bang Rak / Big Buddha)"). Any POI not on its parent city's own waterfront with no in-city
   gazetteer match → drop or re-tag with a reason. **0 silent drops:** every Thailand POI ends in
   keep / retag / dedup / drop-with-reason.

## Permanent guardrail (so this can't recur) — add to the seal rules
A sub-cluster / corridor row is promoted to a rendered `locale` pin **only if** it is (1) in the **same
country** as its parent city, (2) a **single placeable waterfront place**, and (3) **not a routing
artifact** (name matching `via | cross-gulf | round s tip | gulf-of-thailand-side | corridor | gateway |
" + " | top-level " / " between two city names`). Rows failing this stay **route edges / strategy text**,
never origin-city locale pins. A POI's `parent_city_id` must be the **nearest in-country city whose name
the POI carries** — never the regional flagship by default.

## Acceptance gate (QA report must show)
- POIs: 74 dedup applied; 53 retags applied (with route endpoints re-homed); 19 junk dropped;
  residual-gate counts (kept / retagged / merged / dropped+reason); before→after Thailand POI total
  (363 → ~270 pre-residual).
- No Thailand POI parented to a city it does not name; no Pattaya/Krabi/Phi Phi/Phangan pier left under
  Bangkok/Phuket/Samui.
- Locales: exactly the 3 keeps render; the 8 drops are gone from `locale[]`, `CLUSTERS.json`, briefs;
  no Thailand locale pin sits >40 nm from its parent or names a foreign country.
- Guardrail active: 0 corridor / cross-Gulf / combined rows present as locale pins.
- Land-crossing = 0; every surviving POI carries a source id.
