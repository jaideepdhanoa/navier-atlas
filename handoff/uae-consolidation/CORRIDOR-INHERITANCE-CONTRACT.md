# Corridor inheritance contract — how every partner inherits the global network (all partners, all markets)

**Owner:** Tasklet (contract + validation) → Grok (enforce at seal)
**Date:** 2026-07-05 · **Applies to:** every partner in `partner-pitch/partners/`, every market.
**Trigger:** Jaideep — "Make sure this applies to all partners across all markets — Singapore, Indonesia, India etc. should all be inheriting. How did we get 4 partners with 4 different scopes just in UAE?"

## This is NOT a UAE problem — the audit
Measured across all 21 multi-market commercial partners (`CROSS-PARTNER-INHERITANCE-AUDIT.json`):

- **275** clusters referenced across partners.
- **116** clusters are shared by **2+ partners** — every one is a place where corridor divergence can occur.
- **17** clusters are shared by **4+ partners**.
- **2,039** hand-curated per-partner corridor entries across the roster — the divergence surface.

Worst hotspots (contested clusters, by region): **Thailand 17** (Bangkok/Phuket/Krabi/Samui/Pattaya each contested by **6** partners — airasia-move, bolt, grab, grab-thailand, line, line-man-wongnai), **Indonesia 15** (Jakarta/Bali/Komodo by airasia-move, gojek, grab), **India 9** (Chennai + Kolkata by ola, rapido, uber, uber-india), **UAE/Gulf 7**, **Colombia 1** (Cartagena by cabify, didi, uber, yango), **Singapore 1**. UAE was just the one we looked at first.

## Why we got "N partners / N scopes" (the honest, evidence-backed answer)
There are **two** layers of scope in every partner file, and only one of them is inherited today:

1. **Cluster membership** — `_map_scope.cluster_city_ids`. **Already inherited** from `CLUSTERS.json` via `scripts/partner-scope.mjs` (`source: live_cluster_inheritance`). This layer is healthy.
2. **Corridors** — `featured_routes` (14–136 per partner), `wow_corridors` (3–52), `route_ids`, `featured_legs`. **NOT inherited** — each partner hand-curates its own arrays. **This is the divergence.** Careem carries 6 featured routes, Bolt 136, Yango 49 — different subsets of the same geography, nothing forcing them to agree, so they drifted.

So the fix is not to invent a new system — it is to **extend the existing `partner-scope.mjs` cluster inheritance down to the corridor layer**, and stop treating corridors as partner-owned.

## The principle
**A corridor is a property of GEOGRAPHY, not of a partner.** It exists **once**, at the global/cluster layer. A partner does not own or curate corridors. A partner declares **which clusters/cities it operates in**, and inherits **every** canonical corridor in those clusters **1:1** — the Gojek rule ("inherit every real corridor per region 1:1; never curate a subset, never invent") made global.

## Three layers
1. **Global canonical corridor set** — `ROUTES.json`. Every corridor de-duped, land-clean, in-range, stamped with `cluster_id` (+ endpoint `city_id`s). This is the **global map view**; fixing it fixes the global view *and* every partner at once.
2. **Cluster/city registry** — `CLUSTERS.json`. Corridors bind to clusters.
3. **Partner scope** — partner `_map_scope` = **cluster/city membership list + `inheritance_policy`** only. **No authoritative corridor arrays in partner files.**

## Derivation rule (what the renderer does)
```
partner_rendered_corridors(P) = { c ∈ global_canonical : c.cluster_id ∈ P.clusters }
```
Two partners sharing a cluster render **identical** corridors there. Divergence is only possible at **cluster membership** (partner X isn't live in cluster Y) — never at the corridor level. Same geography → same lines, always.

## `featured_routes` / `wow_corridors` — allowed, but constrained
These stay permitted as **narrative highlight lists** for deck/proposal emphasis (a partner may spotlight its marquee corridors). But under this contract they are demoted to **presentation-only pointers** and MUST be a **strict subset** of the inherited set:
```
featured_routes(P) ⊆ partner_rendered_corridors(P)
```
They may **never** introduce geometry, a corridor, or a `route_id` that isn't already in the inherited set. A highlight cannot be a source of a new or divergent line.

## Going-forward enforcement (the seal gate that prevents drift)
`validate_partner_inheritance.py` (new gate, runs for **every** partner at seal):
1. `rendered_corridor_set(P) == global_canonical ∩ P.clusters` — **FAIL** if a partner enumerates a corridor not derivable from its clusters, or omits one that is.
2. `featured_routes(P) ⊆ rendered_corridor_set(P)` — **FAIL** on any highlight outside the inherited set.
3. A new corridor is authored **once** in the global set + bound to a cluster; it then flows to every partner in that cluster automatically. **Adding a corridor to a single partner is forbidden** and rejected.

## Migration (global, staged — UAE and Thailand first as worst hotspots)
1. Grok seals each market's consolidated **global** corridor set, every corridor tagged `cluster_id` (UAE this pass; Thailand next given 6-way contention; then Indonesia, India, Colombia, Singapore).
2. **Demote** every partner's curated corridor arrays to presentation-only (or delete where redundant); strip any that aren't a subset of the inherited set.
3. Confirm each partner's `_map_scope` is membership + `inherit_all_cluster_corridors` policy (membership already comes from `partner-scope.mjs`).
4. Run the parity gate across **all** partners → every partner sharing a cluster renders identically, and identical to the global view.

## Scope
Global and permanent. Every partner, every market, from here on. The gate makes a future "N partners / N scopes" split impossible to seal.
