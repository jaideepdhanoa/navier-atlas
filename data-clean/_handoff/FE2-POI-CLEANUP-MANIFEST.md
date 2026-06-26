# FE-2 — Locale/POI cleanup manifest (2026-06-26)

Source: `data-clean/FEATURES_BY_TYPE.json` (12,494 POIs → **12,380**, −114).
Scope order honored: Thailand first, then all markets. Rule applied: **prefer dropping wrong-city/junk over guessing; null beats confidently-wrong; exactness over coverage.**

## What was DROPPED (114) — applied in this PR
Every dropped id was verified **zero-reference** across `ROUTES.json`, `STORIES.json`, `CLUSTERS.json`, and all `data-clean/partners/*.json` — so removal breaks no geometry, story, cluster, or partner page.

Two junk classes:
1. **Scraped non-marine listings** (~100): coffee shops/cafés, restaurants (ramen/sushi/osteria/pizza/burger), bakeries, yacht-charter & boat-rental ads, wedding-catering venues, "JUMP N FUN", dinner-cruise tour ads, multilingual ad spam. These were never boarding points — Google-Places scrape residue mis-typed as ferry_terminal/marina/etc.
2. **Broken-coordinate pins** (13): 9 Minor Hotels property pins (`q=None`, rendering 4,000–15,800 km from their city — e.g. Oaks "Gold Coast" at 15,809 km), `Panama City` (geocoded to Panama City **FL**), `Volos (mainland)` (2,338 km off), `Six Senses Hua Hin (planned)` (lat wrong), and the **Mae Haad Pier duplicate** wrongly parented to koh-samui (correct koh-tao copy retained).

Full id list: `dropped-114-ids.json`. Thailand-scope removals: Six Senses Hua Hin, Mae Haad-Samui duplicate, Krabi Boat Rental (ad).

False-positive guard: `Dinner Key Marina` (legit Miami marina) was explicitly whitelisted after my first-pass `dinner` token caught it.

## What was NOT touched — HANDED TO GROK (needs reseal)
This PR edits sealed atlas data, so a **gold reseal** is required after merge (ties to SEAL gate, issue #119).

1. **Route-bound junk (16)** — `flag-routebound-junk-16-ids.json`. Junk-named POIs (cafés, yacht ads, "Terra Pizza Çeşme Marina", "Japanos Ramen Bento & Sushi Bar") that a **route is currently bound to**. Dropping would break geometry. Grok must **rebind each route to the correct real pier, then drop the junk POI**.
2. **Hua Hin Pier `bp-cd5ab934c8`** — broken coordinates (renders ~550 km south near Koh Lanta) but **anchors 4 routes**. Cannot drop or guess coords. Grok satellite-validates the true Hua Hin Pier coordinate and reseals.
3. **Multi-parent duplicate dedup (1,069 groups / 1,283 redundant copies)** — `grok-dedup-worklist.json`. The same physical pier listed under 2–4 different parent cities (heavy in the UAE emirates: an Abu Dhabi marina also under Ras Al Khaimah/Sharjah). I deliberately did **not** bulk-delete these: my nearest-parent keeper heuristic proved unreliable on a validated spot-check (Bang Bao Pier — a Bangkok-orphan-parented copy would have caused the correct Koh-Chang copy to be dropped), and at least one redundant copy is referenced in CLUSTERS.json. Recommended keeper rule for Grok: **keep the single copy whose `parent_city_id` is in the city list AND nearest the coordinate; drop orphan-parent and farther-parent copies only after confirming each dropped id is unreferenced in ROUTES/STORIES/CLUSTERS/partners; reseal.**

## Reseal dependency
FEATURES_BY_TYPE.json is sealed. After merge: run the bp/water + story gates and issue a gold reseal (#119) so the live Atlas map re-bakes without the 114 junk pins.
