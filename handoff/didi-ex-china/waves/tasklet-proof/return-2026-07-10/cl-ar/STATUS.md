# Chile + Argentina P1 evidence status — T7/T8

**As of:** 2026-07-10  
**Scope:** 10 exact un-quarantined route IDs from `GROK-CL-AR-HAND-ROUTE-RECEIPT-2026-07-10.json`; exact DiDi proof for nine named towns/zones.

## Result

- **19 records total:** 10 T7 route-demand records and 9 T8 service-area records.
- **3 usable records:** 2 exact-route passenger totals and 1 exact DiDi zone proof.
- **8 T7 routes remain hard-null** for annual passengers.
- **8 Chile T8 towns remain holds. Chile featured remains empty.** Directory absence was not treated as proof of non-operation, and nearby anchor cities were not extended to ferry towns.

## What can materialize

1. **`rn-f451444da7fe` — Rosario → Isla Sabino Corsi:** ENAPRO reports **38,900 passengers** for the full **2025–2026 summer operating season**. This is exact-OD, primary authority evidence. It is a service-season total, not a calendar-year total; directions, unique-person status and round-trip status are not disclosed.
2. **`rn-04b92d6952d2` — Buenos Aires → Colonia:** Uruguay INE/MTOP reports **2,177,670 passenger movements in regular vessel services** in **2024** for the exact Colonia–Buenos Aires port pair. The figure aggregates both directions and all regular operators; it is not a Buquebus-only or unique-visitor count.
3. **Tigre / `rn-f6d1302e7121`:** DiDi Argentina’s current official driver page explicitly names **Tigre** among zones available to drive. This resolves the prior directory-only hold at city/service-zone level. It does not prove realized supply or pickup success at the ferry ramp.

## What stays null or held

### T7 annual passengers — hard-null

No qualifying public exact-OD annual passenger figure was found for:

- `rn-27ac33a14eb2` — Tres Puentes → Porvenir
- `rn-4176c336f07a` — Niebla → Corral
- `rn-60ac3dd2ce79` — Calbuco → Isla Puluqui
- `rn-a5ddce927bd3` — Pargua → Chacao
- `rn-eaedbbb4abe9` — El Pasaje → Coyumbe
- `rn-c6a108b7f3d2` — Lota → Isla Santa María
- `rn-f6d1302e7121` — Tigre Line 452 endpoint
- `rn-97c9f0b33379` — Puerto Pañuelo → Puerto Blest

Schedules, fares, capacities, vehicle traffic, consultation respondents, general visitors and nearby-route numbers were not converted to passengers.

### T8 DiDi exact coverage — hold

No official service-area/polygon or current in-app proof was found for **Niebla, Corral, Calbuco, Pargua, Chacao, Dalcahue, Lota, or Porvenir**. Valdivia, Puerto Montt, Concepción, Punta Arenas and Magallanes are nearby/broader labels only and do not prove these ferry towns.

## Exact next action

1. Materialize only the two published route totals above, preserving their stated periods and unit semantics without direction or round-trip conversion.
2. Send route-specific data requests to TABSA; Chile DTPR/MTT and the relevant subsidized operators; Buenos Aires Province transport/Interisleña; and the Puerto Blest concession/park authority. Request monthly passenger boardings by direction and explicitly exclude vehicle-only counts.
3. For each held Chile town, capture a dated DiDi passenger-app pickup/drop-off result at the exact ferry BP or obtain an official service polygon/name. Keep Chile featured empty until that exact proof exists.
4. Review the Tigre route for eligibility using the official named-zone proof, while keeping supply/wait-time claims null.

All source metadata, quotes, unit semantics, local-language searches and failed-source notes are in `EVIDENCE-LEDGER.json`.
