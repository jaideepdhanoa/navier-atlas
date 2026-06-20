# Partner Map Model — Universal Rollout Handoff (all partners)

**For:** Grok (deterministic materialize / seal / render-check loop)
**From:** Tasklet (registry binding + footprint rosters)
**Supersedes:** the Bolt/Yango-only pass in PR #54. This applies the binding/inheritance
contract to **every partner**, not just the named five.

## What changed

Every partner JSON with a registry presence now carries a **`network_footprint[]`** array of
**references** into `finance/model/corridors.json` — never copied data. The renderer resolves each
`registry_key` → cluster cities, corridor lines, briefs, and economics. **Add/enrich a shared market
(e.g. UAE) once and every partner that references it inherits automatically** (Careem, Uber, Bolt,
Yango all point at the UAE registry markets).

### Footprint entry shape
```json
{ "id": "bolt-uae", "registry_key": "bolt-uae", "covered": true,
  "tier": "sub_proposal", "render": "geometry", "map_promote": true,
  "label": "Uae", "country": "United Arab Emirates",
  "countries": ["United Arab Emirates"], "region": "MENA" }
```

- `registry_key` — the binding (null = not yet grounded → ground backlog).
- `covered` — a `markets[]` sub-proposal overlay exists (overlay only, never controls visibility).
- `tier` ∈ {flagship, sub_proposal, corridor_ready, coastal_aspirational, held_sovereign}.
- `render` ∈ {geometry, cluster_dots, anchor_dots, aspirational, held}.
- **`map_promote`** — honors Grok note #6: `false` keeps a market **brief-only / off the live map**
  until green-lit. Only fully-sealed covered sub-proposals are `true` today. Corridor-ready (incl.
  sealed-but-uncovered) are held `false`.

## Render / hold rules (folded in from Grok's reply)

1. No `non_marine` — gone everywhere; footprint is map + `coverage_note` prose only.
2. No card grid — `network_footprint` is **map-native render data**, not a UI tier list.
3. `coverage_note` prose preserved where it existed; generated (Grab/Uber style) where missing.
4. Sovereign-held (Israel, Lebanon) → `render:"held"`, **excluded from map_scope**.
5. Corridor-ready → `map_promote:false` (hold for green-light), still brief-eligible.
6. `map_scope` = sealed cluster cities of `map_promote:true` entries only — see `map-scope.json`.

## Coverage (23 partners bound; 24 await grounding)

| layer | partners |
|---|---|
| Dense registry (owned keys) | bolt (18 fp), yango (15) |
| Shared SEA + Gulf | grab (10), gojek (6) |
| Sub-proposals only, ungrounded geometry (null binding, aspirational) | uber (9), didi (7), lyft (6), ola (4), rapido (4), indrive (4), kakao-mobility (4), line (3) |
| Gulf / Indian-Ocean anchored | careem, qatar, saudi-pif, red-sea-global, jih-global, french-polynesia |
| Luxury-resort sub-proposals (ungrounded) | aman, four-seasons, six-senses, soneva, discovery-land |

**24 regional operators have no registry market yet** (ferries, hotel groups, authorities) — listed
in `ground-backlog.json` under `no_registry_presence`. They are structurally untouched until grounded.

## Ground backlog (`ground-backlog.json` — 78 tasks)

- **54 ungrounded sub-proposals** — a `markets[]` story exists but no registry geometry. Author
  cities/corridors into the registry → the partner inherits on the next loop with zero page edits.
  (Heaviest: uber 9, didi 7, lyft 6, ola/rapido/indrive/kakao 4 each.)
- **24 no-registry partners** — operating roster not yet in the registry at all.

## Tasklet next bites (research, not deterministic)

1. Ground Uber + Didi full operating rosters into the registry (largest inheritance unlock).
2. Reconcile Bolt/Yango footprints vs official operating-country lists (≈30 shown vs ~45 real).
3. Ground the regional operators' home networks.
