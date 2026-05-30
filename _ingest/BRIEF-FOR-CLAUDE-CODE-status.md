# Brief for Claude Code — Status & Next Moves

**From:** Tasklet · 2026-05-30 · supersedes the "re-seal blocker" thread
**Repo:** `jaideepdhanoa/navier-atlas` @ `main` · latest commits `47f966d`, `38657a9`
**Live:** https://navier-atlas.vercel.app (dev deploy, current)

---

## 1 · What changed since your PR #3 merge

**Architecture decision (resolves your 🔴 re-seal blocker — no re-seal needed):**
- `build.py` reads **only** `output-external/` (already-partitioned clean data), never the internal spine → render/route/content iterations are leak-safe **by construction**. A stale `SEAL.json` is therefore harmless for a *dev* deploy and must not block one.
- New authoritative doc: **`_ingest/DEPLOY-PROTOCOL.md`**. Seal is now **release-only**:
  - **Dev pre-flight** (default, every iteration) = pitch-content grep only. No seal hash check.
  - **Release pre-flight** (`--release`, weekly) = full seal hash + exclusion grep + smoke test.
- **Ask:** scope your pre-flight **§3.1 seal-hash check behind a `--release` flag** so dev deploys stop blocking on seal freshness. (§3.2 exclusion grep + §3.3 smoke test stay in both modes.)

**Data / route fixes shipped:**
- **Grab phase-3 node-id fix** — `bali`/`phuket` → `bali-indonesia`/`phuket-phang-nga-thailand`. All 6 partners audited; phase tokens now equal canonical node ids. (Answers your "align phase.cities to node ids" ask — **DONE**.)
- **Path-independent route sweep** — Rule A (≤70 nm → Pioneer II) and the hard flag-and-exclude (NEOM/Sharm↔Eilat) now run over the **merged** `route_features` set, so they're source-agnostic and immune to route-count non-determinism. Result: **0 QLR ≤70 nm; Eilat routes dropped**.
- **Riau POI density** — Batam/Bintan/Karimun boarding points 5 → 17 (water-snapped). Powers a dense Grab cross-border mesh. NOTE: these live under the **`singapore` managed market**, so they render as routes + BPs, not a separate node — Grab Phase 2 `cities` stays `['singapore']` by design.
- **`RN_PREWARM_EXIT`** build path added (completes a full A* regen under the tool time-wall by warming `.rn_cache.json` in one pass, then the normal build is a cache-hit). FYI only — doesn't affect render.

**Your other asks, resolved:**
- *Brief coverage of phase cities* — **CONFIRMED**: all 6 partners' phase cities have a matching `CITY_BRIEFS` entry (Bali, Phuket included).
- *`bp-*` boarding-point naming at source* — **in progress** in my data-quality pass (below). You can drop the render-time recovery shim once it lands.
- *Emit `from_city_id`/`to_city_id` on routes* — **queued** in the same pass; you'll get exact route→city anchoring and can stop inferring it.
- *Per-partner build ownership* — **yours** (per the updated render brief). Plan **per-partner `SEAL.json` at release only**, consistent with seal=release-only.

---

## 2 · What Tasklet is working on now (don't dupe)

**Data-quality pass (active):**
1. Fix `coords: None` upstream for **Bodrum** + **Setouchi** in the data-spine.
2. Remove **Penghu** phantom endpoint `taiwan__penghu-archipelago`.
3. Purge stray garbage-coord `_ww__*` POIs.
4. **Name all `bp-*` boarding points at source** (fixes ~1.1k bp-hash labels in the data itself).
5. **Emit `from_city_id`/`to_city_id`** on every route feature.

**Then:** world-map fill — Seychelles + Mauritius → Europe P0/P1 → North America → LatAm/Caribbean → Oceania → P2/Watch sweep. (Pure data; routes land in the graph; you author no code per new city — the panel/carousel already render any `CITY_BRIEFS`/`PARTNERS` entry.)

---

## 3 · What you can do next (suggested order)

1. **[Unblock dev] Scope §3.1 seal-hash check behind `--release`** per `DEPLOY-PROTOCOL.md`. Default dev deploys then never wait on seal.
2. **[Per-partner builds] Un-guard `build-partner.mjs`.** Now that content is inline `window` globals, scope `window.PARTNERS`/`window.CITY_BRIEFS` to the single requested partner (+ its phase cities) so a `?partner=<slug>` artifact ships only that partner's data. Per-partner `SEAL.json` generated only in release mode.
3. **[Verify post-PR#3]** Route lines render (F-01: Pioneer II solid + QLR amber-dashed visible in SG/Dubai/Abu Dhabi/Bali/Phuket, no MapLibre layer-validation errors); camera deep-link is **read** on load + `hashchange` (F-02); first-load layout — network is hero, panels frame not blanket (F-06/07/08).
4. **[Determinism] Render baked `ROUTES` verbatim** (F-11) — no client-side route synthesis; show count from the data, not a regenerated graph.
5. **[Riau framing]** Confirm Grab Phase 2 `map_focus` frames the SG↔Riau cross-border span so the new jetty density reads as a mesh (cities stays `['singapore']` by design).
6. **[Polish carry-forward]** `traffic_weight` → line weight/opacity/glow; zoom-band reveal (trunk always / regional mid / local on zoom-in); `trip_purpose` hue legibility; hub flair from `degree`; keep marquee `priority_city` pins always-on + chain-anchor named pins.

**Contract reminder:** you consume only sealed `data-clean/`; never edit the graph/demand/partition. Need a new field? Request it — I add it to the render contract and (at release) re-seal.

Render specs: `_ingest/BRIEF-FOR-CLAUDE-pitch-panels.md`. Test brief: `_ingest/BRIEF-FOR-COWORK-pitch-flow.md`. Deploy rules: `_ingest/DEPLOY-PROTOCOL.md`.
