# Changelog for Claude — 2026-06-01 — Routing re-application + endpoint-alias resolver

Supersedes the routing "still pending" note in the 2026-05-31 changelog. New sealed bundle in
`atlas-repo/data-clean/` (SEAL.json refreshed, sealed_at 2026-06-01T02:34Z). Build:
**cities=108, pois=10,364, routes=4,148 (0/4,148 cross land), briefs=112, partners=10, stories=12.**
All gates PASS: integrity (0 errors), conformance (112), externalization (0 hits), land-crossing (0/4148).

## 1. Harbour-overrides re-applied (validated open-water anchors)
`atlas-external/harbour-overrides.json` — 6 anchors moved to verified open water (robust 3 nm ring check):
- `miami-florida-usa` → [-80.08, 25.765] (Atlantic outside Government Cut, NOT inside Biscayne Bay)
- `palm-beach-florida-usa` → [-79.99867, 26.7717] (Atlantic outside Lake Worth Inlet)
- `sharjah-uae` → [55.35808, 25.4293]; `ras-al-khaimah-uae` → [55.93125, 25.86528] (Gulf)
- `muscat-oman` → [58.57967, 23.68667] (Gulf of Oman); `salalah-dhofar-oman` → [54.089, 16.92833] (Arabian Sea)
- Removed STALE key `salalah-oman` (real node id is `salalah-dhofar-oman`).

## 2. build.py routing hardening (3 changes)
- **`_sea_snap()`** — nudges any endpoint sitting on land to nearest open water (≤6 nm) before
  A*, AFTER the inland guard (so genuine inland nodes still drop). Harbour-override coords are
  already water → no-op.
- **Span-proportional grid pad** in the finer-grid A* retry: `pad = min(2.5, max(0.3, span*0.5))`,
  `target_cells=4000`, `max_detour=4.0`. Lets coast-rounding routes that exit the endpoint bbox
  resolve (Muscat→Salalah rounds Ras al Hadd east of both endpoints; Musandam/Hormuz to the north).
- **Bidirectional A* retry**: grid A* is direction-dependent (start/end cell snapping differs by
  heading). If forward route crosses land, retry the reverse direction and flip the path. This is
  what finally cleared Muscat↔Salalah (forward 2.38 km land → reverse 0.76 km clean).

## 3. Endpoint-alias resolver (NEW: `atlas-external/endpoint-aliases.json`)
The ~11 missing inter-corridor spokes were dropping for TWO reasons, both now fixed:
- **Synthetic `{owner}__{desc}` spoke ids** minted from .md prose (e.g.
  `palm-beach-florida-usa__miami-biscayne-bay`) → mapped to the real anchor.
- **Bare short-id endpoints** in legacy spine edges (`muscat`, `salalah`, `fujairah`, `sharjah`,
  `jakarta`, `doha`, `manama`, `jeddah`, `maldives`→`male-maldives`, etc.) → mapped to canonical
  `{place-slug}-{country-slug}` node ids.
- `build.py._resolve_cross_border()` now applies aliases FIRST; the edge loop resolves aliases
  BEFORE the country-shell/managed guards (so `vietnam__phu-quoc...`→`phu-quoc-vietnam` is no
  longer mistaken for the `vietnam` shell). **35 remaps applied** (was 7).
- `integrity/build_manifest.py` is now **alias-aware** (an aliased endpoint counts as resolved),
  so the integrity gate matches the renderer.

## 4. Edges that now render (verified in sealed ROUTES)
✓ Palm Beach↔Miami · ✓ Muscat↔Salalah · ✓ Fujairah↔Muscat · ✓ Sharm↔NEOM-Sindalah · ✓ Langkawi↔Penang
Sharjah↔RAK / Dubai↔Sharjah / Bali↔Komodo are intentionally owned by `route_network.py` (both
endpoints in MANAGED markets) — correct, not a miss.

## 5. known-gaps trimmed to 3 genuinely node-less endpoints
`integrity/known-gaps.json` unresolved_edge_endpoints = {Tarutao/Koh-Adang, AMAALA-Triple-Bay
(no standalone node), Likupang}. `brunei` now alias-resolves (`brunei-darussalam`).
Antigua↔St-Barths and Miami↔Nassau have NO edge in the build data (pruned upstream / never
authored) — not routing failures; if you want them, author the edge in supplemental-edges.json.

## 6. Build-env note (not a code issue)
Importing `partition_filter` at build end rewrites `output-external/nodes.json` to the 698-node
spine-only subset as a side-effect. Tasklet re-stages the full 739-node nodes.json before each
local build. FYI for your pipeline; no action needed on the sealed surface.

## Ship surface
Bake from `atlas-repo/data-clean/`. SEAL.json carries hashes + 3 gate verdicts.
