# DiDi AU/NZ exact-ID + current-operations gate — 2026-07-10

**Status:** research-complete / mixed gate: 5 city passes, 2 current-operation holds; seal-needed  
**Repo commit:** `d3817d9ec767a9c66a6469daaf324db9bba5ade6`  
**Repository edits:** none

## Gate result

- **No-shrink: PASS.** All 7 existing DiDi AU/NZ city IDs remain in both partner surfaces; no city was dropped or added.
- **Current operation:** 5 exact official city passes; 2 holds (Whitsundays/Airlie Beach and Bay of Islands).
- **Exact candidate route match:** 1/10 (`rn-aa439fa75f13`, Queens Wharf–Days Bay); the other 9 keep `route_id=null`.
- **Demand gate:** 0/10 candidates have route-level `annual_one_way_pax`; no finance promotion.
- **Kotor/New Zealand defect:** New Zealand contamination is resolved: 0 Kotor rows under `new-zealand`; all 10 are currently stamped `montenegro`. **Global cleanup remains:** their endpoint labels require exact country/city revalidation.

## Current DiDi operation by Atlas city

| Atlas city ID | Cluster | Verdict | Evidence | Publication class |
|---|---|---|---|---|
| `brisbane-australia` | `australia` | `pass_current_city_supported` | S01 | display-ready exact existing |
| `gold-coast-australia` | `australia` | `pass_current_city_supported` | S01 | display-ready exact existing |
| `sydney-australia` | `australia` | `pass_current_city_supported` | S01 | display-ready exact existing |
| `whitsundays-australia` | `australia` | `hold_not_currently_verified` | S01 | country/city-supported inherited existing + current-operation hold |
| `auckland-new-zealand` | `new-zealand` | `pass_current_city_supported` | S02, S27 | display-ready exact existing |
| `bay-of-islands-new-zealand` | `new-zealand` | `hold_not_currently_verified` | S02 | country/city-supported inherited existing + current-operation hold |
| `wellington-new-zealand` | `new-zealand` | `pass_current_city_supported` | S02, S28 | display-ready exact existing |

> Endpoint rule: terminal availability is not independently proven. Endpoints inherit only the city verdict; no DiDi service-area polygons were found.

## Atlas reconciliation

- Exact clusters: `australia`, `new-zealand`.
- Exact city IDs: 7/7.
- BP identity audit: 3 exact existing IDs, 17 seal-needed existing IDs, 1 true registry gap (Opua vehicle-ferry landing), 3 non-BP/reject. After current-operation overlay: 2 display-ready, 11 seal-needed, 7 current-operation holds, 1 gap, 3 reject.
- Matching `atlas-external/boarding-points` files: 0.
- Canonical briefs: 4/4 Australian city briefs; 2/3 New Zealand city briefs. Wellington city brief and both cluster briefs are missing.

## Candidate corridor gate

| Candidate | City | Route ID | Classification | Current-op overlay |
|---|---|---:|---|---|
| UQ St Lucia – Northshore Hamilton | `brisbane-australia` | `null` | seal-needed existing IDs | pass |
| Circular Quay – Manly | `sydney-australia` | `null` | seal-needed existing IDs | pass |
| Sea World – Surfers Paradise | `gold-coast-australia` | `null` | seal-needed existing IDs | pass |
| Port of Airlie – Daydream Island | `whitsundays-australia` | `null` | seal-needed existing IDs + current-operation hold | hold |
| Port of Airlie – Hamilton Island Marina | `whitsundays-australia` | `null` | seal-needed existing IDs + current-operation hold | hold |
| Downtown Auckland – Devonport | `auckland-new-zealand` | `null` | seal-needed existing IDs | pass |
| Downtown Auckland – Waiheke Island | `auckland-new-zealand` | `null` | seal-needed existing IDs | pass |
| Paihia – Russell | `bay-of-islands-new-zealand` | `null` | seal-needed existing IDs + current-operation hold | hold |
| Queens Wharf – Days Bay | `wellington-new-zealand` | `rn-aa439fa75f13` | display-ready exact existing | pass |
| Queens Wharf – Matiu/Somes Island | `wellington-new-zealand` | `null` | seal-needed existing IDs | pass |

Nearby/duplicate route rows are recorded only in the JSON and are **not stamped**. Exact route identity requires endpoint BP-ID equality; no fuzzy name match was used.

## Kotor/Montenegro recheck

The prior JSON defect ledger identified ten `ics-*` rows as stamped to New Zealand. Current `ROUTES.json` removes all ten from New Zealand and stamps them `cluster_id=montenegro` / `kotor-montenegro`. That fixes the New Zealand contamination but is not final global geography: five rows name Cavtat/Mlini/Lokrum (Croatia labels), while the other five still need exact Montenegro city review:

