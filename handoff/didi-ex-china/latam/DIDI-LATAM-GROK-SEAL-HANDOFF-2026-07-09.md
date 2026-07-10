# DiDi Latin America — deterministic Grok seal handoff

**Research as of:** 2026-07-09  
**Revised:** 2026-07-10T02:57:33Z  
**Scope:** Waves A1, A2, B and C only: Brazil, Colombia, Costa Rica, Panama, Dominican Republic, Ecuador, Peru, Chile and Argentina. **Mexico is excluded** because its T3/G4 handoff is separate.

## Mandate and state rules

This is an input to a future seal, not evidence that a seal already happened.

1. Use only exact canonical IDs supplied below. Do not fuzzy-match, synthesize, rename or silently drop an ID.
2. A route being present in `ROUTES.json` and correctly cluster-stamped proves **exact existence**, not BP seal, geometry approval, partner binding, current operation or render approval.
3. Under the pinned current-main rules, an active global canonical/renderable route must have `_quarantine != true` and `relevance != "hide"`. Quarantine/hidden records remain stamped inventory but are excluded from global canonical/rendered sets.
4. Corridors belong to geography. Write approved geometry once to the global graph. Derive the DiDi view as `active global canonical routes ∩ approved cluster/city scope`. Never create partner-only geometry. Featured/wow routes may only be subsets of the inherited active set.
5. Preserve no-shrink at the exact-record/ID layer. Do not activate a hidden record without source, BP, geometry and policy approval. Return a reasoned before/after disposition for every changed route state.
6. Do not invent BPs, coordinates, operation claims, fares or demand. Broad tourism, airport, attraction, hotel, whale, cruise and metro counts are not route demand. All 49 `annual_one_way_pax` values remain null unless a new route-level source is attached and separately approved.
7. Do not run the finance cascade in this seal. Exact route existence does not make a market cascade-ready.

## Pinned inputs

- Snapshot: `/tasklet/agent/home/didi-ex-china-audit/repo-snapshot/`
- Scope ledger: `/tasklet/agent/home/didi-ex-china-audit/DIDI-SCOPE-LEDGER-2026-07-09.json`
- Audit plan: `/tasklet/agent/home/didi-ex-china-audit/DIDI-EX-CHINA-COVERAGE-AUDIT-AND-BUILD-PLAN-2026-07-09.md`
- No-shrink baseline: `/tasklet/agent/home/didi-ex-china-audit/handoff/DIDI-P0-NO-SHRINK-BASELINE-2026-07-09.json`
- Route defect ledger: `/tasklet/agent/home/didi-ex-china-audit/handoff/DIDI-ROUTE-STAMP-DEFECT-LEDGER-2026-07-09.json`
- Exact-ID receipt: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-LATAM-EXACT-ID-RECHECK-2026-07-09.json`
- Research control: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-LATAM-RESEARCH-CONTROL-2026-07-09.json`

Pinned snapshot Git SHAs:

- `CLUSTERS.json`: `01121728865b7b9d9e729bcf960179de599061d7`
- `ROUTES.json`: `6338a446635ac5665b9075a0ac6e562d0915cee5`
- DiDi partner JSON: `a125343df2b85067ebb9e7575252dbb9293a1a47`
- Finance `corridors.json`: `90c333a829c0bf7637756dcc9ed78c86235968e8`

The exact-ID receipt passes 15 existing city IDs, four explicitly referenced cluster IDs and 19 non-null route references with valid endpoints. Of those 19 references, 15 are active/renderable under current exclusion rules and four are quarantine/hidden. This PASS is not a seal receipt.

## Current-main route-state truth to preserve in the handback

| Cluster | Stamped / exact-existing | Active / renderable now | Excluded quarantine/hidden |
|---|---:|---:|---:|
| `brazil` | 59 | 59 | 0 |
| `colombia` | 15 | 14 | 1 |
| `costa-rica` | 67 | 65 | 2 |
| `panama` | 47 | 47 | 0 |
| `dominican-republic` | 32 | 29 | 3 |
| `galapagos-ecuador` | 3 | 0 | 3 |
| `peru` | 12 | 12 | 0 |
| **Total** | **235** | **226** | **9** |

