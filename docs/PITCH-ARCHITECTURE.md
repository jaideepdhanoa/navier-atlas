# Navier Atlas → Partner Pitch-Document Architecture (v1)

**Author:** Tasklet · 2026-05-30
**Goal:** Turn the atlas into a *partner-facing pitch document* that scales to many partners and
many cities by authoring small content files — not by rebuilding the app.

The webpage IS the proposal. Tapping a city teaches a viewer (a Grab PM, a Dubai RTA planner)
how marine-mobility demand exists there and how Navier fits — fast. A partner URL (`/grab`) walks
a narrative arc with a phased rollout that drives both the side panel and what's lit on the map.

---

## Three content layers (separation of concerns = scalability)

### Layer 1 — City Brief  `partner-pitch/city_briefs/{city_id}.json`
Partner-NEUTRAL demand synthesis. Reused by every partner. Fills the rich side panel on city click.
Answers: *why marine mobility here, and how does Navier fit?*

Fields (see `schema/city_brief.schema.json`):
- `tagline` — one-line hook
- `demand_signals[]` — the evidence (ferry pax/yr, air O&D, congestion, hotel keys, border crossings)
- `use_cases[]` — mapped to the 5 archetypes (public_transit, super_app, tourism, luxury_charter, corporate)
- `navier_fit{ pioneer_ii, quanta_lr }` — platform-to-need mapping
- `marquee_routes[]` — route ids into ROUTES (hero corridors from/to this city)
- `key_pois[]` — boarding-point ids that matter
- `transit_planning` — the public-transport-authority planning angle
- `partner_overlays{}` — optional per-partner emphasis (e.g. grab → lead with tourism/super-app)

### Layer 2 — Partner Proposal  `partner-pitch/partners/{partner_id}.json`
Partner-SPECIFIC narrative arc + phased rollout. The pitch document. PARTNER-FACING copy (sells
Navier + "what we do together") — never internal scores/strategy/terms.

Fields (see `schema/partner_proposal.schema.json`):
- `hero{ title, subtitle, what_we_do_together }`
- `why_now`
- `phases[]` — ordered; each phase:
  - `n`, `label`
  - `boats` — fleet at this phase
  - `cities[]` — city_ids lit in this phase
  - `routes[]` — route ids lit in this phase (subset)
  - `narrative` — partner-facing copy for the side panel
  - `kpis[]` — {label, value} chips
  - `map_focus{ camera{lng,lat,zoom} }` — where the map flies
- `close{ title, body }`

The phase carousel is the spine: stepping a phase = flyTo(camera) + filter map to phase cities/routes
+ swap side-panel narrative. Phase 1 = beachhead (few boats, few routes); later phases reveal the
full network and new cities.

### Layer 3 — Render  (Claude Code)
- **City side-panel component** renders Layer 1 (sections: hook, demand, use-cases, fit, marquee routes, POIs, transit angle).
- **Partner pitch mode** (`?partner=<slug>`): side panel becomes the pitch doc; a phase carousel
  (prev/next + dots) drives camera + route/city visibility + narrative.
- **Per-partner build**: `atlas build --partner=<slug>` → scopes data to that partner's stories/phases,
  injects `window.__PARTNER_BUILD__='<slug>'`, runs gates + cross-partner leak sweep, emits
  `_dist/<slug>/index.html`. Served path-based on a public `navier-partners` project (`/grab`, `/dubai-rta`).

---

## Division of labor (drift-free)

| Lane | Owner | Deliverable |
|---|---|---|
| Schemas (L1/L2) | **Tasklet** | `schema/*.json`, frozen + versioned |
| City brief content | **Tasklet** | `city_briefs/*.json` (external_safe) |
| Partner proposal content | **Tasklet** | `partners/*.json` (external_safe, partner-facing) |
| Route display-name resolver | **Tasklet** | clean `from_label`/`to_label` on every ROUTE; no raw slugs |
| Quanta-LR city-to-city curation | **Tasklet** | curated marquee corridors; every endpoint a real city |
| Side-panel UI + phase carousel | **Claude Code** | render components binding to L1/L2 blobs |
| Per-partner build + routing | **Claude Code** | `--partner` build, `/slug` deploy |
| QA / usability | **Claude Cowork** | test the pitch flow per market |

Tasklet emits the content blobs into `data-clean/` (sealed); Claude binds the UI to them.
**Contract:** Claude never authors pitch copy; Tasklet never touches render code. Blobs are the interface.

---

## Build/ship contract additions
- New sealed blobs: `CITY_BRIEFS.json`, `PARTNERS.json` (external_safe, in SEAL.json).
- Externalization gate runs on both (partner-facing copy must pass the exclusion list).
- Route blob gains `from_label`/`to_label` (human names) — render reads these for tooltips.

---

## Why this scales
- Add a partner → 1 file (`partners/x.json`). Add a city → 1 file (`city_briefs/x.json`).
- Content authored by Tasklet (research lane); render is generic and partner-agnostic.
- Phases are data, not code — a new phasing is a content edit, instantly reflected in the pitch.
