# DiDi Ecuador/Galápagos + Peru Pacific deepening — status

**As of:** 2026-07-09  
**Lane:** Boarding points + brief maturity + demand/fare research  
**Status:** Research complete; **not finance- or publish-ready** until the Galápagos route-stamp P0 is fixed.

## Atlas baseline and integrity

- **7 existing city IDs:** 4 Galápagos + Lima, Paracas, Pisco/San Andrés.
- **Galápagos:** 4/4 canonical briefs present; three real current member routes exist, but all are stamped outside `galapagos-ecuador`. The cluster is corrupted by **46 foreign-stamped routes, all with neither endpoint in a member city**.
- **Peru:** 2/3 canonical briefs present; `pisco-san-andres-peru` is missing. Eleven routes are stamped `peru`; one member route (`rn-f0a756c7f278`) sits outside the cluster.
- Current DiDi evidence is **country-level only**. It does not prove service in Galápagos, Paracas, Pisco/San Andrés, or at any pier.
- The requested raw `/tmp/navier-atlas` checkout was not mounted. Baseline facts were recovered from the current 2026-07-09 DiDi LATAM audit and route-stamp defect ledger generated from the canonical checkout. No repository edits were made.

## Verified boarding context

### Galápagos

Official DPNG/CGREG/ABG material verifies:

1. **Muelle Gus Angermeyer** — Puerto Ayora / `santa-cruz-galapagos-ecuador`
2. **Muelle de Pasajeros de Puerto Villamil** — `isabela-galapagos-ecuador`
3. **Muelle Tiburón Martillo** — Puerto Baquerizo Moreno / `san-cristobal-galapagos-ecuador`
4. **Muelle turístico y de carga de Puerto Velasco Ibarra** — `floreana-galapagos-ecuador`

Coordinates and exact current BP IDs still require canonical-file confirmation; no coordinates were invented.

### Peru Pacific

- **Verified:** El Chaco tourist embarkation function in Paracas; Muelle Dársena/Plaza Grau and Marina Club access context in Callao.
- **Hold:** DPA San Andrés exists but is a fishing landing with rehabilitation history; public passenger authorization and current operational status are unproven.
- **Non-BP POIs:** Terminal Portuario General San Martín is a multipurpose commercial terminal, not proven public passenger infrastructure. Islas Ballestas and Islotes Palomino are marine destination POIs/circuits, not landing BPs in this evidence set.

## Current route and fare evidence

### Galápagos populated-island launches

DPNG publishes small launches of up to 20 passengers, typical **2–3 hour** trips, and **USD 30 per person per route**.

- Santa Cruz → San Cristóbal: 13:45–16:00; return 07:00–09:30.
- Santa Cruz → Isabela: 13:45–16:00; return 06:00–08:30.
- Santa Cruz → Floreana: 08:00–09:45; return 15:00–17:00, **Tuesday/Thursday**.
- Sea state is described as calmer January–June and rougher July–December.

The three exact current route IDs are retained in the JSON because endpoint matches were confirmed in the current route audit. Do not activate them in DiDi inheritance until the cluster stamp is repaired.

### Peru excursions

- **Paracas–Ballestas:** SERNANP publishes **21.4 km / 1h40 round trip**, year-round visitor context, Monday–Sunday 06:00–13:00. Adult national ANP entry is S/11; combined Paracas/Ballestas promotional entry is S/17. A commercial page advertises S/40 regular and S/60 on specified holidays; re-quote before finance use.
- **Callao–Palomino:** official departure-area evidence exists for Muelle Plaza Grau / Marina Club, but current fare, schedule and annual riders remain null.
- **Lima/Callao–Paracas** and **San Andrés–Paracas** remain future hypotheses, not current services.

## Demand guardrails

- DPNG reports **279,277 Galápagos tourist arrivals in 2024**; 79% were land-based. This is archipelago TAM context, **not inter-island route demand**.
- CEPLAN reports **1,119,437 visits to principal Ica tourist sites**, **1,657,046 lodging arrivals**, and **2,194,261 overnight stays** in 2024. These are regional flows, **not Ballestas or corridor riders**.
- No audited route-level annual passenger counts were verified. Every `annual_one_way_pax` remains `null`.

## Brief maturity

- Existing briefs have 12/12 core fields and should be enhanced, not replaced.
- Floreana is complete but thin (1 journey, 1 signature route, 2 sources).
- Isabela, San Cristóbal, Santa Cruz and Lima are mature by current audit metadata.
- Paracas is complete but still lacks audited corridor demand.
- Pisco/San Andrés needs a new **partner-neutral** canonical brief focused on its fishing-waterfront reality, facility permissions, and passenger-service uncertainty.
- DiDi-specific positioning is isolated in the JSON partner narrative block.

## Geometry / hand-waypoint requirements

- The three Galápagos populated-island links show no apparent land crossing, but harbor-mouth review is still required.
- Ballestas and Palomino need operator/authority tracks or hand waypoints to respect harbor approaches, protected areas and no-go zones.
- Lima–Paracas needs explicit offshore/coastal hand waypoints; never publish a naive endpoint line.
- Any San Andrés–Paracas concept must avoid fishing operations, restricted terminal waters and shallow hazards and must use a Capitanía/APN-approved track.

## Blocking next actions

1. **P0 — Atlas data/geometry:** remove 46 foreign Galápagos stamps, stamp the three real route IDs, rerun corridor-inheritance/no-shrink validation.
2. **P0 — Canonical checkout QA:** confirm exact BP IDs, names, coordinates and Peru route endpoint records in the current repository.
3. Obtain 2024–2026 Galápagos route manifests/load factors/cancellations before economics.
4. Obtain Ballestas and Palomino monthly passengers, sailings, capacity, weather cancellations and full fee stacks.
5. Confirm DPA San Andrés structural status and passenger permissions; otherwise keep it unpublished.
6. Obtain DiDi city-level service confirmation before making local availability claims.

## Artifacts

- Structured research: `DIDI-ECUADOR-PERU-DEEPENING-2026-07-09.json`
- This status: `DIDI-ECUADOR-PERU-STATUS-2026-07-09.md`
- JSON validation: **PASS** (`json.loads` plus required-key, route-field and summary-count assertions).
