# CHANGELOG FOR CLAUDE — 2026-06-05 — City-brief UX fixes (3 items)

Content/label-only reseal. **Geometry byte-unchanged** (ROUTES/STORIES/VESSEL identical except
ROUTES `from_label`/`to_label`; A* not re-run; route count still 5150; land-QA 0 crossers).

## 1. Jakarta de-conflated from Batam/Bintan/Singapore
`data-clean/city_briefs/jakarta-indonesia.json` no longer carries cross-border Singapore/Riau
content. Jakarta = mega-capital + Thousand Islands (Kepulauan Seribu) + inner-harbour only.
The Singapore/Batam/Bintan cross-border cluster remains in `riau-islands-indonesia.json`
(its correct home). No new `batam-indonesia` node was minted (would have been a 3rd overlap).
Jakarta node geocoded to the Marina Batavia waterfront `[106.81342, -6.11967]` (was inland
`[106.8456, -6.2088]`); updated in `nodes.json` and `FEATURES_BY_TYPE.json` (priority_city).
Conflation audit of all 166 briefs found **no other true far-apart conflation** — regional
adjacency clusters (Antigua & Barbuda, Turks & Caicos, Aruba/Curaçao/Bonaire, Bodrum/Turquoise
Coast, etc.) are legitimate and were left intact.

## 2. Distinct boarding-point labels for intra-city routes
1,485 of 1,498 previously-degenerate routes (`from_label == to_label`) now carry distinct
endpoint names derived from each route's polyline endpoints matched to the nearest boarding-point/
POI in the same city cluster. **Labels only — no geometry, no route_id changed.** 13 routes
remain degenerate (no distinct second boarding-point resolvable; renderer keeps hiding those).
Source fix also applied to `route_labels.py` (geometry→BP fallback) so future full builds
reproduce distinct labels.

## 3. `signature_routes` schema: bare string → object  ⚠️ RENDERER CHANGE
Every brief's `signature_routes[]` is now `{ "label": "<verbatim original string>",
"route_id": "<resolved id or null>" }` (mirrors `featured_routes`). Original label text is
preserved verbatim (incl. `↔` and platform suffix). 197 of 551 resolved to a built route
(66 inter-city via city-pair linker, 131 intra via distinctive-terminal match); 354 are
`route_id: null` (no built route — render non-clickable, as with featured_routes). 148 briefs
have object-form signature_routes; 18 briefs have none.

Audit GREEN · postflight PASS (route 5150 · land-QA 0 · leak 0).
