# Grok seal handoff — Dott / Voi enrichment Wave 1

Work from current `main`. Treat the files in this package as research inputs, not pre-approved IDs or geometry. Preserve the corridor-inheritance contract: a route belongs to global geography and partner views inherit the canonical route set by cluster membership.

## Bite 0 — exact-ID repairs first

1. **UK:** decompose/retag the 64 existing `uk` routes into geography-owned water-system clusters while preserving route IDs. Current components are 33 London-only, 18 Liverpool/Mersey and 13 Firth of Clyde. Dott current evidence supports Glasgow but explicitly excludes London and does not establish Liverpool. Voi supports London and Glasgow but not Liverpool. Do not leave either partner on a generic cluster that leaks unsupported cities.
2. **Switzerland:** retag the 14 route IDs listed in the program manifest from `indonesia` to `switzerland`. Their city ID is `lake-geneva-switzerland`. Preserve route IDs and geometry; do not duplicate.
3. **Ibiza:** reuse `ibiza-spain`, its existing brief and its ten visible routes. Normalize terminal aliases only; do not mint duplicate Ibiza–La Savina geometry.

Return a thematic receipt with before/after cluster IDs, route IDs preserved, Dott/Voi route counts and global side effects. Run land/water, orphan, inheritance and partner-copy gates before proceeding.

## Bite 1 — shared Belgium and Switzerland

Use the `be-ch` ledger and handoff. Review proposed IDs; mint only after exact gazetteer/registry checks. Priority is Brussels–Scheldt canal, Basel Rhine and Lake Zürich. Reuse the repaired Lake Geneva graph. Every BP requires sourced coordinates or remains null. Return a 0-silent-drop ledger.

## Bite 2 — UK, Germany and Nordics

Use `uk-de` and `nordics`. Build only marine-relevant water systems. Prefer short domestic legs, exact city IDs, and existing canonical endpoints. Solent/Clyde/Severn, Baltic/Elbe/Rhine-Ruhr, and the high-confidence Nordic systems go first. Do not use a countrywide cluster where it would reintroduce unsupported city leakage.

## Bite 3 — Le Havre, Poland, Austria and Hungary

Use `voi-lehavre-dott-poland` and `dott-at-hu-balearics`. Le Havre is Voi-supported; Dott has no current northern-France evidence. Poland, Austria and Hungary are Dott geography. Voi Vienna is a separate Voi row and must not be used as Dott evidence. Preserve all nulls and BP holds.

## Hard gates after every bite

- `partner routes = visible canonical ROUTES ∩ partner clusters`
- no partner-specific route arrays
- no invented IDs, BPs, coordinates, demand, fares or economics
- 0 land crossings; 0 orphan routes; 0 silent BP drops
- featured/wow routes remain strict subsets of inherited routes
- Dott includes Abu Dhabi and Dubai; Voi has zero MENA scope
- run partner inheritance, finance inheritance and partner-copy validation
- report global and partner before/after route counts by cluster
- commit each thematic bite separately; Jaideep controls merges

## Definition of completion

Wave 1 is complete only when source-backed BPs/cities/clusters/routes are on main, render receipts exist, every held candidate has a reason, and Dott/Voi partner pages show the exact inherited geography without London/Liverpool leakage or Switzerland mis-tagging. Do not change economics in this wave.
