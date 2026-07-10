# DiDi × Navier — Australia & New Zealand deepening status

**As of:** 2026-07-09  
**Lane:** BP + brief maturity + demand/fare source research  
**Status:** Research complete with repository-access blocker; BP/geometry and finance sealing still required.

## Atlas baseline

| Cluster | Existing city IDs | Strict routes | POIs | External BP files | Brief coverage |
|---|---:|---:|---:|---:|---|
| Australia | 4 | 92 | 273 | 0 | Cluster brief missing; 4/4 city briefs present per audit |
| New Zealand | 3 | 42 | 173 | 0 | Cluster brief missing; 2/3 city briefs present; Wellington missing |

The New Zealand raw count is **52**, but **10 Kotor/Montenegro routes are mis-stamped into New Zealand** and must be excluded. Affected IDs:

`rn-814e50139d2f`, `rn-f8d63f4a46a6`, `rn-8a3b2a4099b2`, `rn-05d25e61cc48`, `rn-aac7fd6c2037`, `rn-a81957832f0d`, `rn-026c33a86f9b`, `rn-084bc7c5537e`, `rn-12835a796e79`, `rn-fbf2d32941fe`.

## Research output

- **26 official/operator sources**
- **24 BP/POI records:** 20 verified real-world BPs, 1 unresolved BP candidate, 2 non-BP airport POIs, 1 reject/drop
- **10 source-backed candidate corridors**
- **16 demand/fare records**
- All candidate `route_id` values remain `null`
- All route-level `annual_one_way_pax` values remain `null`
- No coordinates were invented

### Priority corridors

1. Brisbane: UQ St Lucia – Northshore Hamilton
2. Sydney: Circular Quay – Manly (F1)
3. Gold Coast: Sea World – Surfers Paradise (Hopo; dated timetable recheck required)
4. Whitsundays: Port of Airlie – Daydream Island
5. Whitsundays: Port of Airlie – Hamilton Island Marina
6. Auckland: Downtown – Devonport
7. Auckland: Downtown – Waiheke (exact landing unresolved)
8. Bay of Islands: Paihia – Russell
9. Wellington: Queens Wharf – Days Bay
10. Wellington: Queens Wharf – Matiu/Somes Island (selected trips; booking/access conditions)

## Verified fare and flow observations

| Market | Observation | Source-use caveat |
|---|---:|---|
| Brisbane | AUD 0.50 per Translink journey, including CityCat/ferry | Fare only; annual route pax unavailable |
| Whitsundays | AUD 49.50 adult Port of Airlie–Daydream | Current operator fare; annual route pax unavailable |
| Whitsundays | AUD 74.50 adult Port of Airlie–Hamilton Island | Current operator fare; annual route pax unavailable |
| Auckland | NZD 7.80 adult HOP/contactless inner-harbour fare | Confirm each route's category before modeling |
| Bay of Islands | NZD 19.40 adult return Paihia–Russell | Three services/operators; schedule freeze needed |
| Wellington | NZD 17 adult one-way Queens Wharf–Days Bay | Dated timetable exists; annual route pax unavailable |
| Whitsundays | 969,000 regional visitors, YE Jun 2024 | **Not ferry demand** |
| Whitsunday Coast Airport | 510,835 passenger movements, YE Dec 2024 | **Not ferry demand** |
| Brisbane Airport | 22.6m passenger movements, FY2024 | **Not ferry demand** |
| Sydney Airport | >41m passenger movements, CY2024 | **Not F1 demand** |
| Gold Coast Airport | >6m travellers per year | **Not Hopo demand** |
| Auckland Airport | 18.7m passenger movements, FY2025 | **Not ferry demand** |
| Wellington Airport | 5,316,858 passenger movements, FY2025 | **Not ferry demand** |

## DiDi availability

Official city pages verify DiDi in **Brisbane, Gold Coast, Sydney, Auckland and Wellington**. Exact DiDi coverage was **not verified** for **Whitsundays/Airlie Beach** or **Bay of Islands**. Keep these as future coverage/adjacency narratives unless DiDi supplies service-boundary confirmation.

## Brief maturity

A semantic field-by-field review could not be completed because `/tmp/navier-atlas` was unavailable and the alternate app path contained only a source-revision placeholder. The fallback audit establishes only coverage/existence:

- Create partner-neutral cluster briefs for Australia and New Zealand.
- Enhance, rather than replace, existing city briefs.
- Create the missing Wellington brief.
- Keep DiDi framing in the partner narrative, outside canonical briefs.
- Separate public urban ferry, tourism ferry and island-transfer archetypes.
- Preserve the distinction between route demand and broad visitor/airport context.

## Blocking next actions

1. Mount the pinned Atlas repository read-only and rerun exact `ROUTES.json`, brief-content and BP-registry parity checks.
2. Purge the ten Kotor route stamps from New Zealand before map/economics publication.
3. Source official coordinates and access/platform tags for all BP candidates.
4. Hand-route all water geometries; river, harbour and island corridors cannot use naïve straight chords.
5. Obtain route-level annual boardings and dated service-day/seasonality tables before finance modeling.
6. Confirm DiDi service-area coverage at ferry endpoints, especially Whitsundays and Bay of Islands.

## Artifacts

- JSON: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-AUSTRALIA-NEW-ZEALAND-DEEPENING-2026-07-09.json`
- Status: `/tasklet/agent/home/didi-ex-china-audit/waves/DIDI-AUSTRALIA-NEW-ZEALAND-STATUS-2026-07-09.md`

JSON validation passed on 2026-07-09.
