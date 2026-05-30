# Claude Code Brief — Rich City Panels, Partner Pitch Mode & Route Labels

**From:** Tasklet · 2026-05-30
**Context:** We're turning the atlas into a partner-facing *pitch document*. Tasklet owns the data &
content; you own the render. Architecture: `partner-pitch/ARCHITECTURE.md` (in repo under docs/ when pushed).
All data below is live in production now and sealed in `data-clean/`.

---

## 0. Preserve your existing fixes
Keep your F-01 route-render fix, the `symbol-sort-key` collision-thinning on `priority-labels`
(do NOT restore `text-allow-overlap:true`), the Quanta-LR hero treatment, and PARTNER_VIEWS.
Tasklet rebuilt from your PR#2 render, so these are baked into the current `template.html`.

---

## 1. ROUTE TOOLTIPS — use the new clean labels (quick win, do first)
Every route now carries clean, human endpoint fields. **Stop deriving the tooltip from `from`/`to`
ids** (that's why slugs like `salalah-dhofar-oman__hasik` and truncated `__lusail-...-waldorf-r`
leaked). New `properties` on every route:

| field | example |
|---|---|
| `label` | `"Doha → Dubai"` · `"Jeddah → Shura (RSG anchor)"` · `"Salalah → Hasik fishing harbour"` |
| `from_label` / `to_label` | clean endpoint names |
| `from_city` / `to_city` | parent city (short) — every route now reads **City → City** |

**Action:** route hover/click tooltip should show `properties.label` for the origin→destination line
(keep platform · distance_nm · est-time · trip_purpose chips as you have them). This alone fixes all
the underscore / "middle of nowhere" tooltips in Jaideep's screenshots.

---

## 2. NEW BAKED GLOBALS — add two placeholders to template.html
Tasklet's `build.py` already injects these (no-op until you declare them). Add to the data `<script>`:
```js
const CITY_BRIEFS = __CITY_BRIEFS__;   // { city_id: {…brief} }
const PARTNERS    = __PARTNERS__;       // { partner_id: {…proposal} }
```
Schemas: `partner-pitch/schema/city_brief.schema.json`, `partner_proposal.schema.json`.
Reference copies of every blob are in `data-clean/city_briefs/*.json` and `data-clean/partners/*.json`.

---

## 3. RICH CITY SIDE PANEL  (replaces the generic "Select a node")
On city click, if `CITY_BRIEFS[cityId]` exists, render a pitch-synthesis panel. Sections, in order:
1. **Hook** — `display` + `tagline` + `summary`
2. **Why marine mobility here** — `demand_signals[]` as labeled stat chips (`label` / `value` / `note`)
3. **Use cases** — `use_cases[]` grouped/badged by `archetype` (public_transit · super_app · tourism · luxury_charter · corporate), each `title` + `body` + `platform` badge
4. **How Navier fits** — `navier_fit.pioneer_ii` (mint) and `navier_fit.quanta_lr` (amber)
5. **Signature routes** — `signature_routes[]` (+ optionally auto-list live routes where `from_city`/`to_city` == this city, sorted by `traffic_weight`)
6. **For a transport authority** — `transit_planning`
- If `?partner=<slug>` is active and `partner_overlays[slug]` exists, surface `lead_with` + `note` at top (reorders the emphasis).
- Cities without a brief: keep current lightweight context panel.

---

## 4. PARTNER PITCH MODE  (`?partner=<slug>`) — the carousel
When `PARTNERS[slug]` exists, the side panel becomes the **pitch document** and a phase carousel drives the map.

**Side panel layout:**
- `hero.title` + `hero.subtitle` + `hero.what_we_do_together`
- `why_now`
- **Phase carousel** (prev/next + dots), one card per `phases[]` item:
  `label`, `boats`, `narrative`, `kpis[]` (chip grid). Bottom: `close.title` + `close.body`.

**Carousel step → map state (the key interaction):**
On phase change, for `phase[i]`:
- `flyTo(phase.map_focus.camera)` (lng/lat/zoom)
- **Filter routes:** show only routes touching `phase.cities`. `route_scope:"intra"` = routes whose
  `from_city` AND `to_city` are both in `phase.cities`; `route_scope:"all"` = any route with either
  endpoint in `phase.cities`. Dim/hide everything else.
- **Highlight cities** in `phase.cities`; fade others.
- Side panel shows that phase's `narrative` + `kpis` + `featured_routes[]`.
This makes the page literally walk the rollout: Phase 1 (few boats/routes) → Phase 2 (full network)
→ Phase 3 (new cities). See `partners/grab.json` (Singapore → +Riau → +Bali/Phuket) and `partners/dubai-rta.json`.

**Exemplars to test:** `?partner=grab` and `?partner=dubai-rta`.

---

## 5. PER-PARTNER BUILD  (your deploy lane)
`atlas build --partner=<slug>`: (1) scope data to that partner's `cities`/phases + their stories,
(2) inject `window.__PARTNER_BUILD__='<slug>'` (already in your render hook), (3) run gates +
cross-partner leak sweep, (4) emit per-partner `SEAL.json`, (5) output `_dist/<slug>/index.html`.
Recommended: a public `navier-partners` project serving path-based `/grab`, `/dubai-rta`; keep the
all-data `navier-atlas` project SSO-protected. (Roster grows as Tasklet authors more `partners/*.json`.)

---

## 6. Note on Quanta-LR data (may shift)
Tasklet has a Quanta-LR curation review pending Jaideep's go (`partner-pitch/QUANTA-LR-CURATION-REVIEW.md`):
~48 ≤70 nm routes may reclassify Quanta-LR→Pioneer II, and ~6 placeholder spurs may drop. Bind to
`from_city`/`to_city`/`platform` (not hardcoded ids) so your views survive the recut.

---

## Summary of what changed in this push
- `build.py` + new `route_labels.py`: clean `label`/`from_label`/`to_label`/`from_city`/`to_city` on every route.
- `build.py`: bakes `__CITY_BRIEFS__` / `__PARTNERS__` (add the two placeholders to use them).
- New content: `partner-pitch/` (architecture, schemas, 3 city briefs, 2 partner proposals).
- Production redeployed clean (0 leaks, 0/1504 land crossings), sealed, on `main`.
