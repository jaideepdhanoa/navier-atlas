# Grok seal mandate — Grab Thailand upper-Gulf depth pass (2026-06-23)

**Source of truth = GitHub `jaideepdhanoa/navier-atlas` main.** This zip is an **input** package, not a hand-back.
Baseline: all existing Thailand BPs/briefs/corridors already on `main`. This pass adds the **upper-Gulf ring**
(Eastern Seaboard + Royal Coast), 3 new cities, and depth to existing briefs.

## Mandate
1. **Mint 3 new city geometries + seal their BPs** (`boarding-points/*.json`): `hua-hin-thailand` (2 BPs),
   `cha-am-thailand` (1 BP), `koh-samet-thailand` (2 BPs incl. Ban Phe mainland gateway). Coordinates are
   `curated_seed` precision — **regeocode/snap + water-adjacency check**. **0 silent drops** on these 5 BPs.
2. **Build + bind 5 NEW near-term Pioneer II mesh routes** (currently `route_id: null`,
   `_link_status: pending-seal-thailand-depth`). See `inputs/GRAB-THAILAND-DEPTH-BINDSET.json`:
   - `bangkok-thailand → pattaya-thailand` (46nm) — gulf gateway line
   - `pattaya-thailand → koh-samet-thailand` (40nm)
   - `koh-samet-thailand → koh-samet-thailand` (Ban Phe↔Na Dan, 3nm)
   - `hua-hin-thailand → pattaya-thailand` (58nm) — **MARQUEE cross-Gulf line**
   - `hua-hin-thailand → cha-am-thailand` (14nm)
   Apply water/land gates. **Range-gate: all ≤58nm ⇒ Pioneer II** (confirm; never leave a long leg on a 70nm boat).
3. **Render 2 Quanta-LR long-horizon roadmap legs `amber-dashed`** (`_link_status: roadmap-quanta-lr`):
   `pattaya↔koh-samui` (209nm), `bangkok↔koh-samui` (243nm). **In Quanta-LR range but journey-time-gated**
   (~10.5h / ~12h vs a 1h flight) — roadmap only. **Do NOT draw them as solid near-term corridors.**
4. **Seal the 5 markets** (3 existing + 2 new). `eastern_seaboard` + `royal_coast` are net-new
   `PARTNER_VIEWS` scope (derive `scope_city_ids` by ID-match from `partners/grab-thailand-scope.json` —
   never hand-list). Pattaya/Koh Larn/Koh Chang **moved** from the `bangkok` market into `eastern_seaboard`.
5. **Seal 11 city briefs** (`city_briefs/*.json`): 3 new, Phuket **promoted to full flagship parity**, and
   7 connected-city stubs **deepened** (pattaya, koh-larn, koh-chang, krabi, koh-phi-phi, koh-phangan, koh-tao).
6. **Economics cascade (after seal):** `eastern_seaboard` + `royal_coast` are `economics_status: pending-seal`
   — **no TAM fabricated** (null beats confidently-wrong). Once route_ids bind, cascade via
   `aggregate.py → growth.py → splice_growth_into_partner.py → build_transparent_sheet.py → build_economics_sidecar.py`
   using `inputs/GRAB-THAILAND-DEPTH-DEMAND-ANCHORS.json` (source-tiered; no 30k placeholder). Add a Thailand
   `country-reference.json` row if missing (avoid the silent Singapore-opex fallback). CAPEX = $600K/vessel (non-US/EU).
   SOM floor is the honest sell — do not inflate; captive rules N/A (these are contested ride-hail corridors at ~10% capture).

## Anchor-city ID-match (render-gap guard)
Every `anchor_cities` / `connected_cities` id must resolve to a sealed atlas `city_id` (internal id, not filename).
New ids to create: `hua-hin-thailand`, `cha-am-thailand`, `koh-samet-thailand`. Existing must already resolve
(`pattaya-thailand`, `koh-larn-thailand`, etc.). A missed match renders an empty market.

## ID-correction watch (do not regress)
The Dominic de-attribution fix (PR #87) is upstream — these files are already de-attributed. Do not reintroduce
removed attribution.

## Acceptance gate (your QA report must show)
- 5 new BPs sealed (regeocoded/snapped); **0 silent drops**; each carries a source id.
- 5 near-term routes built + `route_id` bound; **0 land-crossings post-allowlist**; Pioneer II range-gate proven (≤58nm).
- 2 Quanta-LR legs render `amber-dashed` roadmap; **no solid Samui marathon corridor** exists.
- 5 markets render; `eastern_seaboard` + `royal_coast` views render real geometry; Pattaya/Koh Larn/Koh Chang
  now under `eastern_seaboard`.
- 11 briefs sealed; Phuket at flagship parity.
- `economics_url` wired; new-market TAM rungs flagged `pending-seal` until cascade completes (not faked).
- Counts: BPs sealed/dropped(+reason), routes built/culled, before→after market+route totals.

## Two-worlds reminder
Economics (Sheets/tracker) and Atlas (render graph) are separate. After you bind route_ids and cascade,
the front end must show new-market geometry **and** non-stale economics provenance.
