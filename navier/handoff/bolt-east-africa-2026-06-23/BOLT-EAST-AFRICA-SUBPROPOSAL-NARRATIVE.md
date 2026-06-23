# Bolt — East Africa coastal cluster sub-proposal (DRAFT for human review)

**Status:** research-complete / seal-needed (geometry) + cascade-needed (economics).
**Date:** 2026-06-23 · Follow-on to PR #83 (Bolt Phuket/Lagos/Cape Town additions).
**Cluster key (proposed):** `bolt-east-africa`

> External/partner-facing copy — stays a **draft** until human review. Numbers below are
> source-anchored assumptions, not sealed economics.

---

## 1. Why Bolt × East Africa, now

Bolt is the **dominant ride-hailing platform in Tanzania** — its 2025 global mobility report named
Tanzania **Africa's fastest-growing rides market (+68% YoY)**, with **30,000+ drivers across eight
Tanzanian cities**, and in **August 2025 Bolt was officially licensed by the Zanzibar government**,
launching on the islands (Stone Town–focused) that September. Bolt is also live on the **Kenyan coast**
(Mombasa, Diani, southern Kilifi).

That gives Bolt exactly the demand-side distribution Navier needs in a region whose geography is
**water-first**: a tourism-heavy archipelago and a long reef coast where the existing options are
slow diesel fast-ferries, rough multi-hour island crossings, car-free islands reachable only by boat,
and a chronically congested channel ferry. This is a natural, reusable coastal-cluster asset.

**Scope note:** Kenya was dropped as a *standalone* node in PR #83 (too weak alone). It returns here
**only as part of a coastal cluster** — a different, stronger thesis, not a reversal.

## 2. The cluster (three sub-regions)

- **Kenya coast:** Mombasa (gateway + Likoni channel), Diani/Ukunda (south-coast resorts), Kilifi
  (creek/marina), with Malindi · Watamu · Lamu as brief-only northern nodes (Lamu is car-free,
  water-access-only via Mokowe jetty).
- **Tanzania mainland:** Dar es Salaam (primary gateway + ferry hub), with Bagamoyo and Tanga as
  brief-only northern nodes.
- **Zanzibar archipelago:** Stone Town/Zanzibar City (ferry hub), Nungwi/Kendwa (north resort cluster),
  Paje/Jambiani (east resort strip), **Pemba** (Mkoani/Wete — dive/eco-lux), **Mafia** (Kilindoni —
  marine-park dive market, poorly connected today).

## 3. Market pull (source-anchored)

- **Zanzibar arrivals:** 638k (2023) → 737k (2024) → **917k (2025), +24%**; air traffic ~2.1M pax/yr,
  tripled in four years.
- **Dar ↔ Stone Town:** ~**76 km / ~41 nm**, today a 90–110 min Azam fast-ferry (4 daily slots each way,
  foreign fare from ~$45); operator added its 12th fast ferry in 2025 — a demand-growth signal.
- **Mombasa ↔ Diani:** ~$29 / 1.5–2 h by road today because of **Likoni channel congestion** — a clean
  water-shortcut thesis.
- **Pemba / Mafia:** 4–6 h rough ferries or flight-only — premium fast-craft unlocks constrained markets.

## 4. Signature corridors (candidate — range-gated)

| Corridor | ~nm | Vessel (gate) | Tier | Note |
|---|---|---|---|---|
| **Dar es Salaam ↔ Stone Town** | 41 | Pioneer II (N30) | **Marquee** | Replaces the flagship Azam ferry |
| **Mombasa ↔ Diani** | 16 | N30 / N35 at scale | **Marquee** | Bypasses Likoni congestion |
| Stone Town ↔ Nungwi | 30 | N30 | Resort transfer | North-tip resort cluster |
| Stone Town ↔ Pemba | ~48 | N30 | Outer island | Replaces 4–6 h rough ferry |
| Dar / Stone Town ↔ Mafia | ~68–70 | N30 (re-gate on seal) | Outer island | Borderline range — flag |
| Mombasa ↔ Likoni shuttle | ~1 | N35 Shuttle | Commuter | Very-high-volume, low fare |
| Mombasa ↔ Kilifi | 30 | N30 | Coastal hop | |
| Mombasa ↔ Malindi/Watamu | ~60 | N30 | Coastal hop | Borderline-OK |
| Malindi ↔ Lamu | ~120 | **Quanta-LR** (amber) | Roadmap | Range-gated long leg |
| Mombasa ↔ Pemba | ~54 | N30 | **Cross-border roadmap** | KE↔TZ clearance required |

All within-70nm legs are **N30/Pioneer II**; the Malindi↔Lamu long leg is **Quanta-LR roadmap**; the
cross-border Mombasa↔Pemba leg is geometrically in-range but **roadmap-only** pending customs/maritime
clearance. Borderline (~65–72 nm) legs are flagged for exact re-gate once Grok seals coordinates.

## 5. Product fit

Two marquee legs (Dar↔Stone Town 41 nm, Mombasa↔Diani 16 nm) plus the resort-transfer and outer-island
hops all sit inside the **N30 ≤70 nm envelope**, with N35 Shuttle as the dense-commuter complement on the
Likoni channel. Only the Lamu long leg needs Quanta-LR. The **clean Kenyan grid** (~90%+ geothermal/hydro)
makes the Kenya legs a marquee zero-emission story; the Tanzania legs still beat the diesel ferries they
displace per trip.

## 6. What's sealed vs. open

- **Tasklet (this package):** source-led footprint, coastal nodes + evidence tiers, 21 candidate boarding
  points with gazetteer hints, 11 candidate signature corridors with range-gate + demand/fare anchors,
  and Kenya/Tanzania country-reference rows.
- **Grok (seal-needed):** geocode + ID-match BPs, build BP↔BP geometry, water/land-crossing gate, re-gate
  borderline legs, stand up the `bolt-east-africa` partner view.
- **Tasklet (cascade-needed, after seal):** country-reference confirm → aggregate → growth → frontend →
  splice → transparent sheet → master tracker → economics sidecar.

## 7. Reuse

The cluster (nodes, BPs, corridors, Kenya/Tanzania country-reference) is **reusable** for Uber
(Kenya + Tanzania coast), Yango (existing Tanzania/Mozambique seeds), and East-Africa hospitality
partners via `inherit-markets` once the geometry is sealed.
