# Colombia P0 / T1 status — 2026-07-10

## Decision

**C — hold.** Keep Colombia unmaterialized in finance, consistent with `GROK-COLOMBIA-SPINE-RECONCILIATION-2026-07-10.json`.

## What stays null

For exact route `rn-aa790551baa7` (**Club de pesca de Cartagena - Marina ↔ Bocachica Tierrabomba Jetty**):

- annual one-way passenger journeys: **null**
- current authoritative fare per passenger boarding: **null**
- current dated timetable/schedule: **null**
- realized yield: **null**

No public source proved that exact current scheduled public passenger service. Sources describing La Bodeguita, generic Cartagena–Bocachica tours/transfers, marina traffic, or regattas cannot be substituted for the exact Club de Pesca BP.

## What can materialize

**Nothing in finance.** The only non-null evidence is benchmark-only:

- District mobility plan, base year 2012: La Bodeguita–Bocachica **706 passengers/study day** (686 excluding tourists), with unspecified directionality. This is not annual and was not annualized.
- January 2018 FDN/BID study, modeled 2017 base: BChica–Bodeguita **82 modeled AM-peak passengers** and **15-minute modeled interval**. This is not an observed annual count or current timetable.
- August 2008 ITDP study: historical multi-stop Bocachica–Caño de Loro–La Bodeguita operation within **06:00–18:00**, but the same study says there were no pre-established fares and records no fixed schedules.
- 2023 La Bodeguita total: **619,282 terminal entries**, with no OD/direction split. It must not be mapped to Bocachica or Club de Pesca.

Classification count: **1 `not_publicly_supported`; 1 `benchmark_only`; 0 `usable_for_base_case`; 0 `permission_required` as standalone records.** Permission remains required and is noted, but the assigned route receives one overall classification only.

## Spine recommendation and inheritance

- **A:** hold — exact geometry exists, evidence gate is still null.
- **B:** do not adopt as-is — no qualifying demand/fare/schedule packet was found, and `rn-3ebf0c9aece2` is present only in `finance/model/corridors.json` (Barranquilla–Puerto Colombia), not current global canonical `data-clean/ROUTES.json`; the other four option-B IDs are canonical. A partner finance spine cannot create geography.
- **C:** **recommended.** This preserves the Grok hold and the corridor-inheritance contract.

## Exact next action

Send a formal information request to Cartagena’s mobility authority, DIMAR/Capitanía de Puerto, Muelle La Bodeguita administration, and authorized Bocachica carrier(s) for:

1. current route authorization and named operator;
2. current published passenger fare per boarding;
3. dated timetable/service window; and
4. monthly exact-OD passenger boardings for one complete recent calendar year, with directionality and passenger/ticket semantics.

If the authoritative OD is **La Bodeguita ↔ Bocachica**, first obtain/seal its exact canonical BP and route ID. Do not reuse `rn-aa790551baa7` or fabricate an ID.
