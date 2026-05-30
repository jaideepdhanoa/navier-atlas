# Work Queue — Claude Code (render + deploy)
_v3 · 2026-05-30 · supersedes prior queue. You now own publish-to-Vercel (see DIVISION-OF-LABOR.md v3 §3)._

## 0 · Take over deploy (one-time setup)
- [ ] Confirm `VERCEL_TOKEN` is in your environment (Jaideep provisions it). Basemap is CARTO (public) — no map-tile secret needed.
- [ ] Implement the **deploy pre-flight** (DIVISION-OF-LABOR.md §3), all three checks, as a script you run before every `vercel deploy --prod`:
      1. **hash match** — recompute canonical sha256 of each injected blob, compare to `data-clean/SEAL.json`; mismatch → abort.
      2. **substring grep** — grep final `index.html` against `docs/EXCLUSION-TOKENS.txt` (case-insensitive regex); any hit → abort.
      3. **MapLibre smoke test** — load the built style headless; assert 0 rejected layers AND route line layers present & bound to `routes`.
- [ ] After a green deploy, post one line to `#tasklet-jaideep`: `✅ deployed <commit> · routes rendering · pre-flight clean`.

## 1 · BLOCKER — fix route rendering (QA F-01) 🔴
The QA viewer confirmed **no route line ever draws** — `route-glow`/`route-p2`/`route-qlr` are rejected by MapLibre style validation:
> *"zoom" expression may only be used as input to a top-level "step"/"interpolate"* · *Only one zoom-based step/interpolate subexpression may be used.*
- [ ] Rewrite the offending `line-width`/`line-opacity` paint expressions so each property has **at most one** top-level zoom `interpolate`/`step`, and any `traffic_weight`-driven term is a **data expression** (`["get","traffic_weight"]` via `interpolate` on the property), not nested inside the zoom expression. Combine with `["*", ...]` at the value level or precompute a single ramp.
- [ ] Same fix for `city-hub-glow.paint.circle-radius` (QA F-12 — dropped by the same error class).
- [ ] Your pre-flight §3.3 smoke test must catch this class going forward (assert these layers register).
- **Acceptance:** Pioneer II solid + Quanta-LR amber-dashed lines visible in Singapore/Dubai/Abu Dhabi/Bali/Phuket; toggles (F-05) and legend (F-04) then resolve downstream.

## 2 · Determinism — render baked routes verbatim (QA F-11)
- [ ] Route count changed across reloads (874→923) → there is **client-side route synthesis** somewhere. Remove it. Render the baked `ROUTES` array verbatim; show the count from `SEAL.json` (`blobs.ROUTES.count`). The graph is Tasklet's; the render must not generate edges.

## 3 · Camera deep-links (QA F-02)
- [ ] On load AND on `hashchange`, **read** `#camera=LNG,LAT,ZOOM` and move the map to it (currently only written, never read). Enables shareable "look at Singapore" links and reproducible QA citations.

## 4 · First-load layout (QA F-06, F-07, F-08)
- [ ] Make the **network the hero** on load; panels frame, don't blanket (F-06).
- [ ] Stop the legend/MAP-KEY panel from occluding the headline stats card at default width (F-07).
- [ ] Side panel must reflect current context at city zoom, not the stale world-view intro; kill the dead empty space (F-08).

## 5 · Marker declutter (QA F-10) + orphan dots (F-09)
- [ ] Offset/declutter the Singapore city dot vs the overlapping ferry/cruise glyph (F-10).
- [ ] F-09 (orphan route-node specks) resolves once F-01 draws the connecting lines — verify after F-01.

## 6 · Cold-load perf (QA F-13, low confidence)
- [ ] Multi-second black-map on cold load + market switches (CARTO tiles). Consider a basemap loading state / preconnect; confirm on a real device. Low priority.

## 7 · Carry-forward render polish (from v2 queue, still wanted)
- [ ] `traffic_weight` → line weight/opacity/glow density; edge-bundle overlapping corridors.
- [ ] Zoom-band reveal (trunk always; regional mid; local on zoom-in).
- [ ] `trip_purpose` hue/legend legibility.
- [ ] Hub flair from `degree`; cluster declutter.
- [ ] Keep marquee-city always-on labels (Tasklet added `priority_city` bucket — 13 cities; render them unclustered/always-on) and the chain-anchor named pins.

## Notes
- You consume ONLY `data-clean/` (sealed). Never edit the graph/demand/partition. Need a new data field? Request via PR/HANDOFF; Tasklet adds it to the render contract and re-seals.
- The QA report's 5 blocked route-correctness checks (land-crossing, dangling, curve, density, trip-purpose colour) become testable once F-01 ships — hand back to Cowork.
