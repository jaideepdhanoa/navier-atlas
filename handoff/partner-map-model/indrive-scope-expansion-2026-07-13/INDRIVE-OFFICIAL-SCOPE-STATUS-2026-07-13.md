# inDrive official scope status — 13 July 2026

**Status:** research-complete / seal-needed. No repository files were edited and no partner-facing or route/economics claims were made.

## Headline counts

- Official help roster: **49 named countries**, despite the same page saying “approximately 48”; the corporate page also says **48 countries**. Treat the aggregate mismatch as `source_cleanup_needed`.
- Existing baseline: **74 footprint rows** spanning **23 identifiable countries** plus one broad “Sub-Saharan Africa” prose bucket. **23/23 baseline countries are named by the current official roster.**
- Row decisions: **51 approved inherited display candidates**, **8 exact city-supported candidates**, **15 brief-only**, **0 held**, **0 excluded**.
- Atlas reconciliation: **22 approved / 0 candidate / 0 held clusters**.
- Current `CLUSTERS-main.json`: **102 member city IDs** across those clusters, **86 marked present**. The supplied plan instead says **101 registered cities**; reconcile the one-city snapshot difference before implementation.
- Candidate route-count ceiling: **2,382 active canonical routes** from the supplied plan. This was not recomputed because no ROUTES registry was supplied and **is not an approval**. The plan says the current effective 3-cluster scope inherits approximately **342** routes.

## Brazil

**Supported and eligible for country-level inheritance review.** The official Brazil page says inDrive is available in major cities across Brazil and names **Rio de Janeiro** and **Florianópolis**; both also have dedicated official city pages. The existing Brazil Atlas cluster has **3 city IDs**. Therefore:

- Rio de Janeiro: `city_supported` (exact anchor; broader Costa Verde label remains country-supported).
- Florianópolis: `city_supported`.
- Angra dos Reis / Ilha Grande: `country_supported` only; no exact official city page was found in this pass.

The plan's **59-route** Brazil figure is a registry ceiling only, not route or economics approval.

## Egypt

**Supported; preserve existing inheritance.** The official Egypt page says inDrive is available in 30 major cities and names **Cairo, Hurghada and Sharm el-Sheikh**. Each has a dedicated official city page; Hurghada's page also explicitly mentions travel to **El Gouna**. The Egypt Atlas cluster has **4 city IDs**.

Cairo remains distribution context: exact ride-hail support does **not** establish a Cairo marine route. The plan's **179-route** Egypt figure is a registry ceiling only.

## Decision summary

All **22 Atlas clusters** reached by the bound baseline rows sit in countries named by the current official roster, so they pass the country-operation gate for 80:20 inheritance review. This is a research approval/candidate classification, not a map seal. The **15 brief-only rows** are preserved because they are non-promoted, umbrella, dot-only, or alias-cleanup cases; none was removed. No row was excluded for lack of direct contrary evidence.

## Unresolved blockers

1. Official aggregate mismatch: 49 names versus “approximately 48” / corporate 48.
2. Registry snapshot mismatch: current CLUSTERS totals 102 member IDs (86 marked present), while the plan says 101 registered cities.
3. No supplied ROUTES registry, so the 2,382 ceiling and Brazil/Egypt sub-counts were not independently verified.
4. Alias cleanup remains for `al-hoceima`, `casablanca`, `tangier`, and `palawan-philippines__el-nido-bacuit-bay`.
5. Route identity, hidden/quarantined exclusion, seal/render checks and visual QA remain pending.

## Primary sources

- [Official availability help roster](https://indrive.com/en-in/help/about-indrive/where-is-indrive-available)
- [Official corporate scope](https://indrive.com/en-in/company)
- [Official Brazil country page](https://indrive.com/en-br), plus [Rio](https://indrive.com/pt-br/rio-de-janeiro) and [Florianópolis](https://indrive.com/pt-br/florianopolis)
- [Official Egypt country page](https://indrive.com/en-eg), plus [Cairo](https://indrive.com/en-eg/cities/cairo), [Hurghada](https://indrive.com/en-eg/cities/hurghada), and [Sharm El Sheikh](https://indrive.com/en-eg/cities/sharm-el-sheikh)
- [Official Mexico city-rides page](https://indrive.com/en-mx/city-rides)