The 46 foreign Galápagos stamps from the stale audit are absent. `rn-f0a756c7f278` is stamped `peru`. These are stamp-cleanup facts only; neither proves a completed route seal or render approval.

---

## Wave A1 — Brazil + Colombia

### Inputs

- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-BRAZIL-COLOMBIA-DEEPENING-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-BRAZIL-COLOMBIA-STATUS-2026-07-09.md`

### Required registry, BP and route actions

1. Preserve `brazil` and `colombia` plus their stamped inventories. The pinned before-state is Brazil 59 stamped/59 active and Colombia 15 stamped/14 active. Only active records may enter canonical/rendered inheritance.
2. Reconcile all 17 researched BP/POI records: ten verified BPs, five coordinate/source candidates and two non-BP POIs. Every record must seal, hold or drop with a reason; zero silent drops.
3. Revalidate the five exact-existing priority routes through BP identity, source, boardability, geometry, endpoint and render gates. Their existence is not prior seal completion.
4. Keep six candidate `route_id` values null unless all promotion gates pass. Keep Barranquilla Río-Bus future-only. Keep canonical city briefs partner-neutral.

### Route-stamp verification

- No A1 priority ID is mis-stamped in the pinned snapshot; verify rather than assume seal completion.
- Colombia record `rn-3d69b89a7af6` is quarantine/hidden and must not render unless Grok returns explicit qualification evidence and a state-change reason.
- `rn-cee507485c05` is a Panama-stamped San Blas–Cartagena cross-cluster record. Visibility must follow approved active global scope, never a DiDi-only Colombia copy.

### Exact IDs to preserve

- Clusters: `brazil`, `colombia`
- Cities: `angra-dos-reis-ilha-grande-brazil`, `florianopolis-brazil`, `rio-de-janeiro-brazil`, `cartagena-colombia`, `barranquilla-colombia`
- Priority route records: `rn-1886629dbf0c`, `rn-80f0d0ebe0bd`, `rn-00bb6ded4be5`, `rn-369ef0eb69d9`, `rn-aa790551baa7`

All five priority records are active in the pinned snapshot, but still require this handoff's BP/geometry/partner/render checks.

### Nulls to preserve

- Six candidate `route_id` values: three Brazil and three Colombia.
- All 18 `annual_one_way_pax` values.
- Unverified BP coordinates/source bindings and unsupported local-service claims.

### Acceptance checks

- Exact IDs and endpoints survive with zero invalid references.
- Handback reports Brazil 59/59/0 and Colombia 15/14/1 as the before-state, then gives explicit post-seal stamped/active/excluded counts and a reason for any delta.
- Render QA tests the approved active set only; it must not claim that all 15 Colombia-stamped records render.
- All 17 BP/POI records have sealed/held/dropped outcomes and reasons.
- No 99 city-level claim for Angra, no current Río-Bus claim and no broad count allocated to a route.

### Handback receipt fields

Wave, Git commit/gold tag, pre/post hashes, preserved IDs, stamped/active/excluded route counts per cluster, excluded route IDs/reasons, BP sealed/held/dropped counts and reasons, null-route dispositions, operation caveats, inheritance result and render anchors/screenshots.

---

## Wave A2 — Costa Rica + Panama + Dominican Republic

### Inputs

- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-COSTA-RICA-PANAMA-DOMINICAN-DEEPENING-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-COSTA-RICA-PANAMA-DOMINICAN-STATUS-2026-07-09.md`

### Required registry, BP and route actions

