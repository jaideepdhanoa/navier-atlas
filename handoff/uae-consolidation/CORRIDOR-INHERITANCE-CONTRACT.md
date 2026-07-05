# Corridor inheritance contract — how partners inherit the global network (UAE first, then everywhere)

**Owner:** Tasklet (contract + validation) → Grok (enforce at seal)
**Date:** 2026-07-05
**Trigger:** Jaideep — "How do we ensure partners inherit the global corridors in their cities/clusters going forward? I don't know how we got 4 partners with 4 different scopes just in UAE."

## Why we got 4 partners / 4 scopes (the honest answer)
Today a corridor is treated as if it belongs to a **partner**. Each partner JSON hand-curates its **own** `_map_scope` subset out of the shared (messy) `ROUTES.json`. There is **no single source of truth** for "the UAE network" — Careem, Bolt, Yango, Noon each independently hand-picked, so we got four different masks over the same 666-route mess → four different UAE maps. Nothing forces them to agree, so they drifted.

## The principle (the fix)
**A corridor is a property of GEOGRAPHY, not of a partner.** It exists **once**, at the global/cluster layer. A partner does **not** own or curate corridors. A partner only declares **which clusters/cities it operates in**, and then inherits **every** canonical corridor in those clusters **1:1** — exactly the Gojek corridor-inheritance rule ("inherit every real corridor per region 1:1; never curate a subset, never invent") applied globally.

## Three layers
1. **Global canonical corridor set** — `ROUTES.json`. Every corridor de-duped, land-clean, in-range, and stamped with `cluster_id` (+ endpoint `city_id`s). **This is the global UAE view** — one set, rendered on the master/global map. Fixing this fixes the global view *and* every partner at once.
2. **Cluster/city registry** — `CLUSTERS.json`. Corridors bind to clusters (`dubai`, `abu-dhabi`, `sharjah-ajman`, `ras-al-khaimah`, `uae-east-coast`, …).
3. **Partner scope** — partner JSON `_map_scope` = a **list of cluster/city IDs only** (a membership set), plus `"inheritance_policy": "inherit_all_cluster_corridors"`. **No corridor arrays in partner files, ever.**

## Derivation rule (what the renderer does)
```
partner_rendered_corridors(P) = { c ∈ global_canonical : c.cluster_id ∈ P.clusters }
```
If two partners both operate Dubai, they render **identical** Dubai corridors. Divergence is only possible at **cluster membership** (e.g. partner X isn't live on the east coast) — **never** at the corridor level. Same geography → same lines, always.

## Going-forward enforcement (seal gate — this is what prevents drift)
- **`validate_partner_inheritance.py`** (new seal gate): for every partner, assert
  `rendered_corridor_set(P) == global_canonical ∩ P.clusters`.
  **FAIL the seal** if any partner enumerates a corridor not derivable from its clusters, or omits one that is.
- A **new corridor is authored ONCE** in the global set and bound to a cluster; it then flows automatically to every partner in that cluster. **Adding a corridor to a single partner is forbidden** and the gate rejects it.
- **Ban hand-curated corridor arrays** in partner `_map_scope`; scope is membership + policy only.

## Migration for this UAE pass
1. Grok seals the consolidated **global** UAE corridor set, each corridor tagged `cluster_id`.
2. **Delete** the 4 divergent per-partner UAE corridor curations.
3. Set each partner's UAE `_map_scope` = **cluster-membership list + inherit-all policy**.
4. Run the parity gate → all four render **identically**, and identical to the global view.

## Scope of this contract
UAE is the first application, but the contract is **global**: it is how every partner inherits every market's corridors from here on. Roll the same gate across all partners/markets so no other geography can develop a UAE-style 4-scope split.
