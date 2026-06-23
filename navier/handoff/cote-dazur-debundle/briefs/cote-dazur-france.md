# Côte d'Azur (French Riviera) — cluster parent

> **Posture:** P0 — Mediterranean (Wave 9-A net-new; **cluster parent**, nodes de-bundled 2026-06-23)
> **Region:** Europe-Med
> _The original superyacht coast — a near-continuous luxury-marine corridor from St-Tropez to Menton — modeled as a cluster of operationally distinct nodes._

## Overview

The French Riviera is the historic heart of the superyacht world and one of Europe's densest concentrations of wealth, yachting and coastal congestion. It is **not a single market** but a string of operationally distinct nodes along a short, protected strip where the corniche roads and the A8 jam constantly and a yacht-conditioned clientele already values water transfer. Short coastal distances (Nice↔Monaco ~8 nm, Antibes↔Cannes ~6 nm, Nice↔Cannes ~13 nm, Nice↔St-Tropez ~45 nm) make the whole corridor a premium Pioneer II commute-and-charter network, layered over a real coastal commuter pain.

**This file is the cluster parent.** Each node below has its own standalone brief with full demand spine, regulatory note and key legs. Côte d'Azur stays as the connective corridor overview; the nodes carry the detail.

## Cluster nodes

| Node | Brief | Role | Distinct demand engine |
|---|---|---|---|
| **Nice** | `nice-france` | gateway / network anchor | Nice Côte d'Azur Airport (France's 3rd-busiest, ~14.2M pax 2023) + year-round corporate/commute base; the Airport↔Monaco corridor |
| **Monaco** | `monaco-monaco` | sovereign HNW hub | Sovereign principality; UHNW/superyacht density; F1 Grand Prix + Monaco Yacht Show event-surge fleet |
| **Antibes** | `antibes-france` | superyacht capital / industrial-maritime hub | Port Vauban — Europe's largest yacht harbour (~1,500+ berths); refit/charter/crew counterparty |
| **Cannes** | `cannes-france` | event-surge node | Film Festival (May), Cannes Yachting Festival (Europe's top in-water show, Sept), MIPIM; Lérins island shuttle |
| **St-Tropez** | `saint-tropez-france` | seasonal-peak node | Notorious summer road gridlock (road-bypass wedge); Pampelonne; Les Voiles late-season regatta |

_Monaco is de-bundled as a sovereign **P1** node but is part of the Côte d'Azur cluster family for network and partner-scope purposes. Nice, Antibes, Cannes and St-Tropez were de-bundled 2026-06-23 under the schema split-trigger rule._

## Corridor network (cluster-spanning routes)

- **Nice Airport ↔ Monaco** (~6.7 nm) — Pioneer II; the marquee corridor, substitutes for helicopter + gridlocked corniche.
- **Nice ↔ Monaco** (~8 nm) — Pioneer II; executive coastal commute.
- **Antibes ↔ Cannes** (~6 nm) — Pioneer II; the two yacht hubs, bypassing the coast road.
- **Nice ↔ Cannes** (~13 nm) — Pioneer II; coastal link bypassing A8 congestion.
- **Cannes ↔ Île Sainte-Marguerite (Lérins)** (~1.5 nm) — Pioneer II; captive island shuttle.
- **Menton ↔ Monaco** (~4 nm) / **Villefranche ↔ Monaco** (~5 nm) — Pioneer II; short coastal hops.
- **Monaco ↔ Sanremo (Italy)** (~13 nm) — Pioneer II; cross-border Riviera leg.
- **Nice ↔ St-Tropez** (~45 nm) — Pioneer II edge; long coastal run beating the summer road.
- **Monaco / St-Tropez ↔ Portofino** (~85–95 nm) — Quanta-LR; experiential line-haul beyond all-electric range.

## Archetype fit

- **Ride-hail / super-app premium marine tier** — Bolt-branded foiling along the corridor (see `bolt-france-riviera` sub-proposal); platform: Pioneer II.
- **Nice↔Monaco executive + airport commute** — beats corniche/A8 + substitutes the helicopter; platform: Pioneer II.
- **Riviera superyacht tender tier** — Monaco/Antibes/Cannes/St-Tropez crew-and-guest tenders; platform: Pioneer II.
- **Riviera coastal hop & island shuttle** — Nice↔Cannes↔St-Tropez + Lérins; platform: Pioneer II.

_Source: cluster parent reorganized 2026-06-23 (nodes de-bundled: nice-france, cannes-france, antibes-france, saint-tropez-france; monaco-monaco folded into cluster family). Boarding points in atlas-external/boarding-points/ per node file._
