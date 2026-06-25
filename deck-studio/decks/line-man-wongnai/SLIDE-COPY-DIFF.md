# LINE MAN Wongnai × Navier — slide copy-diff (mirror of Grab Thailand)

**Generation type:** `create-from-grab-thailand-mirror`
**Source live deck:** Grab Thailand × Navier — `11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo` (24 slides live)
**Target:** new LINE MAN Wongnai deck, Thailand-scoped (16 slides — see scope decision below).

> **Hard rule — numbers never change.** This is a *narrative-only* mirror. Every KPI, route, distance,
> fare, revenue, run-cost, margin, payback, CO₂, fleet count, TAM/SOM/SAM figure and unit-econ line is
> **identical** to the Grab Thailand deck. Do not recompute, re-round, or "improve" any number. Only
> partner-facing prose and the cover logo change. (LINE MAN Wongnai's footprint and economics mirror Grab
> Thailand exactly — same Thai corridors, same model.)

> **Copy gate.** Run `deck-studio/qa/partner_copy_lint.py line-man-wongnai` (blocking, same status as the
> land-crossing gate) before apply/seal. No internal taxonomy in rendered slide text. SOM/SAM/TAM/GMV may
> remain as labels **with a plain-English descriptor alongside**.

---

## Thailand-scope decision (the one substantive judgment call)

Grab Thailand's live deck is a *regional* deck — Grab is a SEA-wide super-app, so the deck carries
non-Thai example-market and unit-econ slides (**Manila, Boracay, Langkawi, Penghu/Taiwan**). LINE MAN
Wongnai is a **Thailand-only national champion** and does not operate in the Philippines, Malaysia or
Taiwan. Those **8 slides are DROPPED** in the LINE MAN Wongnai mirror:

- Example markets: Manila, Boracay, Langkawi, Penghu (Taiwan)
- Unit-econ deepdives: Manila, Boracay, Langkawi, Penghu (Taiwan)

Result: **16 Thailand-scoped slides** (1–14 + the Samui-archipelago example + the Samui premium unit-econ).
If Jaideep instead wants a literal 24-slide clone, flip `thailand_scope_decision.decision` to
`full_mirror` and re-include the 8 regional slides verbatim (they need no copy change since they never
mention the partner).

---

## Global token swaps (apply to EVERY retained slide's text)

Apply in this order (most-specific first), exactly as used to build `line-man-wongnai-derivative.json`:

| Find | Replace |
|---|---|
| `Grab × Navier` / `Grab x Navier` | `LINE MAN Wongnai × Navier` |
| `Grab Thailand × Navier` | `LINE MAN Wongnai × Navier` |
| `Grab-branded` | `LINE MAN-branded` |
| `booked in-app` | `booked in-app` *(unchanged — already partner-neutral)* |
| `in the Grab app` / `the Grab app` | `the LINE MAN app` |
| `Grab land mile` | `LINE MAN RIDE land mile` |
| `Grab Thailand owns the demand` / `…in-app demand` | `LINE MAN Wongnai owns the demand` |
| `Grab Thailand` | `LINE MAN Wongnai` |
| `Grab platform revenue` | `LINE MAN Wongnai platform revenue` |
| `Grab monetizes` | `LINE MAN Wongnai monetizes` |
| `Grab` (standalone, any remaining) | `LINE MAN Wongnai` |

After swapping, **grep the rendered text for `Grab` — zero hits allowed** (except none; there is no
legitimate residual "Grab" in a LINE MAN Wongnai deck).

---

## Per-slide bespoke rewrites

These slides carry Grab-specific framing (regional super-app / "black-car network" / Dominic Ong) that a
token swap alone does **not** fix. Use the exact replacement copy below.

### Slide 1 — Cover ("OWN THE EDGE")
- Eyebrow `OWN THE EDGE` → **unchanged**.
- Title `Water layer for two coasts, a river, and an upper-Gulf ring` → **unchanged**.
- Subtitle: `Grab already owns Thailand's in-app demand. Water is the only surface no one owns yet.`
  → **`LINE MAN Wongnai already owns Thailand's daily-life demand. Water is the one surface no one owns yet.`**
- **Cover logo:** replace the Grab logo lockup with the banked **LINE MAN Wongnai** wordmark
  (`assets/logos/partners/line-man-wongnai/logo-lmwn.png`, status `banked`). Keep the Navier wordmark.
- Footer confidentiality line → unchanged.

### Slide 2 — Exec summary ("PARTNER PROPOSAL")
- Title `Grab × Navier` → **`LINE MAN Wongnai × Navier`**
- Tagline `the black-car network, on the water` → **`Thailand's own super-app, on the water`**
- Lead `Thailand's super-app already owns the demand. Water is the only transport surface no one owns yet.`
  → **`Thailand's national-champion super-app already owns the demand. Water is the one transport surface no one owns yet.`**
- Body `We launch a Grab-branded foiling water tier …` → swap to **`LINE MAN-branded`**; keep the rest
  (Gulf islands, the Andaman, the Chao Phraya … booked in-app, premium-priced and category-defining).
  Drop "and the upper-Gulf ring" only if the upper-Gulf slide is not in the Thai-scope build (keep it if it is).
