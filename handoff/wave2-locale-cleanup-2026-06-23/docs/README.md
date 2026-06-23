# Wave 2 ("the rest") locale + POI cleanup — seal handoff

Fourth and final breadth wave of the locale/POI cleanup program (after UAE #82, Thailand #89, Bolt #90).
Covers **every market outside UAE / Thailand / the Bolt-20**: 151 cities, 9,195 POIs.

## Contents
| Path | What |
|---|---|
| `inputs/WAVE2-CLEANUP-LEDGER.json` | The full ledger (POI dedup/retag/junk/review/keep + locale keep/drop/review + coverage gap) |
| `inputs/WAVE2-SCOPE-CITIES.json` | The 151 scoped cities |
| `docs/GROK-SEAL-PROMPT.md` | Seal mandate + acceptance gate |

## Headline counts
- **POIs:** 54 dedup · 120 retag · 115 junk/artifact · 16 review→Grok · 8,890 keep.
- **Locales:** 11 keep · 17 drop (foreign-country or >150 nm only) · 47 review→Grok.
- **Coverage gap:** 11 in-scope cities with no sealed centroid → Grok seals + gates.

## Method (exactness over coverage)
Country-agnostic, gazetteer-free. A POI is only retagged when its name carries a **different in-scope city's
own sealed name** and geometry strongly agrees (target ≪ parent distance). Locales are hard-dropped **only**
when a different country/territory is named or the pin is >150 nm from its parent (a different cluster);
everything borderline — same-country far/combined labels, non-corroborated names — goes to **Grok's geometric
residual gate**, never deleted by default. Null beats confidently-wrong; we do not delete a cluster's own
archipelago.

## Excluded
Sovereign Saudi-PIF cities (NEOM / Red Sea / AMAALA / Sindalah / Qiddiya / Diriyah) — bespoke/held builds.
