---
name: partner-coverage-research
description: Source-led partner market coverage workflow for Navier partner proposals. Use when scanning multi-market partners and binding coastal/waterfront coverage to Atlas.
---

# Partner Coverage Research Playbook

Use this when scanning a rideshare, mobility, travel, hospitality, logistics, or regional platform partner for Navier proposal coverage.

## Core rule

Do not start from the current partner JSON buckets and call the partner “done.” Existing buckets only prove what is already known. A complete pass starts from source-led partner market coverage, then binds to Atlas.

Equally important: do not let a new source scan shrink existing proposal or Atlas coverage. A source page, country page, or scrape is often incomplete. Treat new scans as additive candidate/gap discovery until they have been reconciled against the existing partner JSON, `network_footprint[]`, map scope, seal scope, and registry artifacts. No source omission can delete or demote existing coverage.

## 80:20 inheritance rule for broad partners

For broad mobility/platform partners, do **not** require false city-level precision when credible country/region evidence already establishes partner presence.

If a credible source shows that a partner operates in a country or region, we may attach that partner to **existing Atlas coastal/island/waterfront clusters and cities inside that country/region**, provided that:

1. the Atlas market already exists and has stable hierarchy/geometry support,
2. the partner evidence tier is recorded clearly,
3. no new geography is invented from country evidence alone,
4. the output distinguishes partner evidence strength from Atlas geometry confidence.

Evidence tiers:

| Tier | Evidence | Allowed action |
|---|---|---|
| `country_supported` | Partner operates in the country | Bind partner to existing Atlas coastal/island/waterfront markets in that country; mark as country-supported. |
| `region_supported` | Partner operates in a region/state/island group | Bind to existing Atlas markets inside that region; mark as region-supported. |
| `city_supported` | Partner names the exact city/service area | Bind directly where Atlas ID/alias/provenance matches. |
| `property_supported` | Specific hotel/resort/community/property evidence | Bind specific property-origin opportunity only. |
| `source_cleanup_needed` | Source is stale, partial, scraped poorly, or ambiguous | Keep as research queue/prose until cleaned. |

This is especially important for Uber, Yango, Grab, Lyft, Bolt, inDrive, DiDi, Gojek/GoTo, Ola, Rapido, LINE, and similar broad platforms. We should use country/region evidence to inherit existing Atlas markets; we should not block useful display coverage waiting for city-level proof for every node.

## Completion-status discipline

Do not call coverage **complete** just because a deck, source queue, or Grok prompt exists. Coverage is only **research-complete** when Tasklet has saved source-backed country/city/BP evidence, normalized/bound it against Atlas where possible, classified gaps, and supplied demand/fare assumptions for every in-scope market that is being promoted to economics. Routes remain **seal-needed** until Grok returns deterministic route geometry/IDs/render QA. Economics remain **cascade-needed** until the model/sheet/sidecar files are rebuilt from sealed routes.

When reporting progress, use these labels:
- `research-needed`: Tasklet still owes source-backed city/BP/demand/fare work.
- `research-complete / seal-needed`: Tasklet evidence is done; Grok route/render seal remains.
- `seal-complete / cascade-needed`: Grok seal is done; Tasklet model/sheet/growth/sidecar cascade remains.
- `complete`: proposal JSON, data-clean JSON, route IDs, render QA, economics, sheet, sidecar, and delivery receipts all exist.

If any artifact is missing, explicitly name it and do not use “ready” without a qualifier such as “deck-ready,” “handoff-ready,” or “research-ready.”

## Definition of done

A partner coverage pass is not done until it has:

1. Source-led operating-market inventory at the best available tier: country, region, city, or property.
2. Normalized country / region / city / market names.
3. Atlas inheritance/binding by stable ID, alias, provenance, or country/region containment into existing Atlas hierarchy.
4. Coastal / waterfront relevance triage.
5. Coverage-density classification:
   - no coverage → some coverage,
   - thin coverage → fuller coverage,
   - fuller coverage → marquee/economics-corridor coverage.