- **"Your world" quadrants:**
  - *Where you are today*: `You are Thailand's everyday super-app — mobility, deliveries, and payments in one.`
    → **`You are Thailand's home-grown super-app — 10M+ users on LINE, 500K merchants, 250K riders, with food, ride-hailing and payments in one.`**
  - *What you're up against*: `Ride-hail on land is maturing and contested — while the water stays on weather-fragile diesel ferries.`
    → **unchanged** (already partner-neutral; "ride-hail on land" fits LINE MAN RIDE).
  - *Where Navier fits*: `Water is the only transport surface in Thailand no one owns yet.` → **unchanged.**
  - *Why now*: `Foiling lifts the hull clear — faster, near-silent and far more efficient per seat-mile.` → **unchanged.**

### Slide 3 — Three C's
- `COST, COMFORT, CONVENIENCE` / `The Three C's of Scalable Water Transportation` and the three columns
  (90% lower energy cost · No noise/fumes/sea-sickness · App integration / any marina) → **all unchanged.**
  (This is a Navier product spine slide — no partner tokens.)

### Slide 4 — Thailand network map + KPIs
- Title `Two coasts, a river, and an upper-Gulf ring — one foiling network` → **unchanged.**
- Subtitle `Grab Thailand owns the demand; Navier brings the foiling fleet proven in the Maldives.`
  → **`LINE MAN Wongnai owns the demand; Navier brings the foiling fleet proven in the Maldives.`**
- All four KPI tiles (`32 routes mapped — 15 anchor + 17 Bucket-C`, `$218M addressable…`, `$21M SOM floor…`,
  `$481M SAM mid…`) → **numbers unchanged.** The SOM tile descriptor stays plain-English.

### Slides 5–7 — Thai example markets (Koh Samui & Gulf / Phuket & Andaman / Bangkok)
- Apply global token swaps only. Route lists, distances, nm, and pier names → **unchanged.**
- Map subtitles that mention the partner ("…owns the demand") → swap to LINE MAN Wongnai.

### Slides 8–10 & 20 — Thai unit-econ deepdives ("WHAT ONE BOAT EARNS · …")
- **All numbers unchanged** (revenue build, run cost, the six flush OPEX lines, margin, payback, CO₂).
- Only the partner name in any caption changes via token swap. Keep the 6-line OPEX layout flush-left.

### Slide 11 — Market sizing ("THE PRIZE")
- Title `A new multi-billion-dollar vertical across Thailand` → **unchanged.**
- Read-it-bottom-up line: `…then the whole journey Grab monetizes around every crossing.`
  → **`…then the whole journey LINE MAN Wongnai monetizes around every crossing.`**
- Ladder rows:
  - `$21M  SOM — Navier fare, Grab Thailand network, today's trips, 10% capture`
    → **`$21M  SOM — Navier fare, LINE MAN Wongnai network, today's trips, 10% capture`**
  - `$0M SAM …`, `$5.77B TAM — total journey GMV through the super-app (induced market)` → **unchanged** (numbers).
  - `Grab platform revenue on Navier-corridor journey GMV` → **`LINE MAN Wongnai platform revenue on Navier-corridor journey GMV`**, value `$259M` unchanged.
  - Keep SOM/SAM/TAM labels with their existing plain-English descriptors.

### Slide 12 — How we work together
- Title `You bring the demand. We operate the water.` → **unchanged.**
- Bullets:
  - `Grab — demand, the app, the wallet and the brand.`
    → **`LINE MAN Wongnai — demand, the LINE app, LINE Pay and the brand.`**
  - `Navier — vessels, crew, maintenance, certification and the network playbook.` → **unchanged.**
  - `Together — a premium foiling water tier across the Gulf, Andaman and Chao Phraya.` → **unchanged.**

### Slide 13 — The Ask
- Three steps (working session / vessel demo / pilot MOU — Samui triangle beachhead) → **unchanged.**

### Slide 14 — Closing
- `Explore the Grab Thailand marine network` → **`Explore the LINE MAN Wongnai marine network`**
- `Open the Navier × Grab Thailand Atlas, pick the first corridor…` → swap to **`Navier × LINE MAN Wongnai Atlas`**.
- `Own the Edge` → unchanged.

### Slide (Samui Gulf archipelago example, grab-live #15)
- Apply token swaps. `$35/seat premium runs today` and all nm/route copy → **unchanged.**

---

## Image / background policy (unchanged from gold)
- N30 composite only, market-specific backgrounds, no Atlas-generated images, minimal gold accents,
  no re-embed (stable registry URLs only). The Thai market backgrounds are **identical** to Grab Thailand —
  reuse the same registered assets; do **not** regenerate them.
- The **only** new image asset is the cover **LINE MAN Wongnai** logo (banked, provenance recorded).

## Acceptance (Grok QA receipt must show)
- New deck ID created; 16 slides (or 24 if `full_mirror`).
- `partner_copy_lint.py line-man-wongnai` green; zero `Grab` tokens in rendered text.
- Cover carries Navier + LINE MAN Wongnai logos.
- Every number byte-identical to the Grab Thailand deck (spot-check the four KPI tiles, the TAM ladder, and one unit-econ slide).
- Image provenance ledger; no re-embedded binaries; Thai backgrounds reused from grab-thailand registry.
