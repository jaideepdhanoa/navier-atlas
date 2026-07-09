# DiDi × Navier — Mexico Caribbean status (2026-07-09)

**Status:** Research complete; one route is display-ready, one is quarantined, and Chetumal is backlog only.

## What is solid
- Preserve canonical IDs: `cancun-riviera-maya-mexico`, `cozumel-mexico`, `playa-del-carmen-mexico`, all in country cluster `mexico`.
- `ics-413f51cd44` (Puerto Juárez ↔ Isla Mujeres, 5.27 nm) exactly matches existing BPs and route geometry. APIQROO recorded **5,458,304 passenger movements in 2025**.
- Playa del Carmen ↔ Cozumel is current scheduled service with **3,853,770 passenger movements in 2025**, but the exact Atlas route remains **quarantined/hidden** until its city berths are reconciled.
- Official DiDi city evidence was found for **Cancún, Chetumal and Campeche** only.
- Chetumal has a real official passenger port and operator-sold Belize link, but no canonical city/BP/geometry yet. It is backlog, not display-ready.

## P0 blockers
1. Reconcile Playa's BP coordinate: the existing BP and route endpoint differ materially.
2. Bind/alias San Miguel ferry terminal to `cozumel-mexico` and clear route quarantine only after QA.
3. Do not claim DiDi operates in Playa, Cozumel, Puerto Morelos, Isla Mujeres or Holbox without new official evidence.

## Finance guardrails
- Treat APIQROO entries + exits as one-way passenger legs, not unique people.
- Keep airport and cruise totals out of route demand.
- Keep Chetumal `annual_one_way_pax` null: its 25,072 movements are a port aggregate, not a San Pedro endpoint split.
- Public one-way fare benchmarks: Playa–Cozumel MXN 320 premium / 190 state resident / 100 local; Puerto Juárez–Isla MXN 290 / 100 / 55; Chetumal–San Pedro MXN 1,340 standard / 1,050 Mexican citizen. No fare mix is assumed.

## Do not publish
- The partner file's 2.4 nm Holbox journey, mismatched Banco Chinchorro card, or ungrounded fleet/economics claims.
- Campeche Lerma as a passenger BP; the official page describes fuel/fishing/support activity.
- Any unbound candidate as a new map city or corridor.

Full structured artifact: `/tasklet/agent/home/didi-ex-china-audit/mexico/DIDI-MEXICO-CARIBBEAN-BP-BRIEF-RESEARCH-2026-07-09.json`
