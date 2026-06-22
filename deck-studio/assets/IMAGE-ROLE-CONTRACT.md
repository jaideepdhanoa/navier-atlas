# Deck Image-Role Contract

Every Navier partner deck (`partner_proposal` type) carries a fixed set of **image roles**.
This contract is the single source of truth for *which* images a deck needs, *where* they sit,
and *how* they are sourced/reused. The asset pack (`ASSET-REGISTRY.json` + `backgrounds/` + `logos/`)
must satisfy every role before a deck is render-complete.

All final images must obey `docs/IMAGE-RULES.md`: **N30/N35 composites only, no Atlas-generated images,
provenance required.** Logos are the only non-composite assets.

## Roles (per deck)

| role | slide | scope | reuse | source |
|---|---|---|---|---|
| `cover_hero` | 1 | deck/market | per anchor-market (place-specific vessel-on-water) | N30 composite |
| `navier_logo` | 1 | shared | every deck (identical) | brand asset |
| `partner_logo` | 1 | partner | every deck for that partner | partner brand asset **(REQUIRED on cover)** |
| `value_prop_bg` | 2 | deck | cost / comfort / convenience background | composite |
| `market_overview_kpis` | 3 | deck | market-overview KPI block (figures, not an image) | manifest/economics sidecar |
| `tam_bg` | 10 | deck | TAM background | composite |
| `partner_roles_bg` | 11 | deck | partner-roles background | composite |
| `atlas_route_screenshot` | 4–6, 14–18 | deck | market side-panel (example + backup) | **human capture** from Vercel Navier Atlas (not generated) |
| `econ_market_bg` | 7–9, 19–23 | **market** | **reusable across any deck featuring that city** | Tier-A full-bleed landmark skyline (`navierBg_*` slots only) |

### `partner_logo` (cover) — required
Every named-partner deck **must** carry the partner's logo on the cover (slide 1). It is part of the
deck-builder request, not optional polish. Source it from the partner's brand assets and bank it under
`logos/partners/{partner}/` with provenance; register it in `ASSET-REGISTRY.json`. If it cannot be sourced
cleanly, leave the role `needs_sourcing` (blocked) — never ship a named-partner cover without it, never guess a logo.

Territory / Navier-only decks with no named partner (for example Caribbean, French Polynesia, Hong Kong) are the
exception: set `partner_logo: null`, use a Navier-only cover, and do **not** invent a government/tourism badge.

### Slide layout families (Grab gold template — do not cross-wire)

Partner decks cloned from the Grab gold template have **two image slot types**:

| Family | Slides | Layout | Target object pattern | Allowed roles |
|---|---|---|---|---|
| Market side-panel | 4–6, 14–18 | `p22` side image | `g3eec5122801_0_*` (not `navierBg_*`) | `atlas_route_screenshot` only |
| Unit economics full-bleed | 7–9, 19–23 | full-bleed behind P&L | `navierBg_s23` … `navierBg_s39` | `econ_market_bg` only |

**Never** apply `econ_market_bg` to slides 4–6 or 14–18. All market side-panel slides (4–6 and 14–18)
are reserved for Atlas route screenshots (human capture). Authoritative per-deck wiring:
`decks/{deck}/slide-image-bindings.json`.

### `atlas_route_screenshot` (slides 4–6, 14–18) — human capture, not generated
Market side-panel slides show the Navier Atlas route/map UI for beachhead and backup corridors. Capture
from the live Vercel Atlas, bank under `assets/screenshots/atlas/{deck}/`, register with provenance,
apply to the side-panel image slot. Do **not** substitute Tier-A generated plates here.

### Deck hyperlinks (white text) — `docs/DECK-LINK-BINDINGS.md`

| Slide(s) | Label | Role | Target |
|----------|-------|------|--------|
| 3 | Interactive link | `atlas_partner_hub` | `/{partner_id}` on Navier Atlas |
| 4–6, 14–18 | Interactive link | `atlas_market` | Market sub-proposal or city page |
| 7–9, 19–23 | Model deepdive | `economics_sheet` | Partner unit-economics Google Sheet |
| 10 | Detailed market sizing | `economics_sheet` | Same economics sheet |

Authoritative wiring: `decks/{deck}/slide-link-bindings.json` (+ auto-merge from
`economics-binding.json`). Apply via `builders/deck_link_bindings.py`. Style: **white + underlined**.

### `econ_market_bg` (slides 7–9, 19–23) — full-bleed landmark skyline
Unit-economics slides: **full-width edge-to-edge** photorealistic market-specific landmark skyline,
coastline, and harbour (identifiable at thumbnail size). No artificial gradient panels or blank chart-safe
zones baked into the image — charts overlay on the slide template. Vessel small in the lower-center,
foils deployed, hull elevated (hydrofoiling — not sitting low like a ferry). Prompt tier:
`econ_unit_landmark` in `N30-TIER-A-PROMPTS.md`.

### `market_overview_kpis` (slide 3) — data role, not an image
Slide 3 carries the market-overview KPIs (e.g., market size, fleet/route counts, demand/fare anchors). It is
a **data/figures role** resolved from the deck manifest + economics sidecar, not a composite image. The
deck-builder/playbook must populate it from the transparent sheet/master tracker, never leave it stale.

### Scope semantics
- **market** — keyed by sealed Atlas `city_id`; the *same* file is reused by any deck that features that city.
  Stored under `backgrounds/markets/{market_slug}/`. Bind to a deck slide only via exact `city_id` match
  (null `atlas_city_id` ⇒ filed by descriptive slug, **not** yet bindable — null beats confidently-wrong).
- **deck** — specific to one deck's narrative slide (value-prop / TAM / partner-roles). Stored under
  `backgrounds/decks/{deck}/`.
- **shared** — one canonical Navier brand asset reused everywhere (`logos/navier/`).
- **partner** — one asset per partner brand (`logos/partners/{partner}/`).

## Directory layout
```
deck-studio/assets/
  ASSET-REGISTRY.json            # master index (image_key -> provenance + binding)
  IMAGE-ROLE-CONTRACT.md         # this file
  backgrounds/
    markets/{market_slug}/...    # reusable, city-keyed econ backgrounds
    decks/{deck}/...             # deck-specific value-prop / tam / partner-roles
  logos/
    navier/                      # shared Navier wordmark/mark
    partners/{partner}/          # per-partner logos
  n30/                           # N30 vessel master (README only until n30.png lands)
```

## Naming convention (observed, canonical)
- market background: `slide-bg-{market}-v{N}-composited.png`
- deck background:   `{deck}-slide{N}-bg.png`
- logo:              `{brand}-logo.png` / `{brand}-wordmark.png`

## Edit-plan / Grok contract
A deck's `image-manifest.json` lists every role with a resolved `target_object_id` (from full inventory)
and an `asset_ref` pointing at an `ASSET-REGISTRY.json` `image_key`. The `deck.editplan.json` consumes
those refs to emit `replaceImage` / `createImage` ops. Grok binds image object IDs **only** from
Tasklet-provided exact evidence; unresolved roles stay `null` (status `needs_generation`/`needs_sourcing`),
never guessed.


## No-reembed / linked URL rule

A checked-in file is not enough by itself for a live Slides update. Every final image must resolve to a stable
registry URL (`source_url` / approved Drive URL) before it is inserted or replaced in Google Slides. Temporary
Google Slides `contentUrl` / `lh*-googleusercontent` links are inspection evidence only and must never become
canonical assets. If an image is embedded-only, regenerate or capture it into `assets/`, publish a stable URL,
update `ASSET-REGISTRY.json`, then apply.