6. A clean gap queue for useful markets that still cannot inherit from existing Atlas hierarchy.
7. Clear separation between:
   - display-ready Atlas-bound markets,
   - country/region-supported inherited markets,
   - brief-only markets,
   - registry/geometry backlog,
   - non-marine or inland exclusions.
8. Updated partner proposal artifacts only after the review batch is accepted.

## Search sequence: broad strokes first, precision second

Do not begin with a narrow city-page crawl. For multi-market partners, first establish the rough operating universe in 10-20 minutes, then decide where exact city binding is worth doing.

Fast pass sequence:

1. Existing baseline: load current partner JSON, `network_footprint[]`, map scope, seal scope, and registry map. This is the no-shrink baseline.
2. Broad country/region hypothesis: capture official/about/press/investor/help/app-store/news summary evidence for countries and major regions. This can be coarse and non-city-complete.
3. 80:20 Atlas inheritance: for each supported country/region, enumerate existing Atlas coastal/island/waterfront clusters/cities inside scope and mark them with the appropriate evidence tier.
4. Partner operating model: classify whether the partner is rideshare, super-app, B2B fleet tech, delivery, taxi marketplace, ferry, hotel group, tourism board, etc. B2B tech presence is not the same as consumer operating footprint.
5. Proposal relevance filter: prioritize coastal/island/waterfront countries and existing Atlas-overlap markets; park clearly inland-only markets.
6. Targeted city discovery: only after the country/region hypothesis is set, collect city/service-area rows where it will change a decision or raise a market to marquee/economics-corridor level.
7. Exact bind / inherited bind: map by stable ID, alias, provenance, or country/region containment into existing Atlas registry. Keep everything else as prose/backlog.
8. Save source URLs, confidence, unresolved questions, and failed-source notes so the next pass starts warm.

A fast broad pass is successful if it gets the partner's regional shape right, identifies existing Atlas markets that should be displayed, and prevents false narrowing. It does not need every city.

## Coverage-density promotion lanes

The goal is not only to move partners from **no coverage → some coverage**. We also need a count and queue for markets that should move from **thin coverage → full coverage / marquee level**, especially where multiple candidate partners overlap or economics corridors are likely.

Classify every matched Atlas market/cluster:

| Lane | Meaning | Typical action |
|---|---|---|
| `new_display_coverage` | Partner has no current map presence in a supported Atlas market | Add to partner coverage review. |
| `thin_to_full_coverage` | Market exists for partner but lacks enough routes/cities/proposal depth | Queue for denser cluster/city coverage and better narrative. |
| `full_to_marquee_coverage` | Market already exists but should become a flagship/economics corridor | Queue for economics corridor modeling, richer partner page, route sidecar, and deck treatment. |
| `multi_partner_corridor_candidate` | Same market/corridor appears across several partners | Prioritize as shared registry/economics unlock. |
| `true_registry_gap` | Partner evidence exists but Atlas has no suitable market/geometry | Step 3 registry expansion queue. |

Record counts by partner and by market:

- number of new Atlas markets to promote,
- number of existing thin markets to deepen,
- number of marquee/economics-corridor candidates,
- number of true registry gaps,
- affected partners per market.

## Step 3 gap queue comes after inheritance

Do **not** build the final registry-expansion gap queue directly from raw leftover rows. First run the 80:20 inheritance pass so country/region-supported markets already in Atlas are promoted instead of misclassified as gaps.

Only call something a registry gap when:

1. partner country/region/city/property evidence exists,
2. the market is relevant to Navier,
3. no existing Atlas country/region/cluster/city/property node can support it,
4. alias/normalization review cannot resolve it.

Step 3 should therefore contain true shared registry expansion tasks, not partner-specific fake/nulls forever.

## Source hierarchy

Prefer sources in this order:

1. Existing Navier baseline artifacts for the partner: current proposal JSON, map scope, seal scope, `network_footprint[]`, registry map.
2. Official partner city/location pages, country pages, app service area pages, help-center location pages.
3. Partner annual reports, investor materials, press kits, and official blogs.
4. App-store metadata and broad web/AI summaries for coarse country/region hypotheses only, not city truth.
5. High-quality public market reports or local launch announcements when official pages are incomplete.
6. Avoid generic SEO pages unless no better source exists, and mark confidence accordingly.

