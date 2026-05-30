# Partner views — config schema + `--partner` build-mode contract

_Created 2026-05-30 (v17 scaffold). Formalizes the `?partner=` mechanism shipped in v11 and the
per-partner build mode recommended in `DIVISION-OF-LABOR.md` §132–133._

A **partner view** narrows the atlas to one partner's story set and brands the chrome for them. It
is a small, data-driven config — adding or changing a partner needs **no render-code change**, only
a `PARTNER_VIEWS` entry (and, for true isolation, a Tasklet per-partner build).

Ownership (per `DIVISION-OF-LABOR.md`): **Claude owns the render hook + this contract; Tasklet owns
the build mode, the real partner roster, the externalization/land gates, and deploy.**

---

## 1 · Two delivery modes

| | **Runtime view** | **Build lock** |
|---|---|---|
| Selected by | `?partner=<slug>` on the full admin build | `window.__PARTNER_BUILD__='<slug>'` injected by a per-partner build |
| Data in the file | **All** partners' data is embedded | **Only** that partner's data |
| `?partner=` override | honoured | **disabled** (lock wins) |
| Admin/all fallback | yes (unknown/absent slug → full view) | **no** (locked; unknown slug → loud build error) |
| Privacy guarantee | unguessable-link **soft** privacy only | **true data isolation** |
| Use for | internal review, quick shares | anything sent outside Navier |

Both modes consume the **same** `PARTNER_VIEWS[slug]` config. The only difference is the isolation
guarantee, which comes from the build, not the config.

> **Privacy note (carried from the in-code comment):** in a single static file a per-partner URL is
> unguessable-link privacy, **not** access control — all embedded data is reachable. Only a
> per-partner build that *ships only that partner's data* gives real isolation.

---

## 2 · `PARTNER_VIEWS[slug]` schema

Defined in `index.html` (search `const PARTNER_VIEWS`). `slug` is the URL/build key (kebab-case).

| Field | Type | Required | Default | Notes |
|---|---|---|---|---|
| `story_slugs` | `string[]` | **yes** | — | Slugs of shipped `STORIES` this partner surfaces. Must contain ≥1 slug that resolves; unresolved slugs are dropped, and if none resolve the view silently falls back to admin/all. |
| `label` | `string` | no | first story's `partner_org_canonical_name` (else slug) | Branding text in the header tag, `<title>`, and landing panel. |
| `intro` | `string` | no | "Your focused Navier mobility view." | Copy on the partner landing panel. |
| `accent` | `string` | no | first story's `accent_class` (else `emerald`) | One of `ACCENTS`. Unknown values fall through to the story/default accent. |
| `regions` | `string[]` | no | — | **Informational only.** Map scope is derived from the stories' `scope_city_ids` / narrative `city_id`s, not from `regions`. |

`ACCENTS` (the supported accent palette, mirrored from CSS `.story-header.accent-*`):
`emerald · coral · gold · steel · violet · teal · amber · rose · sky`.

**Derived, not configured:** the set of focused cities (`scopeCities`) is computed from the selected
stories — never hand-listed in the partner config — so config and map can't drift.

### Example

```js
const PARTNER_VIEWS = {
  // minimal — single story, all branding inherited from the story
  'grab':        { story_slugs:['grab'] },

  // curated multi-story view with explicit branding
  'gulf-transit':{ label:'Gulf Waterborne Transit', accent:'amber', regions:['MENA'],
                   intro:'Waterborne transit and tourism corridors across the Gulf and Red Sea.',
                   story_slugs:['careem','uae-waterfront','qatar-transport','red-sea-global'] },
};
```

Rule (consistent with the render contract): **reference existing shipped stories only — never invent
partner identities or stories in `PARTNER_VIEWS`.**

---

## 3 · `--partner` build-mode contract (Tasklet implements)

The render side exposes exactly one hook the build must target. Everything else is the build's job.

### Render-side contract (already in `index.html`, do not change without a mutual PR)

```js
// null on the admin/all build; the partner slug on a per-partner build
const BUILD_PARTNER = (typeof window !== 'undefined' && window.__PARTNER_BUILD__) || null;
```

- When `BUILD_PARTNER` is set, `_partnerSlug()` returns it and **ignores `?partner=`** → the build is
  locked; the URL cannot escape it.
- If `BUILD_PARTNER` names a slug with no `PARTNER_VIEWS` entry, the atlas logs
  `console.error('[partner-build] … shipping unlocked')` and falls open — a **build error to catch in CI**,
  never to ship.
- The Stories dropdown and landing panel already render from `_activeStories()`, so a lock scopes them
  automatically.

### What `atlas build --partner=<slug>` must do

1. **Validate** `<slug>` exists in the partner roster and that every `story_slugs` entry resolves to a
   shipped story. Fail the build otherwise.
2. **Scope the data**: include in the bundle ONLY the features reachable from that partner's stories —
   the union of each story's `scope_city_ids` + narrative `city_id`s, plus the boarding points and
   `ROUTES` edges whose endpoints fall in that city set. Drop everything else **before** embedding.