- `ics-327dfe7c55` — Mlini Harbour → Lokrum Island Ferry (6.2 nm)
- `ics-4fe80c09ba` — Cavtat Harbour → Lokrum Ferry (5.9 nm)
- `ics-8aaa6c73a6` — Jedrilicarski Klub Delfin → Portonovi Marina (4 nm)
- `ics-b14813cbf4` — Dukley Marina. → Bar Marina (16.5 nm)
- `ics-b793b9cdae` — Mlini Harbour → Lokrum Ferry (4.9 nm)
- `ics-c9153f090d` — Cavtat Harbour → Lokrum Island Ferry (7.2 nm)
- `ics-ddac6d7754` — Jedrilicarski Klub Delfin → Pristaniste Perast (2.9 nm)
- `ics-dea3ec2a3a` — Bay of Kotor → Bay Of Kotor (2.7 nm)
- `ics-ed2acdc803` — Jedrilicarski Klub Delfin → Our Lady of the Rocks (2.8 nm)
- `ics-ff95471dba` — Cavtat Harbour → Mlini Harbour (3.7 nm)

Required global follow-through:
- Mark the **New Zealand contamination** resolved and regenerate cached New Zealand counts/maps.
- Revalidate all ten endpoint labels/coordinates and assign exact country/city IDs; retag, split or quarantine globally as evidence requires. Do not treat blanket `kotor-montenegro` restamping as final.
- Remove the stale ten `rn-*` references from the old Markdown status; none exists in current `ROUTES.json`.
- Retain a route-cluster/endpoint consistency validator and global corridor inheritance gate.

## Key Grok seal actions

1. Preserve all 7 city IDs and inherited cluster scope; do not hand-list DiDi-only corridors.
2. Apply city-supported current-operation labels to Brisbane, Gold Coast, Sydney, Auckland and Wellington. Keep Whitsundays and Bay of Islands inherited but on current-operation hold.
3. Seal straightforward aliases; dedupe Sydney (Circular Quay/Manly), Whitsundays (Port of Airlie/Daydream), Auckland (Downtown/Devonport/Matiatia) and Bay of Islands (Paihia/Russell).
4. Create Opua vehicle-ferry landing only after official coordinate/platform confirmation; do not repurpose Opua marina/club POIs.
5. Retain exact global route `rn-aa439fa75f13`; keep all other proposed route IDs null until deterministic seal.
6. Validate the Matiu/Somes route as a via-Days-Bay service rather than implying an unsupported direct timetable leg.
7. Create partner-neutral Australia/New Zealand cluster briefs and Wellington city brief; enhance existing briefs with URLs/dates and exact IDs.
8. Hold finance cascade until route-level annual passenger evidence exists.
9. Complete global country/city revalidation for the ten former New Zealand mis-stamps; never patch these in DiDi-only scope.

## Unresolved blockers

- **Ten former New Zealand mis-stamps remain blanket kotor-montenegro city assignments despite Croatia/other Montenegro endpoint labels.** Owner: Global Atlas geography steward. Next: Validate label/coordinate provenance, assign exact country/city IDs, and retag, split or quarantine globally; never patch in a DiDi-only scope.
- **Two current-operation holds: Whitsundays/Airlie Beach and Bay of Islands.** Owner: DiDi partnership lead. Next: Obtain written/current DiDi service-area boundary confirmation; app availability and old launches are not sufficient.
- **Nine candidate corridors lack an exact endpoint-ID route match.** Owner: Grok / Atlas geometry. Next: Resolve BP aliases/duplicates, then exact-match or seal globally with hand-waypoint and land-crossing QA.
- **Opua vehicle-ferry landing is a true BP registry gap.** Owner: BP researcher + Grok. Next: Source official landing coordinate/platform and mint once with provenance.
- **Route-level annual passenger totals are absent for all candidates.** Owner: Finance research. Next: Obtain regulator/operator route boardings; keep annual_one_way_pax null otherwise.
- **Schedules/seasonality are not frozen for Hopo, Whitsundays, Bay of Islands and Matiu.** Owner: Operations research. Next: Archive dated timetables, count service days/departures and record seasonal restrictions before utilization modeling.
- **Australia and New Zealand cluster briefs and Wellington city brief are absent.** Owner: Atlas content. Next: Add partner-neutral briefs with claim-level URLs/dates and canonical IDs.
- **No matching external BP research files in repository.** Owner: Atlas data steward. Next: If external BP inputs are restored, reconcile every on-disk BP to sealed POI or reasoned drop; zero silent drops.

## Source highlights

- DiDi Australia current availability: https://web.didiglobal.com/au/help-center/where-is-didi-available/
- DiDi New Zealand current city list: https://web.didiglobal.com/nz/driver/cities/
- DiDi Auckland live city page: https://web.didiglobal.com/nz/driver/cities/auckland/
- DiDi Wellington live city page: https://web.didiglobal.com/nz/driver/cities/wellington/
- Full 36-entry source ledger (official transport/operator/airport/tourism + commit-pinned repo sources) is in the JSON.

## Validation

- JSON round-trip parse: PASS.
- Invariants: 7 cities; 24 BP records; 10 corridors; exactly 1 non-null route ID; all candidate and demand-record `annual_one_way_pax` values null; no scope shrink.
