# Claude Code Brief — Rich City Panels & Partner Pitch Mode (v2 — data is LIVE)

**From:** Tasklet · updated 2026-05-30
**Context:** We're turning the atlas into a partner-facing *pitch document*. Tasklet owns data & content; you own render.
Architecture: `partner-pitch/ARCHITECTURE.md`. **Everything below is already live in production** at
https://navier-atlas.vercel.app and sealed in `data-clean/`.

> **What changed since v1:** (a) The pitch data is now injected as **`window.CITY_BRIEFS` / `window.PARTNERS`
> globals — no placeholder wiring needed; consume them directly.** (b) The **Quanta-LR A+B+C+D recut shipped**
> (section 6 is resolved, not pending). (c) Content grew to **19 city briefs + 6 partner proposals**.
> (d) New: the **node-ID matching contract** in §2.5 — read it, it's the #1 silent-fail trap.

---

## 0. Preserve your existing fixes
Keep your F-01 route-render fix, the `symbol-sort-key` collision-thinning on `priority-labels`
(do **NOT** restore `text-allow-overlap:true`), the Quanta-LR hero treatment, and PARTNER_VIEWS.
Tasklet rebuilt from your PR#2 render, so these are baked into the current `template.html`.

---

## 1. ROUTE TOOLTIPS — use the clean labels (already shipped; verify you bind to them)
Every route carries clean human endpoint fields. **Do not derive tooltips from `from`/`to` ids.**

| field | example |
|---|---|
| `label` | `"Doha → Dubai"` · `"Sharm El Sheikh: Jaz Mirabel — Nabq Jetty → Nuweiba Port"` |
| `from_label` / `to_label` | clean endpoint names |
| `from_city` / `to_city` | parent city (short) — every route reads **City → City** |

Tooltip should show `properties.label` for origin→destination (keep platform · distance_nm · est-time ·
trip_purpose chips). This already fixed all the underscore / "middle of nowhere" / `Bp <hash>` tooltips —
including a latent **906-route** local-mesh hash-label bug Tasklet fixed in this cycle.

---

## 2. THE DATA IS LIVE AS GLOBALS — consume directly
`build.py` injects, right before `</body>`:
```js
window.CITY_BRIEFS = { city_id: {…brief} };   // 19 cities
window.PARTNERS    = { partner_id: {…proposal} }; // 6 partners
```
No `__CITY_BRIEFS__`/`__PARTNERS__` placeholder is required anymore (build falls back to the global-inject if
the placeholders are absent — which they currently are). If you'd rather bind via the data `<script>`, you can
still add `const CITY_BRIEFS = __CITY_BRIEFS__;` and the build will fill it; otherwise just read `window.*`.

**Live keys (verified):**
- `CITY_BRIEFS` (19): abu-dhabi-uae, bali-indonesia, bangkok-thailand, colombo-sri-lanka, doha-qatar,
  dubai-uae, hong-kong, jakarta-batam-indonesia, jeddah-ksa, komodo-flores-indonesia, lombok-indonesia,
  male-maldives, manama-bahrain, muscat-oman, neom-sindalah-ksa, phuket-phang-nga-thailand,
  red-sea-global-ksa, sharm-el-sheikh-egypt, singapore
- `PARTNERS` (6): grab, dubai-rta, careem, abu-dhabi-itc, singapore-mpa, red-sea-global

Schemas: `partner-pitch/schema/city_brief.schema.json`, `partner_proposal.schema.json`.
Reference copies: `data-clean/city_briefs/*.json`, `data-clean/partners/*.json`.

### 2.5 NODE-ID MATCHING CONTRACT (read this — #1 silent-fail trap)
`CITY_BRIEFS` keys, `partner.phases[].cities[]` tokens, and the map's **node feature ids** all use the same
canonical id space (e.g. `bali-indonesia`, `phuket-phang-nga-thailand`, `dubai-uae`, `singapore`).
Tasklet already fixed a Grab mismatch (`bali`/`phuket` → `bali-indonesia`/`phuket-phang-nga-thailand`).

**Two render rules that follow from this:**
1. **Child/split nodes resolve to the parent brief.** Split anchors look like `parent__child`
   (e.g. `bali-indonesia__nusa-lembongan-penida-ceningan`). On click, resolve the brief with
   `CITY_BRIEFS[id] ?? CITY_BRIEFS[id.split('__')[0]]` so children inherit the parent's pitch panel.
