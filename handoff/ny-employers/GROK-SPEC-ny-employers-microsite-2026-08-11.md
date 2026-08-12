# GROK SPEC — New York Employer Microsite (`/ny-employers`) · 2026-08-11

**Owner:** Tasklet (content, data, math) → Grok (deterministic front-end build) → Jaideep (merge gate)
**Surface:** New route `/ny-employers` in the navier-atlas front end. Same Vercel deploy, same map stack.
**Template:** Clone of `/bay-employers` (merged; spec at `handoff/bay-employers/`). Same page skeleton, same house style, same component patterns — NYC data, NYC math, NYC copy. Reuse the Bay page's components wherever possible; this should be a data-skin, not a new build.
**Purpose:** Employer-facing microsite for the New York employer water network — corridor map, interactive ROI calculator, two-product offer, non-binding letter-of-intent CTA. Sales surface for HR / workplace / real-estate leaders, **not** an investor or partner-ops surface.

---

## 0 · Scope guards (read first)
- **Nine of ten network stops are already sealed POIs** in `data-clean/` under `new-york-harbor-usa` — exact `bp_id` pins in `inputs/ny-employers-data.json → stops[]`. Resolve by ID-match only; never hand-type coordinates. **Do not create duplicate POIs** — the cluster contains legacy duplicates (two Pier 11s, two Paulus Hooks, two Pier 79s); the data file pins the canonical pick per stop.
- **Three short new route segments are required** (flagged `new: true` in `corridors[].segments`): E 90th ↔ E 34th · Weehawken/Lincoln Harbor ↔ Pier 79 · Paulus Hook ↔ Brookfield Place. Each connects two already-sealed POIs. Standard gates: 0 land crossings, no shore clipping, distances computed from routed geometry (never hand-entered — `distance_nm: null` in the data file means *compute it*). All other segments already exist in `ROUTES.json` (gold `route_id` pinned per segment).
- **This page is NYC-only.** It must not alter the global map, partner views, existing ROUTES.json semantics, or any existing page — including `/bay-employers`.
- **No dock / berth / landing dependency framing anywhere on the employer surface** (Jaideep ruling 2026-08-11). Do not say letters of intent unlock terminals or that shore access is a blocker. Letters of intent sequence *which line* and *how many seats*. Terminal names (Pier 11, E 34th St) are fine as stop labels — access language is not.
- **Locked numbers (2026-08-11, Jaideep):** N45 = 20 seats · N30 = 8 seats · seat price $750/seat-month standard, $900/seat-month on lines with no ferry alternative today · anchor underwrite indicative ~$125K/month · launch trigger ≈ 60–72 committed seats per line. Any conflicting source is superseded.
- **Held corridor rule:** Williamsburg appears nowhere on this page.

## 1 · Page structure (in order — mirrors `/bay-employers`)
1. **Hero** — full-bleed NYC water imagery from committed repo assets, headline: *"New York already commutes by water. We make it the best seat in the city."* Sub: *"A commuter water network for New York employers — electric hydrofoil vessels, terminal-to-terminal, above the traffic and the toll."* CTA button → §7 form.
2. **Problem band** — three stat chips: `$9/day` congestion toll into the Manhattan CBD · `$570/mo` average Manhattan parking · `$340/mo` IRS pre-tax commuter benefit your employees can apply.
3. **Precedent + credential band** — two short blocks, copy verbatim from `inputs/ny-employers-data.json → copy.precedent` and `copy.stripe_lesson`. Block 1: New York institutions already fund employee shuttles — including an employee *water* shuttle run by one of the city's largest hospital systems (no institution names on the page). Block 2: our Bay pilot credential — wrong vessel, right idea; the N45 fixes that.
4. **The two products** — cards: N30 Executive Shuttle (8 seats, on-demand, available now) · N45 Commuter Line (20 seats, scheduled service, launches on committed demand). N45 card = spec card, **no vessel render exists — never fake one**.
5. **The network map** — centerpiece. Atlas map stack, viewport locked to New York Harbor (Upper Bay + East River to Hell Gate + Hudson to ~W 40th). Ten stop markers + Lines NY-1…NY-4 and the LGA executive line as styled display corridors, water-time chips per §3. Clicking a stop lists the employer clusters it serves (`stops[].serves`).
6. **Interactive ROI calculator** — §2. Mirrors the NY ROI Calculator v1 workbook exactly.
7. **The ask / letter-of-intent CTA** — non-binding letter of intent, two flavors: Option A anchor underwrite (an institution sponsors a scheduled line — indicative from ~$125K/month) · Option B seat commitment ($750–900/seat-month band). **Option A listed first** (NYC is anchor-first). Copy in `copy.loi_cta`. Form fields: name, company, role, stop nearest office, est. interested employees, flavor, email. Submissions → `mailto:jaideep@navierboat.com` or existing Atlas form infra.
8. **Footer** — Navier wordmark, "Letters of intent are non-binding," contact.

