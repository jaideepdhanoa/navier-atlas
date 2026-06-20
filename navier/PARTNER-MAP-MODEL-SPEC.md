# Partner Map Model — Binding & Inheritance Contract

**Status:** canonical. Applies to **every** partner page (Grab, Uber, Didi, Careem, Bolt, Yango, … all 49).
**Owner split:** Tasklet authors the registry + footprint rosters (research/model). Grok runs the
deterministic materialization / seal / render-check loop from this contract.

## 1. The one rule

> The **shared corridor registry** (`finance/model/corridors.json`) is the **single source of truth**
> for cities, routes, and economics. A partner page never copies that data — it **references** it.
> Add a data point to a shared market (e.g. **UAE**) and **every partner that references that market
> (Careem, Uber, Bolt, Yango, …) inherits it automatically.** No per-partner hand-maintenance.

## 2. Data model

Each partner page carries a full-roster **`network_footprint[]`**. Each entry is a *reference*, not a copy:

```json
{
  "id": "uae",
  "registry_key": "uae-careem",   // pointer into corridors.json markets; null = not yet grounded
  "covered": true,                 // a markets[] sub-proposal overlay exists for this market
  "tier": "flagship",              // flagship | sub_proposal | corridor_ready | coastal_aspirational | inland_waterway | held_sovereign
  "render": "geometry",            // geometry | cluster_dots | aspirational | anchor_dots | held
  "label": "UAE", "country": "United Arab Emirates", "region": "MENA",
  "one_liner": "Dubai Marina ↔ Palm ↔ Abu Dhabi — the marquee, fully-built proposal."
}
```

- **`registry_key`** is the binding. The renderer resolves it → cluster city nodes, corridor lines,
  city/cluster briefs, and economics. Many partners may point at the **same** shared key (that *is* the
  inheritance: UAE → Careem + Uber + Bolt + Yango).
- **`covered`** is an *overlay flag*, not a separate dataset. `markets[]` holds the rich sub-proposal
  narrative for covered markets; it never duplicates geometry/economics.
- **No `corridors` count, no embedded city lists, no economics** live on the footprint entry. All derived.

## 3. Render rules (full footprint, not just sub-proposals)

The map shows **every** footprint market the partner operates in — covered or not:

| `render` | When | On the map |
|---|---|---|
| `geometry` | `registry_key` set **and** ≥1 sealed corridor | full cluster + corridor lines |
| `cluster_dots` | `registry_key` set, no sealed corridor yet | cluster city dots (no lines) |
| `anchor_dots` | no `registry_key`, anchor city nodes exist | anchor dots only |
| `aspirational` | coastal, ungrounded | **visibly aspirational** marker, never fake-sealed |
| `held` | `held_sovereign` | **not rendered** (sovereign hold) |

- `covered` controls only the **overlay** (sub-proposal styling / brief depth), **never** visibility.
- Bidirectional `↔` corridors on the front end; featured routes must render real geometry or read aspirational.

## 4. Removed (do **not** reintroduce)

- ❌ **No `non_marine_footprint`** and **no "non-marine" category/word** anywhere. Landlocked/no-water
  markets simply have no registry geometry and drop off the map — `null` beats confidently-wrong.
- ❌ **No network-footprint card grid.** Footprint lives on the **map** + the **`network_thesis.coverage_note`**
  prose (Grab/Uber style). The roster array is render data, not a UI card list.

## 5. Inheritance loop (Grok, deterministic)

For every partner, on registry change:
1. Resolve each `network_footprint[].registry_key` → cluster cities, corridors, briefs, economics.
2. Materialize `scope_city_ids` / render scope from the resolved set (held → excluded).
3. Render-check: **assert the full footprint renders** (each non-held entry shows at its `render` level),
   anchor-city ID-match, no orphan ids, `null` where ungrounded.
4. Emit the economics sidecar from the inherited registry economics — never hand-keyed per partner.

## 6. Ground backlog (Tasklet research)

Any footprint entry with `registry_key: null` (and `render` ≠ `held`) is a **grounding task**: author the
market's cities/corridors/economics into the shared registry. Once added, **all referencing partners inherit
on the next loop** with zero page edits. Current backlog: see `out/ground-backlog.json` (Bolt/Yango coastal+inland,
all Uber non-GCC, all Didi LatAm).