3. **Scope the config**: emit a `PARTNER_VIEWS` containing only the `<slug>` entry (don't ship other
   partners' rosters in a partner build).
4. **Inject the lock**: place `<script>window.__PARTNER_BUILD__='<slug>';</script>` **before** the main
   `<script>` in the output `index.html`.
5. **Gate**: run the normal externalization + land gates on the scoped bundle, then the post-deploy
   substring sweep. The sweep must additionally confirm **no other partner's identifiers** appear.
6. **Name the output** deterministically, e.g. `_dist/<slug>/index.html`, so each partner deploys to
   its own URL/path.

### Acceptance checks (per partner build)

- [ ] `window.__PARTNER_BUILD__` is set and equals `<slug>`.
- [ ] Booting with **no** query param lands directly on the partner view (locked).
- [ ] Appending `?partner=<other>` does **not** change the view.
- [ ] No story outside `story_slugs` appears in the Stories dropdown.
- [ ] Substring sweep finds **zero** out-of-scope city / partner identifiers in the shipped file.
- [ ] Externalization + land gates pass on the scoped bundle.

---

## 4 · Quick reference — where things live

| Thing | Location |
|---|---|
| `PARTNER_VIEWS` config | `index.html` → `const PARTNER_VIEWS` |
| `ACCENTS` palette | `index.html` → `const ACCENTS` (+ CSS `.story-header.accent-*`) |
| Build-lock hook | `index.html` → `const BUILD_PARTNER` / `_partnerSlug()` |
| Runtime selection | `?partner=<slug>` → `initPartnerView()` → `applyPartnerView()` |
| Story definitions | `index.html` → `const STORIES` (Tasklet-owned content) |
| This contract | `docs/PARTNER-VIEWS.md` |

---

## 5 · Concrete roster + routing target  _(2026-05-30 — precise target for Tasklet)_

### Roster (every entry references a shipped `STORIES` slug — no invented identities)

Derived from the 7 shipped stories. This is exactly the `PARTNER_VIEWS` now in `index.html`; for a
locked per-partner build, ship **only** the matching row.

| Partner slug (URL key) | Stories | Org (from story) | Region |
|---|---|---|---|
| `grab` | `grab` | Grab | SEA (19 cities) |
| `careem` | `careem` | Careem (Uber subsidiary) | MENA (10) |
| `uae-waterfront` | `uae-waterfront` | UAE Transport Authorities (Dubai RTA + Abu Dhabi ITC) | Gulf (2) |
| `red-sea` | `red-sea-global` | Red Sea Global | Red Sea (3) |
| `singapore-mpa` | `singapore-mpa` | Maritime & Port Authority of Singapore | SG (3) |
| `maldives` | `maldives-hospitality` | Maldives luxury resorts | Maldives (1) |
| `qatar-transport` | `qatar-transport` | Qatar transport authorities | Qatar (1) |
| `sea-transit` _(bundle)_ | `grab` + `singapore-mpa` | Southeast Asia Transit | SEA |
| `gulf-transit` _(bundle)_ | `careem` + `uae-waterfront` + `qatar-transport` + `red-sea-global` | Gulf Waterborne Transit | MENA |

Add/remove partners by editing this table + `PARTNER_VIEWS` — no other render change.

### Routing — recommended: a separate **public** Vercel project for partner builds

The admin/all build (root `index.html`) embeds **every** partner's data and must stay **internal**
(it's behind the current project's SSO Deployment Protection). Partner builds are meant to be sent
**out**, so they must be **public** — and that's safe only because each ships **only its own data**.
Vercel Deployment Protection is per-project, so the clean split is **two projects**:

| Project | Contents | Protection | URLs |
|---|---|---|---|
| `navier-atlas` (existing) | admin/all `index.html` | **SSO on** (internal) | `navier-atlas.vercel.app` |
| `navier-partners` (new) | `_dist/<slug>/index.html` for each roster slug | **off** (public) | `navier-partners.vercel.app/<slug>` (e.g. `/grab`, `/gulf-transit`) |

- **Tasklet build output:** `_dist/<slug>/index.html` per roster slug (per §3), plus a `_dist/vercel.json`
  with `{ "cleanUrls": true }` so `/grab` serves `/grab/index.html`.
- **Deploy:** `vercel deploy --prod` **from `_dist/`** for the partner project → no repo `.vercelignore`
  juggling (the deploy root *is* `_dist/`, which contains only gated per-partner files).
- **`.vercelignore`:** the repo's allowlist (`index.html` + `vercel.json`) stays as-is for the internal
  project. If you'd rather deploy partner builds from the repo root instead of `_dist/`, add
  `!_dist/**` to `.vercelignore` — but deploying from `_dist/` is cleaner and the recommendation.
- **Pre-flight per partner:** run §3 (hash vs that partner's `SEAL.json` · exclusion grep · MapLibre
  smoke) on each `_dist/<slug>/index.html`, plus the §3.5 cross-partner sweep (no *other* partner's
  identifiers in the file).

Alternatives considered: path-based on the **same** project (rejected — can't make `/` protected but
`/grab` public on one project); custom domains per partner (fine later, but more setup). Final call on
project layout + custom domains is Jaideep's.