2. **Phase highlighting must also match children.** A phase listing `["singapore","bali-indonesia"]` should
   light the anchor **and** its `parent__*` children. Treat a city token as a prefix: highlight any node where
   `nodeId === token || nodeId.startsWith(token + "__")`.

---

## 3. RICH CITY SIDE PANEL (replaces generic "Select a node")
On city click, if a brief resolves (per §2.5), render a pitch-synthesis panel. Sections in order:
1. **Hook** — `display` + `tagline` + `summary`
2. **Why marine mobility here** — `demand_signals[]` as stat chips (`label` / `value` / `note`)
3. **Use cases** — `use_cases[]` badged by `archetype` (public_transit · super_app · tourism · luxury_charter · corporate), each `title` + `body` + `platform` badge
4. **How Navier fits** — `navier_fit.pioneer_ii` (mint) and `navier_fit.quanta_lr` (amber)
5. **Signature routes** — `signature_routes[]` (+ optionally auto-list live routes where `from_city`/`to_city` == this city, sorted by `traffic_weight`)
6. **For a transport authority** — `transit_planning`
- If `?partner=<slug>` active and `partner_overlays[slug]` exists, surface `lead_with` + `note` at top.
- Nodes without a resolvable brief: keep the current lightweight context panel.

---

## 4. PARTNER PITCH MODE (`?partner=<slug>`) — the carousel
When `PARTNERS[slug]` exists, the side panel becomes the **pitch document** and a phase carousel drives the map.

**Side panel layout:** `hero.title` + `hero.subtitle` + `hero.what_we_do_together`; then `why_now`; then the
**phase carousel** (prev/next + dots), one card per `phases[]` item: `label`, `boats`, `narrative`,
`kpis[]` (chip grid). Bottom: `close.title` + `close.body`.

**Phase object shape (verified):**
`{ n, label, boats, cities[], route_scope, featured_routes[], narrative, kpis[], map_focus:{camera:{lng,lat,zoom}} }`

**Carousel step → map state (the key interaction).** On phase `i`:
- `flyTo(phase.map_focus.camera)`
- **Filter routes by `route_scope`:** `"intra"` = routes whose `from_city` AND `to_city` are both in
  `phase.cities`; `"all"` = any route with either endpoint in `phase.cities`. Dim/hide the rest.
- **Highlight cities** in `phase.cities` (prefix-match children per §2.5); fade others.
- Side panel shows that phase's `narrative` + `kpis` + `featured_routes[]` (display strings, render as-is).

This walks the rollout literally: Phase 1 (few boats/routes) → Phase 2 (full network) → Phase 3 (new cities).
**Exemplars to test:** `?partner=grab` (Singapore → +full Riau → +Bali/Phuket) and `?partner=dubai-rta`
(Creek pilot → full Dubai → Dubai↔Abu Dhabi corridor).

---

## 5. PER-PARTNER BUILD (your deploy lane)
`atlas build --partner=<slug>`: (1) scope data to that partner's `cities`/phases + their stories,
(2) inject `window.__PARTNER_BUILD__='<slug>'`, (3) run gates + cross-partner leak sweep,
(4) emit per-partner `SEAL.json`, (5) output `_dist/<slug>/index.html`. Recommended: a public
`navier-partners` project serving path-based `/grab`, `/dubai-rta`, …; keep the all-data `navier-atlas`
project SSO-protected. Roster grows as Tasklet authors more `partners/*.json` (add a partner = one JSON).

---

## 6. Quanta-LR — RECUT SHIPPED (resolved)
The A+B+C+D recut is live: QLR routes 94→46, **0 routes ≤70 nm** (short hops reclassified to Pioneer II),
illustrative placeholder spurs dropped, hash endpoints resolved. Still: **bind to
`from_city`/`to_city`/`platform`, never hardcoded ids**, so your views survive future recuts.

---

## Summary of current state
- `route_labels.py` + `build.py`: clean `label`/`from_label`/`to_label`/`from_city`/`to_city` on every route;
  bp-hash endpoints now resolve to real name + parent city.
- `build.py`: bakes `window.CITY_BRIEFS` / `window.PARTNERS` (no placeholder needed).
- Content: `partner-pitch/` — 19 city briefs, 6 partner proposals, architecture + 2 schemas.
- Production redeployed clean (0 leaks); QLR recut live; on `main`.
- **Your move:** §3 city panel, §4 carousel+map-drive, §5 per-partner builds. The node-ID contract in §2.5 is the
  one thing that will silently break highlighting if missed.
