# DiDi × Navier Mexico economics sourcing status

**Market:** Mexico — Pacific + Caribbean  
**As of:** 2026-07-09  
**Status:** **research-needed** — two Caribbean corridor totals and public fare snapshots are source-backed, but no Mexico corridor is yet finance-model-ready.

## What is now grounded

| Corridor / pool | Source-backed fact | Atlas match | Finance treatment |
|---|---:|---|---|
| Playa del Carmen–Cozumel | **3,853,770 passenger movements** and **27,920 ferry departures** in 2025 | `ics-dd1d814699` is the exact visible Ultramar/Winjet route match | Keep `annual_one_way_pax: null`; corridor total has no direction, operator, or observed fare-mix split |
| Puerto Juárez–Isla Mujeres | **5,457,733 passenger movements** in 2025 | `ics-413f51cd44` matches endpoints, but its label is Magna-specific | Keep route allocation and `annual_one_way_pax` null; source is all-operator corridor total |
| Playa–Cozumel public fares | Ultramar Premium Plus adult **MXN 320 one way / 640 round trip**; Winjet adult regular **MXN 310 from Cozumel / 335 from Playa / 645 round trip** | `ics-dd1d814699` | Snapshot only; no weighted realized fare or operator/fare-class mix |
| Puerto Juárez–Isla Mujeres public fares | Ultramar tourist adult **MXN 290 one way / 580 round trip**; Xcaret Xailing adult single **USD 14.50** | No operator-safe allocation | Snapshot only; products, terminals, currencies, resident fares, and mix differ |
| Puerto Vallarta–Yelapa | Current boat-only access and multiple daily water-taxi departures; local fare indication **MXN 350 one way / 550 round trip** | `ics-89a8844858` | Annual ridership and exact BP pair remain null |

Primary route-flow source: Government of Quintana Roo / APIQROO, 8 Jan 2026:  
<https://cgc.qroo.gob.mx/logra-quintana-roo-crecimiento-sostenido-en-la-actividad-maritima-durante-2025/>

## Context pools — not route demand

- **Cancún airport:** 29,345,538 terminal passengers in 2025; **Cozumel airport:** 646,606 (ASUR).
- **Los Cabos airport:** 7,529,900; **Puerto Vallarta airport:** 6,947,700 in 2025 (GAP).
- **Cozumel cruise:** 4,732,250 passengers in 2025; **Cozumel nautical tourism:** 212,792 (APIQROO).
- **Puerto Vallarta port:** 535,132 passenger movements in official 2025 workbook.
- **Cabo San Lucas port:** 1,147,082 summed from the official monthly 2025 image table; confirm table definition/status before finance use.

No airport, cruise, tourism, or nautical pool has been converted into L3 route demand. Conversion and capture assumptions remain null.

## Atlas baseline reviewed

- Five canonical city IDs: `cancun-riviera-maya-mexico`, `cozumel-mexico`, `playa-del-carmen-mexico`, `los-cabos-mexico`, `puerto-vallarta-mexico`.
- **57 current Mexico routes reviewed:** 24 Cancún/Riviera Maya, 16 Los Cabos, 16 Puerto Vallarta, plus one hidden/quarantined canonical Playa–Cozumel inter-city edge.
- No matching `atlas-external/boarding-points` artifact was found in this repo snapshot.
- The exact canonical Playa–Cozumel edge `e__playa-del-carmen-mexico__playa-del-carmen-ferry__cozumel-mexico__cozumel-ferry-san-miguel` is hidden/quarantined and must not be published. Visible duplicate/alias review is required against `ics-dd1d814699` and `ics-9d3a6b961f`.

## Economics blockers

1. APIQROO directional and operator passenger splits for Playa–Cozumel and Puerto Juárez–Isla Mujeres.
2. Observed fare-class/operator/discount/fee mix and realized yield.
3. A clean official Isla Mujeres departure table; the 2025 government prose around `38,063` departures is malformed.
4. Route-level ridership and fares for Los Cabos resort routes and Puerto Vallarta bay routes beyond Yelapa.
5. Exact BP aliases, coordinates, berth suitability, and hand-sealed approaches.
6. Confirmation of Cabo San Lucas 2025 passenger-table definition/status.
7. Separate official sourcing for existing DiDi market-leadership and airport-transfer claims.

## Brief maturity

Current canonical briefs have strong qualitative narratives but weak exact source/date, demand, fare, and economics fields. Recommended action is **in-place enhancement**, not replacement. Keep canonical briefs partner-neutral; keep DiDi-specific first/last-mile and in-app orchestration language in the partner sub-proposal only.

## Safe proposal framing

- Caribbean: two independently verified mass passenger corridors exist, but total corridor traffic is **not** DiDi-addressable or Navier-capturable demand without explicit approved assumptions.
- Pacific: airport/cruise counts are context only. Yelapa has current water-service evidence; Los Cabos Atlas resort corridors remain future opportunities pending route-level evidence.

## Artifacts

- Structured JSON: `DIDI-MEXICO-L3-DEMAND-FARE-SOURCING-2026-07-09.json`
- This status file: `DIDI-MEXICO-ECONOMICS-STATUS-2026-07-09.md`
