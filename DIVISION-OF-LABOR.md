# Navier Atlas — Tasklet × Claude: Division of Labor & Merge Protocol
_v2 · 2026-05-30 · the anti-drift contract_

## Principle
**Tasklet owns the GRAPH. Claude owns the EYES.**
Tasklet produces a clean, classified, demand-weighted, land-validated route graph plus
render-contract fields. Claude consumes that graph and makes it beautiful. Neither side
infers the other's half. The frozen render-contract JSON schema (below) is the seam —
changed only by mutual PR.

---

## 1 · Who owns what

### TASKLET — data spine · routing · demand · security · deploy · research
1. **Source of truth**: `.md` city files + all research, enrichment, outreach materials. (internal tree)
2. **The route graph** (the real fix that unblocked the visuals):
   - Routes built ON the boarding-point graph (BP↔BP, BP↔hub), never between bare city centroids.
   - Every endpoint canonicalized to a real node id (BP id or city id). No raw-label endpoints.
   - Layered network: `trunk` (high-demand backbones) · `regional` (cross-cluster) · `local` (BP↔BP capillaries).
   - No orphan boarding points — every boardable BP connects to ≥1 edge.
   - Every edge sea-routed + land-validated (0 land-crossings, hard gate).
3. **Demand model** — `traffic_weight` & `trip_purpose` (see `docs/route-demand-model.md`). Calibrated to
   observed flows (ferry pax, air O&D, border crossings, hotel keys). NOT graph degree.
4. **Confidentiality & deploy**: partition → externalization gate → land gate → deploy from `_dist/` →
   post-deploy substring sweep. **Tasklet is the ONLY side that deploys to production.**

### CLAUDE — render layer · aesthetics · interaction
1. **Density visuals**: line-weight & opacity by `traffic_weight`; edge-bundling where corridors overlap
   ("many overlapping high-traffic routes" look); zoom-band reveal — trunks always visible, regional mid-zoom,
   local capillaries on zoom-in.
2. **Node/cluster hierarchy**: hub flair from `degree`; cluster glyphs; declutter across zoom bands.
3. **Curve quality**: smooth (Catmull/bezier) but **clamped inside Tasklet's validated corridor** so smoothing
   never re-clips land. No geometric inference beyond cosmetic smoothing.
4. **Chrome**: legend/filters/panels polish; filter-color ↔ map-glyph parity; partner views (`?partner=<slug>`).
5. Works against the **sanitized `data-clean/` sample**; hands back the front-end template + `HANDOFF`.
   **NEVER** deploys to the live project, touches partition/security, or edits the graph.

---

## 2 · The seam — render contract (frozen JSON shapes)
```jsonc
// EDGE  (ROUTES feature.properties)
{
  "id": "edge__<from>__<to>",     // slug-only, no strategy words
  "from": "<node-id>",            // MUST be a BP id or city id — never a label string
  "to":   "<node-id>",
  "edge_class": "trunk|regional|local|intra-city",   // (+ legacy: hub-radial-spoke|intra-cluster-spoke)
  "traffic_weight": 0.0,          // 0–1 DEMAND signal (NOT degree): trunk 0.80–1.00 · regional 0.45–0.79 · local 0.10–0.40
  "trip_purpose": "commuter|business|tourism|luxury|local|mixed",  // partner-story tag; safe to surface in UI
  "platform": "Pioneer II|Quanta-LR",                // Quanta-LR renders amber (locked)
  "distance_nm": 0.0
  // geometry: clean sea-routed LineString, land-validated. Claude may smooth, not reroute.
}
// NODE (city) / BP (poi) properties
{ "id":"...", "degree": 0, "on_route": true, "hub_rank": 0.0 }
```
- **Render note**: map `traffic_weight` → line weight/opacity so trunks read heavy & locals light; `trip_purpose`
  is available to colour/legend by partner story.
- Rule: if a field isn't in this contract, Claude treats it as absent (graceful fallback).
- Rule: Tasklet never ships a field that fails the externalization gate.

---

## 3 · GitHub merge protocol (how we kill drift)

**Why git:** one canonical artifact, reviewable diffs, explicit conflict surfacing, and a permanent changelog.
The biggest historical conflict source — both sides editing the giant bundled `index.html` — is removed by the
**template/data split**: Claude edits the front-end *template*; Tasklet injects `data-clean/` to produce the
bundled `index.html`. They touch different files.

### Repo: `navier-atlas` (PRIVATE)
```
main            ← released state; mirrors live. ONLY Tasklet merges here.
 ├─ claude/render   ← Claude's front-end/render work
 └─ tasklet/data    ← Tasklet's refreshed data-clean/ + rebuilt index.html
```

### The loop
1. **Tasklet → repo**: on any data/graph change, Tasklet pushes refreshed `data-clean/` + current gate-passed
   `index.html` to `tasklet/data`, opens/updates a PR to `main`, version-stamped. (This just happened: demand model.)