## Matching rules

- Exactness where it matters; avoid false precision where country/region evidence is enough.
- ID / alias / provenance match beats fuzzy name match.
- Country/region-supported inheritance is allowed only into existing Atlas hierarchy/geometry.
- Null beats confidently wrong.
- Do not invent cities, corridors, or boarding points.
- Do not add a market to `network_footprint[]` unless it maps to an existing sealed registry key with Atlas hierarchy support.
- Coastal candidates without geometry are proposal brief / backlog, not display-ready map footprint.

## Partner proposal display rule

For partner proposals, display markets from the existing Atlas hierarchy and geometry even if economics are missing. Track economics separately. Economics should not gate display; geometry and registry grounding gate map display.

Use:

- `network_footprint[]` only for registry keys with sealed cluster cities.
- `coverage_note` prose for broader partner reach.
- No separate non-marine footprint card grid.
- Corridor-ready but unsealed markets stay brief-only until green-lit and grounded.

## Hospitality / property-origin partner rule

For hotel, resort, residential-club, and hospitality partners such as Aman, Four Seasons, Six Senses, Discovery Land, and Soneva, do **not** expand them as full country/city operating footprints. Their Navier-relevant route opportunities originate from specific properties: hotels, resorts, clubs, residences, marinas, or waterfront estates.

Use a property-origin workflow:

1. Treat official property/resort/club/location lists as the source inventory, not broad country/city coverage pages.
2. Create or update a property-origin footprint/backlog rather than expanding `network_footprint[]` across every city or country where the brand exists.
3. Exact-bind only where a specific property can be safely associated with an existing Atlas city, cluster, locale, boarding point, or corridor.
4. If a property is coastal/island/waterfront but lacks Atlas-supported geometry, keep it as property-origin backlog, brief-only opportunity, or future BP/corridor candidate.
5. Do not add full country nodes, broad city nodes, or non-property market cards just because the hotel group operates in that country.
6. Proposal language should say “selected property-origin routes,” “resort and marina transfers,” or similar — not “countrywide operating footprint.”

This caveat does not apply to non-hotel partners in the same P2 queue. Rapido remains a mobility partner and LINE remains a non-hotel platform partner; process both through their normal mobility/platform coverage workflows.

## Careem current rule

For the current proposal coverage lane, Careem is UAE-only. Mark it as such and skip further Careem global coverage research unless the user explicitly reopens it.

## Bolt current rule

Bolt has a large official city inventory. Treat it as a country/region rollup first, then inherit existing Atlas coastal/island markets in supported countries/regions. Do not bulk-add all official Bolt cities to Navier map footprint; most will be inland or irrelevant.

Current Bolt workflow:

1. Use official city rows as the source inventory.
2. Roll up by country/region.
3. Apply 80:20 Atlas inheritance for existing coastal/island/waterfront Atlas markets.
4. Prioritize thin-to-full and marquee/economics-corridor markets where Bolt has strong overlap.
5. Queue unbound coastal candidates for registry/alias/geometry work.
6. Exclude inland/non-marine rows.

## Yango current rule

Yango needs aggressive broadening outside GCC, but still under Atlas-grounding rules.

Critical correction: Yango already has a broad existing proposal/map baseline. A partial official-source scan is not the Yango universe and must never reduce current coverage. Before changing Yango, reconcile against `partner-pitch/partners/yango.json`, its `_map_scope`, `network_footprint[]`, and any `map-scope.json::yango`/seal-scope artifact. Treat captured official rows and user-provided regional scope as additive evidence.

Current Yango workflow:

1. Load existing Yango proposal/map baseline first.
2. Capture official country/city pages where possible and preserve user-provided interim country/region seeds.
3. Diff source rows against existing coverage.
4. Apply 80:20 inheritance: country/region-supported Yango scope may activate existing Atlas coastal/island markets inside those scopes, marked as interim/country-supported where needed.
5. Split rows into:
   - already-covered baseline markets,
   - country/region-supported inherited markets,
   - exact-bound additive markets,
   - thin-to-full or marquee/economics-corridor candidates,
   - coastal/waterfront candidates needing grounding,
   - inland/non-marine exclusions,
   - B2B-tech-only / not consumer footprint.
