# Grok seal mandate — Bolt-markets locale + POI cleanup (2026-06-23)

## Why
Wave 1b of the locale/POI cleanup (UAE = PR #82, Thailand = PR #89). Same disease across Bolt's footprint:
hand-authored POIs filed under the nearest *flagship* instead of the real city, double-ingestion copies,
and locale rows that are corridor artifacts. Directive: **rather not have them than have them wrong.**
Tasklet supplies the spec/ledger (country-agnostic, **no hand-curated aliases — no guessing**); Grok applies
deterministically and runs the residual gate. Input package only; `main` stays source of truth.

## Scope
Bolt footprint **excluding UAE (done, PR #82) and Thailand (PR #89)**: Bahrain, Croatia, Egypt, Estonia,
Finland, France (Riviera), Greece, Ireland, Italy, Kenya, KSA (Bolt cities only), Monaco, Morocco, Nigeria,
Portugal, Qatar, South Africa, Spain, Sweden, Tanzania. **Sovereign Saudi-PIF cities (NEOM, Red Sea Global,
AMAALA, Sindalah) are explicitly EXCLUDED** — bespoke/held builds, do not touch here.

## Mandate (deterministic) — apply `inputs/BOLT-CLEANUP-LEDGER.json` in order
1. **Dedup (16).** Drop each `poi_layer.dedup_exact_drops` id; keep its `keep` id (same parent+name+coords).
2. **Retag (38).** Re-parent each `poi_layer.retag_identity` POI `from` → `to`: the POI name carries a
   *different* in-scope city's own name and is geometrically closer to it. (e.g. Mykonos POIs under Paros;
   the whole Riviera — Nice/Cannes/Antibes — under Monaco; Doha POIs under Manama and vice-versa; Hurghada↔
   Sharm; Dar es Salaam under Zanzibar; Casablanca under Agadir; Kilifi/Diani under Mombasa.) Re-home route
   endpoints with the POI.
3. **Drop junk/artifact (19).** Remove each `poi_layer.junk_drops` id — retail/tour-operator (coffee,
   trading, boat-rental, hostel, dive-club) **and cross-border corridor pointers/endpoints** ("Dubai Marina
   (Dubai) — cross-border Quanta-LR endpoint" under Doha, "Sharm El Sheikh … (POINTER, cross-border)" under
   Jeddah, "Kos Marina — Cross-border Pioneer pier" under Rhodes, ASRY yard pointer). These are strategy
   endpoints, not parent-city boarding points — same class as the UAE corridor-endpoint artifacts.
4. **Locale layer.** DROP the 5 `locale_layer.drop` ids (combined/inland artifacts: "Al Khor / Ras Laffan",
   "Doha Corniche / West Bay / Old Doha Port", "NEOM / Sindalah", "Thuwal / KAUST proximity", "Bahrain F1 /
   Sakhir (inland)"). KEEP the 6 `locale_layer.keep` (single placeable waterfronts: Katara, Lusail,
   The Pearl-Qatar, Manama waterfront, Sharm Naama/Sharks Bay, NEOM coast ref).
5. **Residual gate (you own this).** Apply the **51 `review_name_only`** items (name carries another city
   but geometry not corroborating) plus the bulk geometric nearest-city retag, water-adjacency, and fuzzy
   near-duplicate merge. **0 silent drops:** every in-scope POI ends keep / retag / dedup / drop-with-reason.

## Permanent guardrail (add to seal rules)
A row becomes a `locale` pin only if (1) same country as parent, (2) single placeable waterfront place,
(3) not a routing artifact (`via | cross- | "+" | top-level "/" between city names | pointer | endpoint`).
A POI's `parent_city_id` must be the nearest in-country city whose name it carries — never the regional
flagship by default. Cross-border pointer/endpoint rows stay route edges / strategy text, never POIs.

## Acceptance gate (QA report must show)
- POIs: 16 dedup + 38 retag (endpoints re-homed) + 19 junk/artifact applied; 51 review + residual resolved
  with counts (kept / retagged / merged / dropped+reason); before→after in-scope total (2258 → ~).
- No in-scope POI parented to a city it does not name; Riviera/Doha/Sharm/Dar mis-parents resolved.
- Locales: 6 keeps render, 5 drops gone from `locale[]` + `CLUSTERS.json` + briefs; no locale pin >40 nm
  from parent or naming a foreign country.
- Sovereign NEOM / Red Sea Global / AMAALA / Sindalah untouched.
- Guardrail active; land-crossing = 0; every surviving POI carries a source id.