1. Preserve `costa-rica` / `nicoya-papagayo-costa-rica`, `panama` / `san-blas-panama`, and `dominican-republic` / `samana-dominican-republic`.
2. Reconcile all 123 baseline BP IDs with no shrink: 39 Costa Rica, 48 Panama and 36 Dominican Republic. Reconcile the additive Sabana de la Mar candidate separately; its BP ID and coordinates remain null pending authority/operator proof.
3. Revalidate all ten exact-existing priority routes. Keep Cartí–Colón null and non-publishable. Existing route IDs do not prove service, fare or boardability.
4. Preserve the stamped inventories, but derive/render only the active sets: Costa Rica 67 stamped/65 active, Panama 47/47, Dominican Republic 32/29.

### Route-state verification

- Costa Rica exclusions: `rn-8e6faf8a79cd`, `rn-47e93bfb7d7b`.
- Dominican Republic exclusions: `rn-dc5887c587f3`, `rn-60740d4c3114`, `rn-699787624fc1`.
- `rn-60740d4c3114` is one of the ten exact-existing priority IDs but is quarantine=true and relevance=hide. Preserve its ID and excluded state unless all activation gates pass; do not render it merely because it exact-matches.
- No Cartí–Colón ID may be minted from this research file.

### Exact IDs to preserve

- Clusters: `costa-rica`, `panama`, `dominican-republic`
- Cities: `nicoya-papagayo-costa-rica`, `san-blas-panama`, `samana-dominican-republic`
- Routes: `rn-1efe26f3c0f4`, `rn-21a0133c6d5c`, `rn-55b63e976bb7`, `rn-60740d4c3114`, `rn-64effc46b976`, `rn-7e59f984abec`, `rn-87eec178e86f`, `rn-8fb072f5a8a8`, `rn-c3a4ef933700`, `rn-eb4ca32edbef`

Pinned state: nine of these priority records are active; `rn-60740d4c3114` is excluded.

### Nulls to preserve

- Cartí–Colón `route_id`.
- Sabana de la Mar candidate BP ID and coordinates.
- All 12 `annual_one_way_pax` values.
- Local DiDi service at Papagayo/Nicoya terminals, Cartí/Guna Yala and Samaná until directly proven.

### Acceptance checks

- 124 BP records reconcile to explicit sealed/held/dropped outcomes, including all 123 baseline IDs and the additive candidate.
- All ten exact IDs remain valid; the excluded priority route does not render without an approved state transition; Cartí–Colón remains null unless independently sealed.
- Handback reports the 67/65/2, 47/47/0 and 32/29/3 before-state, plus post-seal counts and reasoned deltas.
- Render QA covers only the approved active inherited sets. It must not say the complete stamped sets render.
- Copy retains Liberia gateway overlap, Panama City gateway only, and Dominican country presence without Samaná city support.

### Handback receipt fields

Wave, commit/tag/hashes, preserved IDs, per-market stamped/active/excluded counts and route IDs, BP preservation and outcomes, additive-candidate disposition, exact priority route eligibility, Cartí–Colón null state, operation caveats, inheritance result and render evidence.

---

## Wave B — Ecuador + Peru

### Inputs

- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-ECUADOR-PERU-DEEPENING-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-ECUADOR-PERU-STATUS-2026-07-09.md`

### Required registry, BP and route actions

1. Preserve `galapagos-ecuador` and its four exact city IDs; preserve `peru` and `lima-peru`, `paracas-peru`, `pisco-san-andres-peru`.
2. Reconcile the 12 researched BP/POI records. The wave contains no accepted Atlas BP IDs. Hold DPA San Andrés pending passenger authorization; keep General San Martín rejected as a passenger BP and Ballestas/Palomino as non-landing POIs.
3. Preserve the three exact-existing Galápagos route IDs **as quarantine/hidden records**. Current state is three stamped and zero active/renderable. Do not call them sealed and do not render them without source, BP, protected-area, geometry and policy approval.
4. Keep all four Peru wave candidate `route_id` values null until BP, authority and geometry gates pass.
5. `rn-f0a756c7f278` is an active Peru-stamped reference in the pinned snapshot. Its corrected stamp is hygiene only; independently run BP/geometry/partner/render checks before any seal claim.
6. Bind partner-market content only with visible operation caveats: Galápagos, Paracas and Pisco/San Andrés are not locally proven DiDi service; Lima is the sole city-supported Wave B ID.

### Route-stamp cleanup state

- The stale 46 foreign Galápagos stamps are absent.
- The three genuine member records are stamped `galapagos-ecuador`, but all are `_quarantine=true`, `relevance=hide` and excluded from active canonical/rendered sets.
- `rn-f0a756c7f278` is stamped `peru` with Lima endpoints.
- Do not describe these facts as completed route seal, partner-market binding or render approval.

### Exact IDs to preserve

- Clusters: `galapagos-ecuador`, `peru`
- Cities: `santa-cruz-galapagos-ecuador`, `isabela-galapagos-ecuador`, `san-cristobal-galapagos-ecuador`, `floreana-galapagos-ecuador`, `lima-peru`, `paracas-peru`, `pisco-san-andres-peru`
- Quarantine/hidden Galápagos records:
  - `e__santa-cruz-galapagos-ecuador__puerto-ayora__isabela-galapagos-ecuador__puerto-villamil`
  - `e__santa-cruz-galapagos-ecuador__puerto-ayora__san-cristobal-galapagos-ecuador__puerto-baquerizo-moreno`
  - `e__santa-cruz-galapagos-ecuador__puerto-ayora__floreana-galapagos-ecuador__puerto-velasco-ibarra`
- Peru stamp-cleanup reference: `rn-f0a756c7f278`

### Nulls to preserve

- All 12 researched BP IDs and unresolved coordinates as recorded.
- All four Peru candidate `route_id` values.
- All nine `annual_one_way_pax` values.
- All local DiDi claims except Lima city support; all Callao pier service-area claims remain unverified.

### Acceptance checks

- Before-state is reproduced exactly: Galápagos 3 stamped/0 active/3 excluded; Peru 12/12/0.
- Galápagos has zero foreign stamps and all three genuine IDs remain exact. Any activation is individually source-qualified, reasoned and accompanied by BP/geometry/protected-area/render proof.
- `rn-f0a756c7f278` remains `peru` with Lima endpoints, but handback separately states whether it passed route seal and render QA.
- No General San Martín passenger marker, DPA passenger claim, Ballestas/Palomino landing marker or straight-line protected-area route is published.
- Zero silent BP loss; operation caveats remain visible.

### Handback receipt fields

Wave, commit/tag/hashes, preserved IDs, 3/0/3 and 12/12/0 before-state, post-state and reasoned deltas, each Galápagos route's quarantine/relevance/activation decision, Peru restamp plus independent seal/render result, BP outcomes, four Peru null-route dispositions, operation caveats, inheritance result and render evidence.

---

## Wave C — Chile + Argentina

### Inputs

- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-CHILE-ARGENTINA-REGISTRY-DEEPENING-2026-07-09.json`
- `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-CHILE-ARGENTINA-STATUS-2026-07-09.md`

### Required registry, BP and route actions

1. Treat this as registry research, not canonical data. The pinned snapshot has no Chile/Argentina clusters, canonical cities, BPs or route IDs.
2. Registry owner approves country/cluster hierarchy and promoted marine city labels before minting. Do not mint directly from candidate keys.
3. Candidate city anchors are Chile: Concepción, Puerto Montt, Punta Arenas, Valdivia, Valparaíso, Viña del Mar; Argentina: Bariloche, Buenos Aires, Rosario. Nearby ferry municipalities do not inherit DiDi service without direct proof.
4. Reconcile 22 BP records and ten route candidates. Authority-grade coordinates and hand-routed water-only geometry are prerequisites. Muelle Prat stays excursion-only; Muelle Blanco unverified; Rosario–Isla Sabino Corsi seasonal; Buenos Aires–Colonia requires cross-border review.
5. Write approved routes once to global geography, then derive DiDi scope from approved registry IDs. Never create partner-only Chile/Argentina geometry.

### Route-stamp state