6. For proposals, keep existing display-ready markets live and discuss ungrounded candidates in prose/backlog until grounded.

## Multi-market partner scan order

When multiple partners are active, prioritize:

1. Partners with live proposals or near-term decks.
2. Partners with broad coastal operating footprints.
3. Partners whose official coverage source is structured enough to avoid repeated manual research.
4. Partners with overlap into existing Atlas hierarchy.
5. Markets where multiple partners unlock the same shared registry/economics corridor.

Suggested active order:

1. Lyft and Bolt — structured rows + likely immediate Atlas inheritance gains.
2. Uber, Yango, Grab — country/region-supported inheritance should unlock broad existing Atlas coverage.
3. DiDi, Gojek/GoTo, Ola, inDrive, Cabify, FREENOW, Rapido, LINE.
4. Kakao Mobility and other region-specific platforms.
5. Luxury/hospitality/property-origin partners as proposal demand requires.

## Durable artifacts to save

For each partner or batch, save these under the repo handoff path, not only in chat:

- Raw or structured source inventory JSON.
- Source URL / source type / source confidence per row.
- Normalized row fields: partner, country, region, source market name, normalized city, normalized country, source scope.
- Atlas binding result: registry key, city ID, cluster ID, country tag, match basis, evidence tier, confidence.
- Relevance result: coastal/waterfront candidate, inland/non-marine, country-scope-only, region-scope-only, unknown.
- Coverage-density result: new display coverage, thin-to-full, full-to-marquee/economics-corridor, multi-partner corridor candidate, true registry gap.
- Proposal status: display-ready, inherited display-ready, brief-only, backlog, exclude.
- Gap queue with exact reason and next action.
- Human-readable status markdown.

Recommended filenames:

- `partner-market-coverage-research.json`
- `partner-market-coverage-inheritance-batch.json`
- `partner-market-coverage-density-promotion-queue.json`
- `partner-market-coverage-research-gap-queue.json`
- `partner-market-coverage-proposal-priority-queue.json`
- `partner-market-coverage-{partner}-city-triage.json`
- `partner-market-coverage-{partner}-country-rollup.json`
- `partner-market-coverage-multicluster-scan-control-YYYY-MM-DD.json`
- `partner-market-coverage-p0-no-shrink-baselines-YYYY-MM-DD.json`
- `PARTNER-MARKET-COVERAGE-RESEARCH-STATUS.md`
- `PARTNER-MARKET-COVERAGE-INHERITANCE-STATUS.md`
- `PARTNER-MARKET-COVERAGE-MULTICLUSTER-SCAN-STATUS.md`

## What to bank after every pass

After each partner pass, record:

- Which sources worked and which failed.
- Which source pages are structured enough to reuse.
- Known false-positive traps.
- Alias mappings discovered.
- Coastal market candidates that recur across partners.
- Registry gaps that should become shared routes/cities.
- Thin markets that should be deepened.
- Marquee/economics-corridor candidates.
- Partner-specific scope decisions, such as Careem UAE-only.

## Current repo context

Primary working area:

- `handoff/partner-map-model/`

Important current artifacts:

- `partner-market-coverage-research.json`
- `partner-market-coverage-research-gap-queue.json`
- `partner-market-coverage-proposal-priority-queue.json`
- `partner-market-coverage-yango-city-triage.json`
- `partner-market-coverage-bolt-country-rollup.json`
- `global-inheritance-registry.json`
- `partner-global-registry-map.json`

## Common mistakes to avoid

1. Do not confuse “all existing buckets are bound” with “full partner market coverage is researched.”
2. Do not mistake raw leftovers for true Step 3 registry gaps before the inheritance pass.
3. Do not require city-level proof where credible country/region evidence plus existing Atlas hierarchy is enough.
4. Do not create new geography from broad country evidence alone.
5. Do not ignore thin-to-full and marquee/economics corridor promotion opportunities just because a partner already has some coverage.
