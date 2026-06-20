# Tasklet → Grok corridor handoff — 2026-06-20 (Egypt + Qatar node repair)

First **GitHub-native** Tasklet→Grok handoff (replaces the Downloads-zip model — see note at bottom).

## What changed in `corridors.json`
Master: `finance/model/corridors.json` (Tasklet-owned). This is the full file; diff is scoped to 2 markets / 21 corridor rows.

### 1. Egypt — broken node IDs (why Grok minted 0 Egypt routes) — `bolt-egypt` + `yango-egypt`
Every Egypt corridor referenced **gold city chips that don't exist** (`hurghada-egypt`, `el-gouna-egypt`),
and three sub-regions were *all* mis-tagged to `hurghada-egypt`. Fixed **geography-aware** (not a blanket rename):

| Corridor group | old node(s) | new gold chip |
|---|---|---|
| Hurghada / El Gouna intra (Giftun, Sahl Hasheesh, Soma Bay, Abu Tig, Hurghada↔El Gouna) | `hurghada-egypt` / `el-gouna-egypt` | `hurghada-el-gouna-egypt` |
| Sharm area (Ras Mohammed / Tiran, Dahab) | `hurghada-egypt` (wrong) | `sharm-el-sheikh-egypt` |
| Cairo Nile (Maadi↔Zamalek, Maspero↔Warraq) | `hurghada-egypt` (wrong) | `cairo-egypt` |
| Hurghada/El Gouna → Sharm (inter-city) | `hurghada-egypt`→`sharm` | `hurghada-el-gouna-egypt`→`sharm-el-sheikh-egypt` (stays `aspirational:true` — long cross-gulf, no active ferry) |

- **20 node remaps** total (10 per market). All endpoints now resolve to gold chips
  (`hurghada-el-gouna-egypt`, `sharm-el-sheikh-egypt`, `cairo-egypt`). Verified: 0 nodes off-gold.
- Added `endpoint_boarding_points` to the **Hurghada → El Gouna** row (the `no_bp` row):
  `{from: "Hurghada Marina", to: "Abu Tig Marina, El Gouna"}`.
- Set `country: "Egypt"` on both markets (was `null` → was silently inheriting **Singapore opex**, golden rule #8).
- **Intentional holds kept:** Hurghada/El Gouna → Sharm stays `aspirational:true` (already carries
  `gcn-73d7e2f19c-bolt`); yango copy mirrors with `aspirational:true`. Do not chase pin.

**Expected after your mint:** `gcn-6f2754b63b-yango` (Hurghada→El Gouna) pins; all Hurghada/Sharm/Cairo
intra-city corridors resolve via `endpoint_boarding_points` fuzzy-match to the sealed bp-* set.

### 2. Qatar — `gcn-e2b0929d6f-qatar` Doha → Al Wakrah Marina (the 1 Qatar `mint_gcn` row)
- Node IDs were **swapped** vs labels (row reads Doha→Al Wakrah Marina but nodes were `al-wakrah-qatar`→`doha`).
  Corrected to `doha` → `al-wakrah-qatar` (both confirmed valid gold chips — the `rn-1066679a7f79` bolt/yango
  twin already minted on them).
- Added `endpoint_boarding_points`: `{from: "Doha Corniche (Al Bidda / Mina District ferry point)",
  to: "Al Wakrah Marina"}` — supplies the missing `from_bp` (triage already resolved `to_bp=bp-b7acff0504`).

## NOT in this handoff (deliberately deferred — flagged for you)
- **Jakarta/Bangkok `gcn-*-shared` rows** (triage filed under `bali`/`phuket`): gold minted `gcn-…-shared`
  IDs that were **never backfilled into the registry** (my rows carry `ics-*` or null). The same-node loops
  (Pantai Laguna↔itself, Batavia↔itself, ICONSIAM↔itself, Chalong↔itself, Benoa↔itself) are genuine
  **single-pier `aspirational_intra_city`** — structural holds, *not* failures; no honest second endpoint exists.
  → Recommend a **gcn-backfill sync** (gold `gcn-*-shared` → registry `route_id`), not fabricated endpoints.
- **Turkey (20) + the 37 `one_bp` corridors**: these need **new boarding-point research** (`seal_bp`), not a
  corridors.json edit. Coming as a dedicated BP-research handoff (Lagos, Croatia, Singapore, Italy, Turkey coastal…).
- **Turkey per-city node-chip split** (Bodrum/Antalya/Çeşme off `istanbul-turkey`): paired with that BP batch.

## Ingest
Replace the corridors copy you read today with this `corridors.json`. After you mint, **backfill the new
`route_id`s onto the matching rows** so the next sidecar rebuild stays deterministic (your §7 rule).

---
**Channel note (for Jaideep's question):** this is the first handoff shipped as a **GitHub PR** instead of a
Downloads zip. Source of truth stays singular (the repo), Grok gets a reviewable diff, and the stale-local-mirror
problem disappears. Proposing all future Tasklet→Grok input handoffs go this way.
