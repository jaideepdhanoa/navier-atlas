# Route Demand Model — `traffic_weight` methodology
_locked 2026-05-30 · governs every route's line weight on the atlas_

## Why this exists
`traffic_weight` (0–1) drives how heavy/bright a route draws. It must be a **grounded demand
thesis**, not graph degree — because those thick lines are exactly what we defend to Grab / RTA /
ITC ("why is this corridor heavy?"). Degree-based weighting is explicitly rejected: connectivity ≠ demand.

## The model
```
traffic_weight = normalize( expected_volume × navier_fit )
trip_purpose   = commuter | business | tourism | luxury | local | mixed   (separate tag)
```

### 1. expected_volume — calibrated to OBSERVED flows, never invented
Anchor each city-pair to real travel that already happens between the two endpoints:
- existing ferry pax / yr
- air O&D pax / yr (routes a boat could substitute)
- road / bridge / border crossings / day
- destination hotel-key capacity (tourism mass)
- population × economic mass / travel-time  (gravity term — but **calibrated to the flows above**, not free-floating)

### 2. navier_fit — does the foiling boat actually win here?
Modifier in [0.4 … 1.2]:
- time saved vs incumbent mode (drive / ferry / fly)
- crossing roughness → seasickness relief (the #1 latent-demand unlock)
- no-bridge / no-road structural advantage
- range feasibility: Pioneer II (≤70 nm all-electric) vs Quanta-LR (hybrid, long-haul)

### 3. trip_purpose → maps to the partner story
- `commuter` → transit authority / super-app daily demand
- `business` → super-app premium + corporate
- `tourism` → hospitality / experience
- `luxury` → charter / resort
- `local` → intra-city water-taxi capillaries

## Confidence tiers (mirrors the BP grading philosophy)
- **high** — documented existing flow (ferry stats, border counts, air O&D)
- **med** — gravity-modeled from population/economic mass + hotel capacity
- **low** — judgment estimate
Store the underlying anchor as evidence so every heavy line is auditable. Evidence text is
**internal_only** (it can name operators / volumes); only the numeric `traffic_weight` + neutral
`trip_purpose` + `edge_class` ship externally.

## Edge classes & weight bands
| class | what | typical weight | render |
|---|---|---|---|
| `trunk` | heavy backbone corridors (proven mass) | 0.80–1.00 | heaviest, always visible |
| `regional` | cross-cluster / cross-border connectors | 0.45–0.79 | mid-zoom |
| `local` | intra-city BP↔BP capillaries | 0.10–0.40 | light, brighten on zoom-in |

## Worked calibration (the markets Jaideep named)
| corridor | purpose | observed anchor (internal) | fit | class | weight |
|---|---|---|---|---|---|
| Johor/JB ↔ Singapore | commuter | ~300k+/day land crossings (world's busiest border); marine captures premium slice only | med | regional | 0.55 |
| Singapore ↔ Batam | tourism/business | millions ferry pax/yr (established boat market) | high | trunk | 0.90 |
| Singapore ↔ Bintan | tourism/luxury | resort ferries (Bintan/Lagoi) | high | regional | 0.60 |
| Dubai ↔ Abu Dhabi | business+tourism | heavy E11 corridor, ~90-min drive; Quanta-LR range | high | trunk | 0.85 |
| Dubai ↔ Sharjah | commuter | notorious daily road congestion | high | trunk | 0.80 |
| Dubai intra (Marina↔DIFC↔Palm) | local | existing abra/ferry + dense waterfront | high | local | 0.30–0.40 |
| Sanur ↔ Nusa Penida/Lembongan | tourism | huge fast-boat market | high | trunk | 0.88 |
| Bali ↔ Gili/Lombok | tourism | busy Padangbai/Serangan↔Gili fast-boats | high | trunk | 0.85 |
| Phuket ↔ Phi Phi | tourism | dense daily speedboat/ferry | high | trunk | 0.88 |
| Phuket ↔ Krabi/Railay | tourism | heavy daily ferry | high | regional | 0.70 |
| Phuket ↔ Langkawi | tourism (cross-border TH↔MY) | seasonal; ~80 nm → Quanta-LR | med | regional | 0.50 |

## Key principle (from Jaideep)
> Singapore↔Batam/Bintan is tourism-led, NOT commuter. The real commuter mass is Johor↔Singapore,
> but boats only capture a premium slice of a land-bridge flow. The model must preserve that
> distinction instead of flattening every line to the same weight.

## Implementation
- `route_network.py` reads curated boarding-point JSONs + `route-demand-config.json`, builds a
  **layered BP-graph network** (local mesh + regional + trunk) with endpoints on real BP coords,
  land-validates every edge (SeaGrid A* + interior-land guard, 1.9 km gate), and emits
  `traffic_weight` + `trip_purpose` + `edge_class` per edge.
- Evidence/anchor strings stay internal; never shipped past the externalization gate.
