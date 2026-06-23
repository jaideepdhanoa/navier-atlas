# Grok seal mandate — UAE locale + POI cleanup (2026-06-24)

## Why
Jaideep flagged the UAE map as "a complete mess": Abu Dhabi locales (Corniche, Saadiyat,
Sir Bani Yas) rendering **under Dubai**; combined multi-place labels producing pins that land
nowhere near the named place (e.g. "Abu Dhabi Corniche / Saadiyat" plotted ~95 km east of either;
"Al Dhafra / Western Region coastal (Mugheirah, Sila, Marawah…)" plotted in Abu Dhabi **city**);
and a vague "Sharjah / Ajman / RAK coastal hop" that means nothing and lands near the Oman mountains.

Two root causes:
1. **The seal promoted *every* sub-cluster row into a rendered locale pin** — including cross-emirate
   "corridor endpoint" / "mid-corridor" rows that are strategy analysis, not places.
2. **A radius scrape** tagged POIs from neighbouring emirates / across the Gulf to the search-origin city.

## Mandate (deterministic)
Apply `inputs/UAE-CLEANUP-LEDGER.json`. Reseal to the next gold tag.

### A. Locale layer — exact
- **DROP** the 14 locales in `locale_layer.drop[]` (by `id`). Remove them from `FEATURES_BY_TYPE.json`
  `locale[]`, from `CLUSTERS.json`, and delete the matching `data-clean/city_briefs/<id>.json` stubs.
- **KEEP** the 17 in `locale_layer.keep[]` unchanged (geometry already accurate).
- Net UAE locales after: Dubai 6, Abu Dhabi 5, Sharjah 3, RAK 1, Fujairah 2.

### B. POI layer — high-confidence drops + residual gate
- **DROP** the 165 POIs in `poi_layer.drops` (by `id`) — wrong-emirate identity, foreign-country,
  explicit cross-emirate pointer, or junk-keyword (restaurants/salons/clinics/trading firms).
- **Residual gate (you own this):** for every *remaining* UAE POI, run the water-adjacency +
  nearest-city gazetteer check. Any POI that is not on its parent city's own emirate waterfront and
  has no in-emirate gazetteer match → **drop or re-tag to the correct city**. Honour the per-emirate
  legitimately-distant allowlist so you do NOT nuke real outliers:
  - **abu-dhabi-uae:** Al Dhafra / Western Region (Sir Bani Yas, Delma/Dalma, Mugheirah, Sila,
    Marawah, Jebel Dhanna, Ruwais, Mirfa, Al Yasat) are genuine — keep.
  - **sharjah-uae:** east-coast exclaves (Khorfakkan, Kalba, Khor Kalba) are genuine Sharjah — keep.
  - **fujairah-uae:** the ~70 km N–S coast (Dibba, Aqah, Murbah, Dadna) is genuine — keep.
- **0 silent drops:** every UAE POI ends in keep / retag / drop-with-reason in your QA report.

### C. Permanent guardrail (so this can't recur)
Add to the seal rules: **a sub-cluster / corridor row is promoted to a rendered `locale` pin only if
it is (1) in the same emirate/country as its parent city, (2) a single placeable waterfront place,
and (3) not a routing artifact** (name matching `corridor endpoint | mid-corridor | overland |
from <place> | cross-emirate | cross-border | pointer`). Rows failing this stay as **route edges /
strategy text**, never as origin-city locale pins. The markdown briefs legitimately keep cross-emirate
Quanta-LR corridor rows for *analysis* — they must simply never render as pins again.

## Acceptance gate (QA report must show)
- UAE locales: exactly the 17 keeps render; the 14 drops are gone from `locale[]`, `CLUSTERS.json`, briefs.
- No UAE locale pin sits in a different emirate than its parent city; no combined-label pin lands >5 km
  from every place it names.
- UAE POIs: 165 ledger drops applied; residual-gate counts (kept / retagged / dropped+reason); the
  per-emirate allowlist outliers survive.
- Guardrail active: 0 corridor-endpoint / cross-emirate rows present as locale pins.
- before→after UAE locale + POI totals; land-crossing = 0; every surviving POI carries a source id.
