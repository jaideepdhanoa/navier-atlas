# Navier Atlas — Data Architecture Direction
_Authored 2026-05-30 in response to: "anything we should learn/improve so the matrix of cities/nodes/routes/entity-types stays structured, scalable, reusable across mediums?"_

## TL;DR
The graph spine is healthier than it looked, but **content↔graph joins are enforced by naming convention only**, confidentiality is **re-derived** each build rather than tagged, and data is **shaped for the map** rather than projected to many mediums. Fix in three moves: (1) **integrity gate** [SHIPPED], (2) **field-level visibility tags**, (3) **one spine → many projections**.

---

## What we have today (measured 2026-05-30)
| Layer | Count | Keyed by | Join health |
|---|---|---|---|
| Graph nodes | 803 features (62 labelled anchors) | node `id` | ok |
| Edges/routes | 1,376 | `from_node_id` / `to_node_id` | **was 37 dangling → fixed to 5 known-gap** |
| Orgs | 1,213 | org id | not joined to cities/routes |
| Humans | 648 | human id | not joined |
| City briefs | 38 | `city_id` (= anchor node id) | 1 dangling (colombo) |
| Partner proposals | 9 | `partner_id` | ok |
| Boarding points | per-city JSON | bp id | named-at-source backlog |

**Good news:** edges already reference node ids (not hashes) and carry `distance_nm`/`platform`/`edge_class`. The spine is normalized.

**The real weakness:** two id namespaces that *must* align — anchor `city_id` (content) and node `id` (spine) — with **nothing enforcing it**. Every id bug this session (`jakarta-batam`→`jakarta`, `salalah-oman`→`salalah-dhofar-oman`, colombo-no-node, 19 alias-drift edge endpoints like `muscat`→`muscat-oman`) is this one root cause.

---

## Principle: ONE SPINE, MANY PROJECTIONS
The graph spine (nodes + edges + orgs + humans) is the **single source of truth**. Everything else is either (a) a reference *into* it by id, or (b) a generated *projection out* of it.

- **Content layer** (briefs, partners) must reference entities **by id**, never restate spine facts (coords, distances, platform). A brief says "see route X"; it does not re-encode the route.
- **Mediums** (Mapbox atlas, pitch deck, PDF export, Proposal Designer app, future API) are **projections**: a small adapter selects + reshapes spine data. Adding a medium = adding an adapter, not re-keying data.
- **Consequence:** change a fact once, every medium updates. Today a city's name/coord lives in nodes *and* is implied in briefs *and* in partner phase text — three hand-syncs.

## Three concrete improvements

### 1. Referential-integrity gate  ✅ SHIPPED (2026-05-30)
`atlas-external/integrity/build_manifest.py` — read-only, modifies nothing. Checks:
- every edge endpoint resolves to a node id
- every brief `city_id` resolves to a node id
- every `*_city_id` in partner files resolves
- coverage stats (anchors without briefs)

`known-gaps.json` allowlist separates **new regressions (hard ERROR)** from **tracked gaps (WARN)** — no cry-wolf. Wire into seal/build pre-flight so broken joins can never ship silently. **This alone kills the recurring id-mismatch bug class.**

### 2. Field-level visibility tags (replace the partition re-derivation)
Today confidentiality = a separate partition pass that re-derives an external copy each build (`output-external/`), and internal jargon leaks as *field names* (`wedge_archetype` in edges, "wedge" tokens in briefs).
- Tag sensitive **fields** with `"_visibility": "public" | "deck" | "internal"` at source.
- Externalization becomes a **filter** (`drop where visibility != public`), not a re-derivation.
- Rename internal-jargon field names (`wedge_archetype` → `archetype` / `fit_archetype`) so a field name can never be the leak.
- Principal names (e.g. Maldives deal principal, Mohamed El-Jana, Sheikha Maktoum) live in `internal`-tagged fields, structurally un-exportable.

### 3. Stable, namespaced, human-readable ids + canonical id registry
- Keep human-readable ids (good for debugging) but **namespace by type**: `city:…`, `org:…`, `route:…`, `bp:…`, `human:…`. Eliminates cross-type collisions and makes any reference self-describing.
- Routes: derive id deterministically from sorted endpoint ids (`route:{a}__{b}`) — never a hash, never a hand-typed composite (the malformed `…__rsg-neomsindalah` / `…__jakarta-direct-bali-600-nm` endpoints were exactly this failure).
- A generated `manifest.json` (id → {type, label, source_file, referenced_by[]}) is the registry every adapter and the Proposal Designer app reads. (Linter already walks all layers; promoting it to emit the manifest is a small step.)

## Sequencing (non-disruptive)
1. ✅ Integrity gate + known-gaps allowlist (done; modifies nothing).
2. Wire gate into seal + build pre-flight (next regen).
3. Resolve 5 tracked gaps: karimunjawa self-ref re-point, Miri + Likupang nodes, colombo decision.
4. Add `_visibility` tags incrementally as files are touched (already touching all partners/briefs this batch — fold in).
5. Emit `manifest.json` from the linter; point Proposal Designer app at it (workstream E benefits directly).
6. Backfill org↔city and human↔org joins so the 1,213 orgs / 648 humans become queryable per market (powers "who do we know in Bali" instantly).

## Why this is the scalable answer
- **Reusable on any medium:** deck, PDF, app, API all become thin projections of one spine.
- **Self-healing:** the gate makes the whole id-drift bug class impossible to ship.
- **Confidentiality by construction:** visibility is a property, not a fragile post-process.
- **The entity graph finally pays off:** joining orgs/humans to cities turns 1,861 dormant records into outreach intelligence.