2. **Claude → repo**: Claude branches from `main` into `claude/render`, edits the front-end template/render only,
   builds against `data-clean/`, commits, opens a PR to `main` with a `HANDOFF-FOR-TASKLET.md` changelog.
3. **Tasklet merges**: Tasklet reviews Claude's PR, pulls the template into the internal tree, runs the REAL
   pipeline (partition → enrich → build → **externalization gate** → **land gate** → `_dist/`), deploys, runs the
   post-deploy substring sweep, then merges the PR to `main` and pushes the resulting gate-passed `index.html`.
   **Tasklet's gates are the final authority** — a PR is not "done" until it ships clean.
4. **Conflict policy**: data ↔ template separation means conflicts should be rare; if `index.html` ever conflicts,
   it is regenerated by Tasklet (it's a build artifact), never hand-merged.

### Hard rules
- Claude **never** merges to `main`, never deploys, never edits anything under `.gitignore`.
- Vercel is **not** wired to auto-deploy from this repo — deploy stays Tasklet's gated CLI path from `_dist/`
  (auto-deploy would bypass the gates and the dist-isolation rule).
- Nothing internal ever enters git history (see `.gitignore` + repo `README`).

---

## 4 · Since the last merge (v15 → current)  — Tasklet changelog

**Headline: routes were rebuilt on the boarding-point graph with a real demand model.** Root cause of the
"routes cross land / connect to nothing / not dense" problem was that routes and the ~1,885 boarding points lived
in two disconnected id-spaces (~0% of BPs sat on a route; 340/400 route endpoints were raw label strings).

- **New `route_network.py`** (Tasklet-internal): layered demand-weighted network built ON the BP graph for the
  marquee markets (UAE, Singapore, Bali, Phuket) — `local` BP↔BP mesh + `regional`/`trunk` featured corridors.
  Endpoints land on real BP coords / real node ids.
- **Demand model locked** (`docs/route-demand-model.md`): `traffic_weight = expected_volume × navier_fit`,
  calibrated to observed flows; `trip_purpose` tag added. Your calls are reflected — Johor↔SG = commuter mass but
  boats win only a premium slice; SG↔Batam/Bintan = tourism-led; Tanah Merah surfaced as the cross-border hub.
- **Routing fixes**: nearest-open-water anchor search for lagoon/channel jetties; sea-facing re-points
  (Sharjah Corniche, Tanjung Belungkor); hand-waypoint override for sub-grid channels (Tanah Merah↔Batam).
- **Results**: boarding-point→route connectivity **18% → 88%** (Dubai/Langkawi/Fujairah 100%); **373 → 861 routes**;
  all 13 demand corridors route cleanly; **0/861 routes cross land**; deployed clean; leak sweep 0 hits.
- **New render-contract fields now in `data-clean/ROUTES.json`**: `traffic_weight` (demand), `trip_purpose`.

---

## 5 · Claude — focus from here (priority order)
1. **Render the density.** Map `traffic_weight` → line weight + opacity + glow so trunks read heavy and locals
   light. This is the single biggest visual win now that the data carries real demand. Edge-bundle overlapping
   corridors so high-traffic lanes visibly thicken.
2. **Zoom-band reveal.** Trunks always visible; regional appear mid-zoom; local capillaries fade in on zoom-in —
   so the map reads clean at world view and rich at city view.
3. **`trip_purpose` legibility.** Use it for legend/filter or subtle hue so commuter vs tourism vs luxury vs local
   reads at a glance (helps the Grab / RTA / hospitality framing).
4. **Hub hierarchy from `degree`.** Data-derived hub flair (not hardcoded); cluster glyph declutter across zoom.
5. **Curve smoothing clamped to corridor** — keep the v15 Catmull smoothing, ensure it never re-clips land at any zoom.
6. **Marquee-market polish first** (Singapore, Dubai, Abu Dhabi, Bali, Phuket) to the acceptance bar below, then
   we propagate. Hand back the front-end template + `HANDOFF-FOR-TASKLET.md`.

Open questions still pending Jaideep: (a) drop "Confidential" from header? (b) `--partner` per-build vs presentation-only
`?partner=` — recommendation: proceed with `--partner` build mode, feed real roster when shared.

---

## 6 · "Good looks like" acceptance bar (prove on marquee markets first)
Singapore · Dubai · Abu Dhabi · Bali · Phuket:
- [x] 0 land-crossings (0/861)
- [x] ≥90% of boarding points on a route (88% aggregate; Dubai/Langkawi/Fujairah 100%; 4 markets in 60–76% to lift)
- [ ] visible trunk/regional/local hierarchy with density where corridors overlap  ← **Claude**
- [x] cross-border story legible (Singapore↔Batam/Bintan/Desaru, Dubai↔Abu Dhabi↔RAK)
- [x] no raw-label endpoints anywhere in ROUTES