## 2 · ROI calculator (exact math — no deviation; source = NY ROI Calculator v1 Sheet `1Rig2ouN_yzAX3XrEmTAcwXYx4cX_ZL_-wUSJP2YMzBk`)
Inputs (defaults in parentheses, all editable): committed seats **S** (60) · commute days/employee/month **D** (16) · price per seat-month **P** (750; slider bounded **750–900**, tick labels "standard $750 · no-ferry-alternative $900") · employer subsidy share **σ** (0.80) · pre-tax commuter benefit cap/month **X** (340) · current shuttle cost/seat-month **V** (0; helper text "enter your current shuttle or vanpool cost if you run one") · Manhattan parking cost/stall-month **K** (570) · share of riders displacing a stall **ρ** (0.50) · congestion toll/weekday **G** (9) · weekdays/month **W** (21).

Outputs (monthly):
- Gross program cost = `S·P`
- Employee pre-tax contribution = `S·min(X, (1−σ)·P)`
- Net employer cost = `S·P − S·min(X,(1−σ)·P)` · **Net employer cost per rider = ÷S** (headline #1; at defaults = **$600/rider**)
- Status-quo benchmark per rider = `K + G·W` (at defaults = **$759/rider** — parking + congestion toll)
- **Headline banner: net employer cost/rider vs benchmark** — at defaults **$600 vs $759**, display *"less than the parking space it replaces."* Negative delta renders green.
- Parking offset = `S·ρ·K` · Shuttle offset = `S·V`
- Net incremental employer cost after offsets = net employer cost − parking offset − shuttle offset (at defaults = **$18,900/mo ≈ $315/rider**)
- **No hours-returned / CO₂ / productivity rows in v1** — the NY workbook does not carry them; do not import the Bay page's versions.

Caveat line verbatim: *"Indicative planning tool, not a quote. Pre-tax treatment and shuttle displacement require employer verification."*

## 3 · Corridors & stops
Machine-readable in `inputs/ny-employers-data.json`. Ten stops, five display lines:

| Line | Public label | Stops | Geometry status |
|---|---|---|---|
| NY-1 | **Upper East Side Medical Line** | E 90th St ↔ E 34th St | 1 new segment |
| NY-2 | **Hudson Gold Coast Line** | Weehawken/Lincoln Harbor · Hoboken ↔ Midtown W 39th | Hoboken↔Pier 79 exists (`ics-25a683a51c`); Lincoln Harbor↔Pier 79 new |
| NY-3 | **Lower Hudson Crossing** | Paulus Hook ↔ Brookfield Place · Pier 11 | Pier 11↔Paulus Hook exists (`ics-bdacfbafa1`); Paulus Hook↔Brookfield new |
| NY-4 | **Brooklyn Tech Line** | Brooklyn Navy Yard · DUMBO ↔ Pier 11 (optional extension E 34th) | All segments exist (`rn-7d501d48d2f3`, `rn-c5916368a650`, ext `rn-b2490e3f6350`) |
| EXEC | **LaGuardia Executive Shuttle** | E 34th St ↔ LGA Marine Air Terminal | Exists (`rn-0e2b916d3b8d`, 5.9 nm) |

Time chips: **"X.X nm · ~Y min on the water"** where Y = distance ÷ 20 kn cruise, rounded up to the nearest 5 min, computed from routed geometry — labeled *indicative*. **No land-side minute claims** (no sourced drive/subway times in the package — do not invent them). **No schedules — do not invent timetables.**

## 4 · Copy rules (hard gates)
- Plain English throughout; must pass `scripts/audit_partner_copy.py`. Banned: "node" (say *stop* or *terminal*), "LOI" in visible copy (say *letter of intent*), knots/speed figures, "corridor" in customer-facing headers (say *line* or *route*), all internal process vocabulary ("Motion A/B", "Tier-1", "anchor-tenant" — say *sponsor a line* or *underwrite a line*).
- **Dock/berth/landing-access language banned entirely** (§0).
- Price appears **only** inside the calculator and the letter-of-intent section ($750–900 band; ~$125K/mo indicative on Option A). Emotional anchor: *"less than the parking space it replaces."*
- Non-binding nature stated wherever the letter of intent is mentioned.
- **No employer or institution names anywhere on the public page** — precedent block stays anonymized ("one of the city's largest hospital systems"). The Stripe pilot may be named (public record, our credential).
- No NYC Ferry / NY Waterway comparisons by name — say "conventional ferries" if contrast is needed.

## 5 · Visual rules
- House style: Atlas dark field, gold accents, Playfair Display / Exo 2 / Poppins — identical to `/bay-employers`.
- Imagery only from committed repo assets (shared Navier assets; NYC plates if present in `deck-studio/assets/`). No AI-generated new plates in this pass. If no NYC hero plate exists in repo assets, use the dark-field pattern treatment — never a wrong-city photo.
- Text never sits on an unscrimmed photo.

## 6 · Acceptance gate (QA report must show)
1. `/ny-employers` renders on the existing deploy; no other route's snapshot changes (before/after diff on `/`, `/bay-employers`, one partner page).
2. Map: ten stops resolve by ID-match to the pinned sealed POIs (list chosen `bp_id` per stop); zero duplicate POIs created; the three new segments route water-clean (0 land crossings — East River segments respect Roosevelt Island; Hudson segments respect pier lines); computed `distance_nm` reported per new segment.
3. Calculator reproduces the worked example exactly: defaults → **$600/rider net employer vs $759 benchmark; $18,900/mo net incremental after offsets ($315/rider)**.
4. Copy audit passes (`audit_partner_copy.py` + banned list §4) over all rendered strings; zero hits on dock/berth/landing-access framing.
5. Letter-of-intent form delivers (mail handoff or form infra) — show a test submission with Option A selected.
6. Mobile rendering verified (opened from LinkedIn messages on phones).
7. Cross-page parity: `/bay-employers` unchanged pixel-for-pixel; shared components refactored only if both pages' snapshots stay identical.

## 7 · References
- Data package: `inputs/ny-employers-data.json` (stops, lines, calculator model, copy blocks)
- Bay template: `handoff/bay-employers/` (merged spec + data) and the live `/bay-employers` route
- NY pitch deck (visual parity target): Slides `18Za-zVWdbAFnpsstmBrJQu2WVZs35cCK74gNBECnkWY`
- Drive program folder: NY Employer Network `1AQE1bf3VvDjBHA-I7W_wlKTXykNymDpB` (parent: Employer Water Networks `1SHFUrLnnR1sKvzcyenCGY0D0pZM_X2LT`)
- NY ROI Calculator v1: `1Rig2ouN_yzAX3XrEmTAcwXYx4cX_ZL_-wUSJP2YMzBk` · NY Service P&L v1: `10uHWjwdiYTjmGxEXrPfsktHj3-r9jbk1awEPGG63rx8`
- Locked economics: $750/$900 seat bands · ~$125K/mo anchor underwrite · N45 20 seats · N30 8 seats · trigger 60–72 seats/line (2026-08-11, Jaideep)
