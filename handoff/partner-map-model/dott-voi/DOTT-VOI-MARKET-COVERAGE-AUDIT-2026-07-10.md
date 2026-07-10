# Dott & Voi market coverage audit

**Audit date:** 10 July 2026  
**Atlas source:** `8adf384da2214629b8b672b897fcd91011d3040d`  
**Status:** Research-complete / source and rendering fixes needed

## Executive finding

Jaideep’s instinct is correct: this is **not primarily a shortage of routes**. The current Dott and Voi pages have two simultaneous faults:

1. **Undercoverage:** the partner build removes many canonical routes that already exist in supported markets.
2. **Scope leakage:** old city lists activate countries where the partner does not currently operate.

The screenshots are reproducible from current `main`: **Dott emits 430 routes and Voi 374**. But only **268 Dott routes** and **184 Voi routes** sit inside the partners’ current, officially supported country footprints. The remaining totals include stale or unsupported markets.

| Partner | Current official directory | Canonical routes in supported Atlas clusters | Supported routes emitted | Inheritance | Stale/unsupported routes emitted |
|---|---:|---:|---:|---:|---:|
| Dott | 18 named countries · 380 listed service areas | 1,430 | 268 | **18.7%** | **162** |
| Voi | 13 countries · 133 listed service areas | 427 | 184 | **43.1%** | **145**, plus 45 UAE expansion routes |

Dott separately reports “20 countries / 400+ cities” in Q1 2026, but its current named directory exposes only 18 countries and 380 service-area entries. The two unnamed countries must remain unresolved rather than guessed.

## Direct answers

### Are Dott or Voi currently in Lebanon?

**No current official evidence supports either partner operating in Lebanon.**

- Lebanon is absent from Dott’s current location directory and explicit help-country list.
- Lebanon is absent from Voi’s complete 13-country current directory.
- Both partner scopes nevertheless contain the stale city key `beirut-lebanon`.
- The current build consequently emits **four Lebanon routes for Dott and four for Voi**.

Lebanon should be removed from both current footprints. This is a stale-scope defect, not a new-market opportunity supported by partner evidence.

### Are the UK, Nordics, Belgium, Germany and northern France missing?

**Yes, but for different reasons.**

- **UK:** already has 64 canonical routes, but only 32 render for each partner. The route-display layer is dropping half of the existing set. Atlas also lacks many partner-exact waterfront cities, so the UK needs both an inheritance repair and registry expansion.
- **Nordics:** Norway has 86 canonical routes but only 13 render; Finland has 31/24; Denmark 4/2. Voi’s 20 Swedish routes all render. The Nordics are therefore partly a display bug and partly a thin-registry problem.
- **Germany:** all 15 existing canonical German routes render. The weak appearance is because Atlas currently represents Germany mainly through Hamburg; it does not yet reflect the partners’ much broader waterfront footprint.
- **Belgium:** both partners currently operate there, but Atlas has no Belgian cluster or canonical routes. This is a true registry/geometry gap.
- **Northern France:** Voi currently names **Le Havre** and has a live official city page, but Atlas has no Le Havre/Seine-estuary market. Dott’s current directory does **not** name a northern-France service area; do not add Lille, Dunkirk, Calais or Le Havre as current Dott operations without new evidence.

## Why existing routes disappear

The build currently activates a legacy density policy whenever a page exceeds 40 routes. It then:

- caps intra-city routes even on inherited partner hubs; and
- runs a second legacy filter that removes lower-tier local routes.

This conflicts with the permanent inheritance rule:

`partner routes = global canonical routes ∩ partner clusters`

Density should change visual emphasis, opacity or default zoom—not remove canonical geography from a partner page.

A second defect compounds the issue: the hub scope generator unions old `_map_scope.cluster_city_ids` into the current scope. Those stored arrays include markets such as Beirut, Egypt, Croatia and Portugal for both partners, even when current partner evidence does not support them.

## Existing Atlas coverage that should inherit now

### Dott

| Supported market | Canonical routes | Current routes | Missing now |
|---|---:|---:|---:|
| UAE | 597 | 48 | 549 |
| Greece | 239 | 37 | 202 |
| Saudi Arabia | 184 | 16 | 168 |
| Norway | 86 | 13 | 73 |
| France, including Riviera cluster | 62 | 7 | 55 |
| Italy, including Bay of Naples cluster | 108 | 57 | 51 |
| UK | 64 | 32 | 32 |
| Spain | 29 | 14 | 15 |
| Netherlands | 8 | 0 | 8 |
| Finland | 31 | 24 | 7 |
| Denmark | 4 | 2 | 2 |
| Germany | 15 | 15 | 0 |
| Israel | 3 | 3 | 0 |

Switzerland is officially supported but its existing cluster has **zero canonical routes**, so it needs geography work rather than an inheritance toggle.

### Voi

| Supported market | Canonical routes | Current routes | Missing now |
|---|---:|---:|---:|
| Norway | 86 | 13 | 73 |
| France, including Riviera cluster | 62 | 7 | 55 |
| Italy, including Bay of Naples cluster | 108 | 57 | 51 |
| UK | 64 | 32 | 32 |
| Spain | 29 | 14 | 15 |
| Netherlands | 8 | 0 | 8 |
| Finland | 31 | 24 | 7 |
| Denmark | 4 | 2 | 2 |
| Germany | 15 | 15 | 0 |
| Sweden | 20 | 20 | 0 |

