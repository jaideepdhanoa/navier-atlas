# Grok Routing Brief — Bucket B Boarding Points (2026-06-19)

**From:** Tasklet (research lane) · **To:** Grok (deterministic routing/seal lane)

## Ownership recap (corrected RACI)
- **Tasklet** identifies boarding points, marquee/signature routes, demand, ID crosswalks, and builds the financial model.
- **Grok** routes identified BPs into navigable water-path geometry, applies allowlist masks (LB-242), reseals, render-checks, runs aggregate→growth, commits.

## What's in this package
6 newly-minted atlas boarding-point files (27 BPs total) for the previously truly-missing nodes, plus the corridor ID crosswalks already applied to `corridors.json`.

| node_id (atlas city_id) | BPs | coord confidence | Grok action |
|---|---|---|---|
| `lisbon-tagus-portugal` | 10 | high (Transtejo/Soflusa canonical) | route lagoon/estuary crossings; ready |
| `abidjan-cote-divoire` | 5 | mixed (1 OSM-confirmed, rest medium/low) | route Ébrié-lagoon network; validate CITRANS quay |
| `al-wakrah-qatar` | 3 | high (marina-DB confirmed) | route coastal; ready |
| `dammam-khobar-ksa` | 4 | medium/low | validate marina/yacht-basin coord, then route |
| `amaala-ksa` | 2 | **low — giga-project** | **validate coord vs satellite before routing** |
| `neom-ksa` | 3 | **low — giga-project** | **validate coord vs satellite before routing** |

## ⚠️ null-beats-wrong flags
`amaala-ksa` and `neom-ksa` are giga-projects under construction. Coordinates are **approximate** (regional placement only) and tagged `confidence: low`, `precision: approx_*`. Do **not** seal their geometry as confirmed until validated against current satellite imagery. Better to keep aspirational than render confidently-wrong.

## ID crosswalks already applied to corridors.json (no minting needed — geometry pre-existed)
`manama→manama-bahrain`, `fujairah→fujairah-uae`, `ras-al-khaimah→ras-al-khaimah-uae`, `red-sea-global-ksa→red-sea-global`, `lagos→lagos-nigeria`, `cote-divoire→abidjan-cote-divoire` (72 + 12 node-field remaps).

## Verification state after this work
- Bolt/Yango bound node refs geometry-ready: **288/288 (100%)** — was a confused/partial count before.
- Atlas distinct city_ids: 174 → **180**.

## Still open (Tasklet research, separate from this package)
- **Bucket C** — ~19 null-node aspirational stubs (Bolt Baltics/Med tail, Yango CIS/Africa) need BPs + signature route identified from scratch before they can bind.
- Then: Tasklet builds Bolt/Yango `growth_case` (held until geometry + demand complete, per sequencing).
- Fold **LB-242 `route_water_allowlist.json`** into the routing/mask lane.
