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
| `value_prop_bg` | 2 | deck · **per market** | exec-summary booking/berth scene — **woman on a phone booking a ride**, N30 at the dock; **one distinct composite per anchor market** (distinct from the Three C's plate) | composite |
| `market_overview_kpis` | 3 | deck | market-overview KPI block (figures, not an image) | manifest/economics sidecar |
| `tam_bg` | 10 | deck | TAM background | composite |
| `partner_roles_bg` | 11 | deck | partner-roles background | composite |
| `econ_market_bg` | 7–9, 19–23 | **market** | **reusable across any deck featuring that city** | N30 composite, keyed by Atlas city ID |

### `partner_logo` (cover) — required
Every named-partner deck **must** carry the partner's logo on the cover (slide 1). It is part of the
deck-builder request, not optional polish. Source it from the partner's brand assets and bank it under
`logos/partners/{partner}/` with provenance; register it in `ASSET-REGISTRY.json`. If it cannot be sourced
cleanly, leave the role `needs_sourcing` (blocked) — never ship a named-partner cover without it, never guess a logo.

Territory / Navier-only decks with no named partner (for example Caribbean, French Polynesia, Hong Kong) are the
exception: set `partner_logo: null`, use a Navier-only cover, and do **not** invent a government/tourism badge.

### `market_overview_kpis` (slide 3) — data role, not an image
Slide 3 carries the market-overview KPIs (e.g., market size, fleet/route counts, demand/fare anchors). It is
a **data/figures role** resolved from the deck manifest + economics sidecar, not a composite image. The
deck-builder/playbook must populate it from the transparent sheet/master tracker, never leave it stale.

### Slide 2 `value_prop_bg` — SEALED + market-specific (definitive, 2026-06-22, rev-3)

**Status: SEALED for Grab (SE Asia).** The distinct slide-2 image is generated, locked, and applied
live (`replaceImage` on `narr2_bg_img`). The interim borrowed Three C's plate is **retired**.

- **Sealed SE-Asia gold reference:** `backgrounds/decks/grab/grab-value_prop_bg-southeast_asia.png`
  (1536×864) — Drive `id=1OiOsLLNSdzR9P0vwZ7S_sQr42RWd5EFe`. Scene: modern city riverfront skyline,
  a professional woman lower-left on her phone walking the dock to board, canonical N30 bow-to-dock
  with the gangway down, navy lower-third scrim. Reference-guided on the **N30 neutral** only (the
  Three C's plate was deliberately **not** used as a composition reference — that incidental reuse
  was the original echo). Provenance: `…-southeast_asia.provenance.json`.
- **`value_prop_bg` is MARKET-SPECIFIC.** Scope is `deck`, but the scene must be generated for the
  deck's **anchor market** — there is **one variant per market**, never a shared cross-market plate.
  The SE-Asia urban-riverfront read is the Grab variant; a different anchor market gets its own
  composite to the same brief. Build per `backgrounds/decks/{deck}/SLIDE2-IMAGE-BRIEF.md`
  (the deterministic per-market process + literal prompt template live there).
- Each market variant must still pass the **distinctness check** vs that deck's Three C's plate.

### Slide 2 vs the "Three C's" slide — distinct images (history, 2026-06-22, rev-2)
After the exec-summary insert, the live deck order is: 1 cover, **2 exec-summary/thesis**
(`value_prop_bg`), **3 "Three C's" (Cost/Comfort/Convenience)**. There is **no rule — and no
Grok instruction — to share a background across slides 2 and 3.** They came out identical only
because `value_prop_bg` was banked from the *same* N30 composite the Three C's slide already used
(Drive `…id=1ZyY6gGGWJ9ab4JFQdD2mUsputE70Rytz`). That is incidental reuse, not intent.

**Definitive policy (rev-2 — reviewer call 2026-06-22): the Three C's slide background is correct
as-is; slide 2 gets its OWN new image rather than borrowing it.**
- **Slide 3 "Three C's" background — canonical, keep as-is.** The existing N30 composite
  (Drive `…id=1ZyY6gGGWJ9ab4JFQdD2mUsputE70Rytz`) is the accepted asset for this slide. It is **not**
  re-sourced and **not** a placeholder. No `three_cs_bg` sourcing work is open. *(The slide-3 figures
  role `market_overview_kpis` is unaffected — see that row.)*
- **Slide 2 `value_prop_bg` — needs its OWN distinct composite (`needs_generation`, blocked).**
  Slide 2 is the exec-summary "today/proof" hero. Its image must be a **distinct** N30 composite —
  not the Three C's plate — built to the literal brief in
  **`backgrounds/decks/grab/SLIDE2-IMAGE-BRIEF.md`**: a **woman on a phone at the berth booking a
  ride**, with the canonical N30 at the dock, market-specific plate, navy lower-third scrim for copy
  legibility. Until that asset is sourced/composited (per `IMAGE-RULES.md`: N30 neutral reference, no
  Atlas-generated images, provenance required, stable URL), slide 2 may keep the borrowed Three C's
  plate as a **documented interim only** — never the final answer, never guessed.

> Note: the table row `market_overview_kpis (slide 3)` is the *figures/KPI* role for the
> deck-builder's canonical slide 3; the live Grab deck's physical slide 3 is the Three C's slide,
> whose background is the canonical asset above. The open image work is **slide 2 only**.

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