Voi’s UAE/Dubai material is an **expansion opportunity**, not a current-operation claim. The official Voi directory does not include the UAE. The current proposal labels the UAE as expansion; that distinction must be retained.

## Stale markets to remove from current scope

### Dott stale scope clusters

`bahrain`, `cyprus`, `dalmatia-croatia`, `egypt`, `estonia`, `ireland`, `lebanon`, `monaco`, `morocco`, `portugal`, `qatar`, `romania`, `sweden`

Dott explicitly reports exiting **Qatar and Sweden** during 2025. Those should not survive through old location keys.

### Voi stale scope clusters

`cyprus`, `dalmatia-croatia`, `egypt`, `estonia`, `greece`, `ireland`, `israel`, `lebanon`, `monaco`, `morocco`, `portugal`, `romania`, `saudi-arabia`

The UAE is not in Voi’s current operating footprint but is retained separately as an explicitly labelled proposal expansion.

## Registry and corridor gaps to plug

These are not candidates for invented routes. They require exact city binding, real boarding points and globally canonical corridors before display.

### Priority 1 — large, exact partner overlap

- **Belgium:** Dott names Brussels, Ghent, Liège and Charleroi among its current areas; Voi names Antwerp and Brussels. Atlas has no Belgian cluster/routes.
- **Northern France / Seine estuary:** Voi has exact current evidence for Le Havre. Add only after real waterfront nodes and corridors are sourced.
- **UK depth:** Voi has 21 current areas and Dott 10. Highest marine relevance includes the Solent/Portsmouth–Southampton–Isle of Wight area for Voi, Scotland/Firth of Clyde overlap, and Bristol/Bath/Severn opportunity for Dott. Existing London, Liverpool and Clyde geography is too thin to represent the official footprints.
- **Germany depth:** existing Hamburg routes are working, but both partners support additional coastal/river cities such as Kiel, Lübeck, Rostock, Flensburg and Berlin; Rhine/Ruhr opportunities also need exact geometry review.
- **Norway depth:** current Atlas routes are abundant but the city registry remains narrow relative to Voi’s 19 current areas and Dott’s named operations. Exact coastal candidates include the partners’ sourced official rows around Oslo, Bergen, Stavanger, Trondheim and southern/coastal Norway.

### Priority 2 — existing-country expansion and missing local geometry

- **Netherlands:** existing Atlas cluster has eight routes but is absent from both scopes. Turn on country-supported inheritance first; then assess exact partner cities.
- **Switzerland:** existing cluster has no routes. Voi’s Nyon evidence supports a Lake Geneva priority; Dott’s listed Swiss footprint also points to Rhine/Lake Zürich/Lake Constance research.
- **Finland and Denmark:** inherit the complete existing sets, then deepen beyond Helsinki and Copenhagen where exact partner rows justify it.
- **Poland:** Dott has 85 current directory entries, including Baltic/coastal areas. Atlas has no Polish cluster; this is a substantial Dott-only registry opportunity.
- **Austria and Hungary:** current partner rows create Danube/lake candidates, but Atlas has no suitable clusters. Keep all route IDs and economics null until sourced and sealed.

## Required fix sequence

1. **Fix inheritance at the renderer:** for partner hub pages, select routes by canonical `cluster_id` membership and ship the entire inherited set. Use visual styling—not route deletion—for density.
2. **Clean the source scopes:** remove stale legacy city arrays and store only canonical, evidence-supported cluster membership. Retain Voi UAE solely as an explicit expansion case.
3. **Activate existing supported clusters:** Netherlands and the omitted Italy/Spain subclusters for both partners; Switzerland as a visible market only after its zero-route state is handled honestly.
4. **Rebuild and verify:** Dott and Voi must each satisfy exact set equality against `ROUTES.json ∩ partner.clusters`; no Lebanon routes; no unsupported country leakage.
5. **Expand the registry:** Belgium, Voi Le Havre, broader UK/Germany/Nordics, Poland, Switzerland and the Austria/Hungary water networks—source first, then global mint/bind.
6. **Keep economics separate:** display coverage may grow from existing geometry; no economics should be promoted without sourced demand/fare evidence and sealed route IDs.

## Acceptance checks

- Dott and Voi each pass route-set equality by canonical route ID.
- Shared clusters produce identical route sets across partners.
- Dott and Voi each emit **zero Lebanon routes**.
- Dott emits zero current-scope Qatar and Sweden routes.
- Voi emits zero unsupported current-operation routes; UAE remains clearly marked expansion.
- Netherlands inherits its existing eight canonical routes for both partners.
- No country/city claim is inferred from a route alone.
- All new-country route IDs remain `null` until global geography is sealed.

## Sources and durable evidence

Primary official sources:

- Dott current locations: <https://ridedott.com/locations/>
- Dott FY2025 report and exit disclosure: <https://ridedott.com/wp-content/uploads/2026/03/dott-q4-and-fy-2025-financial-report.pdf>
- Dott Q1 2026 aggregate disclosure: <https://ridedott.com/press-release/q1-2026-financial-report/>
- Voi current locations: <https://www.voi.com/city>
- Voi Le Havre: <https://www.voi.com/city/le-havre>

Supporting artifacts are stored beside this audit: full source ledgers, current-output route parity, and the exact gap queue. Unsupported values remain null. No new route IDs, boarding points, demand, fares or economics were invented.