There are no canonical Wave C IDs or stamps to repair. All ten route IDs remain null. After approved mint/seal, run endpoint, quarantine/visibility, inheritance, land-crossing, orphan, range, source and render gates.

### Exact IDs to preserve

None. Every Wave C cluster, city, BP and route ID is intentionally null. Candidate labels and keys are not IDs.

### Nulls to preserve

- Two cluster IDs, all proposed city IDs, BP IDs/coordinates where null, endpoint city IDs and ten route IDs until canonical approval/mint/seal.
- All ten `annual_one_way_pax` values.
- Nearby-municipality service claims, unverified schedules/fares and cross-border deployment claims.

### Acceptance checks

- Registry approval precedes minting; every new exact ID returns with canonical parent and source.
- All 22 BP records receive sealed/held/dropped dispositions with reasons.
- New routes pass water/land-crossing, orphan, range, source, protected-area, quarantine/visibility and render gates.
- DiDi views derive from approved active global scope, not hand-listed corridors.
- Broad counts stay context only; annual route demand remains null.

### Handback receipt fields

Wave, commit/tag/hashes, registry approvals, every minted cluster/city/BP/route ID and parent, route quarantine/relevance/active state, every deferred/rejected candidate and reason, BP/route seal counts, geometry/inheritance/render results, operation caveats and screenshots.

---

## Global acceptance checks

1. Re-run exact-ID validation against the post-seal snapshot: zero invalid city/cluster/route IDs and zero invalid endpoints.
2. Reproduce the pinned before-state of 235 stamped/exact-existing, 226 active/renderable and nine quarantine/hidden records across the seven existing clusters. Return post-state counts and reasoned record-level deltas.
3. No shrink at exact-ID layer: seven existing clusters, 15 city IDs and 19 validated non-null route references remain. Wave C additions require prior approval.
4. Active canonical/rendered sets exclude quarantine/hidden records. No receipt may say full stamped sets render.
5. Partner inheritance passes on the active set: DiDi rendered routes equal active global canonical routes intersected with approved scope; shared clusters remain identical across partners; featured/wow is a strict subset.
6. All 175 researched BP/POI records are sealed, held or dropped with reasons; zero silent drops, ghost endpoints and orphan routes.
7. Geometry/source gates pass: zero disallowed land crossings; every surviving BP has a source; water-only and protected-area checks pass.
8. Evidence tiers and all `do_not_publish` controls survive. Aspirational markets are visibly labeled.
9. All 49 annual one-way demand values remain null unless a new route-level source is attached and separately approved. No finance cascade occurs here.
10. Render QA uses active routes only and provides anchor-city screenshots/URLs. Route existence, correct stamp or partner scope membership alone is not render approval.

## Required Grok handback receipt

Return one machine-readable and one human-readable receipt with:

- UTC timestamp, Git commit, gold tag and pre/post SHA-256 for `CLUSTERS.json`, `ROUTES.json` and DiDi partner JSON.
- Exact preserved IDs by wave; minted Wave C IDs and hierarchy; deferred/rejected ledger.
- Per cluster and per wave: stamped/exact-existing, active/renderable, quarantine/hidden and rendered counts; excluded route IDs/reasons; explicit before→after deltas.
- Each route-stamp repair with before/after cluster and endpoint IDs, plus a separate BP/geometry/seal/render verdict. Specifically prove Galápagos before-state 3/0/3 and `rn-f0a756c7f278`=`peru` without calling either fact a seal.
- BP counts by market: researched, exact-matched, minted, sealed, held and dropped with reasons; pre/post POI totals; zero-silent-drop result.
- Route counts by market: created, exact-preserved, null-held, culled, activated and excluded; land-crossing/orphan/source/protected-area results.
- Partner inheritance and shared-cluster parity results; featured/wow subset result.
- Operation caveats and do-not-publish controls carried forward.
- Render QA URLs/screenshots and exact anchor city IDs tested.
- Finance status: no cascade performed; list new route-level evidence separately or confirm all 49 annual one-way values remain null.
