# GROK SPEC — Bay Area Employer Microsite (`/bay-employers`) · 2026-08-10

**Owner:** Tasklet (content, data, math) → Grok (deterministic front-end build) → Jaideep (merge gate)
**Surface:** New route `/bay-employers` in the navier-atlas front end. Same Vercel deploy, same map stack.
**Purpose:** Employer-facing microsite for the Bay Area employer water network — corridor map, interactive ROI calculator, two-product offer, non-binding letter-of-intent CTA. This is a sales surface for HR/workplace/real-estate leaders, **not** an investor or partner-ops surface.

---

## 0 · Scope guards (read first)
- **No new geography is created.** All six network nodes are already sealed POIs in `data-clean/` (candidate IDs in `inputs/bay-employers-data.json` → `nodes[].candidate_bp_ids`; resolve canonical picks by ID-match, never by hand-typed coordinates).
- Corridor **display lines** (A/B/C) connect existing sealed POIs. If line geometry must be drawn, it passes the standard water-crossing gates: 0 land crossings, no shore clipping.
- **This page is Bay-only.** It must not alter the global map, partner views, ROUTES.json semantics, or any existing page.
- **The stale corridor PDF is superseded.** Any prior source stating a 30-seat N45 or a 1,000–1,500-seat launch trigger is wrong. Locked numbers: **N45 = 20 seats · corridor launch trigger ≈ 60–80 committed seats · seat price band $800–1,200/seat-month.**

## 1 · Page structure (in order)
1. **Hero** — full-bleed Bay imagery (reuse WETA asset pack, `deck-studio/assets/weta/`), headline: *"The Bay is the fastest lane your team isn't using."* Sub: *"A commuter water network for Bay Area employers — electric hydrofoil vessels, terminal-to-terminal, faster than the bridge at rush hour."* CTA button → §7 form.
2. **Problem band** — three stat chips: `75–90 min` typical Marin→Peninsula rush-hour drive · `2×` water is ~twice conventional ferry speed (no knots anywhere) · `4 ft` foiling above chop — smooth enough to work.
3. **Proof + honest lesson** — the Stripe pilot block. Copy verbatim from `inputs/bay-employers-data.json → copy.stripe_lesson`. This is the credibility section; do not soften or pad it.
4. **The two products** — cards: N30 Executive Shuttle (8 seats, on-demand, available now) · N45 Commuter Line (20 seats, scheduled corridor service, launches on committed demand). N45 card = spec card, **no vessel render exists — never fake one**.
5. **The network map** — the centerpiece. Atlas map stack, locked to SF Bay viewport. Six node markers + Lines A/B/C as styled display corridors with water-vs-drive time chips (data in `corridors[]`). Clicking a node lists the employer clusters it serves (`nodes[].serves`).
6. **Interactive ROI calculator** — §2. Mirrors the v2 workbook exactly.
7. **The ask / LOI CTA** — non-binding letter of intent, two flavors: Option A seat-commitment, Option B anchor-tenant line underwrite. Copy in `copy.loi_cta`. Form fields: name, company, role, node nearest office, est. interested employees, flavor, email. Submissions → `mailto:jaideep@navierboat.com` handoff or existing Atlas form infra if present.
8. **Footer** — Navier wordmark, "Letters of intent are non-binding," contact.

## 2 · ROI calculator (exact math — no deviation)
Inputs (defaults in parentheses, all editable): committed seats **S** (60) · commute days/employee/month **D** (16) · price per seat-month **P** (1000; slider bounded 800–1200) · employer subsidy share **σ** (0.80) · pre-tax commuter benefit/month **X** (325) · current shuttle cost/seat-month **V** (550) · parking stall cost/month **K** (350) · share of riders displacing a stall **ρ** (0.50) · one-way car minutes **Tc** (75) · one-way water minutes **Tw** (30) · one-way car miles **M** (20) · kg CO₂/car-mile **E** (0.35) · loaded employee-hour cost **H** (90).

Outputs (monthly):
- Gross program cost = `S·P`
- Employee pre-tax contribution = `S·min(X, (1−σ)·P)`
- Net employer cost = `S·P − S·min(X,(1−σ)·P)`
- Shuttle offset = `S·V` · Parking offset = `S·ρ·K`
- **Net incremental employer cost = net employer cost − shuttle offset − parking offset** (headline output; at defaults = **$4,500/mo ≈ $75/rider** — display "roughly a parking space — often less")
- Hours returned = `S·D·2·(Tc−Tw)/60` · Productivity value = hours × H (label "for framing only, not savings")
- CO₂ avoided (t/mo) = `S·D·2·M·E/1000`
- Net cost per employee-hour returned = net incremental ÷ hours returned (guard div-by-0)

Show the caveat line: *"Indicative planning tool, not a quote."*

## 3 · Corridors & nodes
Machine-readable in `inputs/bay-employers-data.json`. Six nodes: Larkspur · SF Ferry Building · Mission Bay (16th St/China Basin) · Oyster Point · Redwood City · Alameda/Jack London. Three lines, times verbatim from the verified corridor source (A: Larkspur–Ferry Bldg–Oyster Point · B: Mission Bay–Oyster Point–Redwood City · C: Alameda/Oakland–Mission Bay/Oyster Point). **No schedules exist — do not invent timetables.** Time chips show "~25 min on the water · 60–90 min driving" style pairs only.

## 4 · Copy rules (hard gates)
- Plain English throughout; must pass `scripts/audit_partner_copy.py`. Banned: "node" (say *stop* or *terminal*), "LOI" in visible copy (say *letter of intent*), knots/speed figures, "corridor" in customer-facing headers (say *line* or *route*), all internal process vocabulary.
- Price appears **only** inside the calculator and the pricing section as the $800–1,200 band; the emotional anchor is "≈ a parking space."
- Non-binding nature stated wherever the letter of intent is mentioned.
- No employer names anywhere on the public page (no Stripe-era client list, no target list). The Stripe pilot itself may be named — it is public record (TechCrunch/Bloomberg 2024).

## 5 · Visual rules
- House style: Atlas dark field, gold accents consistent with existing Atlas pages; Playfair Display / Exo 2 / Poppins.
- Imagery only from committed repo assets (`deck-studio/assets/weta/`, shared Navier assets). No AI-generated new plates in this pass.
- Text never sits on an unscrimmed photo.

## 6 · Acceptance gate (QA report must show)
1. `/bay-employers` renders on the existing deploy; no other route's snapshot changes (before/after screenshot diff on `/`, one partner page, one city page).
2. Map: six stops resolve by ID-match to sealed POIs (list the chosen `bp_id` per stop); Lines A/B/C render with 0 land crossings; viewport locked to the Bay.
3. Calculator reproduces the worked example: defaults → **$4,500/mo net incremental, $75/rider** — exact.
4. Copy audit passes (`audit_partner_copy.py` + banned list §4) over all rendered strings.
5. Letter-of-intent form delivers (mail handoff or form infra) — show a test submission.
6. Mobile rendering verified (this page will be opened from LinkedIn messages on phones).
7. No references to 30-seat N45, 1,000+ seat triggers, knots, or internal vocabulary anywhere.

## 7 · References
- Data package: `inputs/bay-employers-data.json` (nodes, lines, calculator model, copy blocks)
- Pitch deck (visual parity target): Slides `1ZNH2_YFGw1XXLlC_0a7A2qxv-iefwtBh7PNJ9FFVnP8`
- Drive program folder: `18U5DJ7gDRqOAw6x5Q0lhHAT6dSh7l_ys`
- Locked economics: seat band $800–1,200 · N45 20 seats · N30 8 seats · trigger 60–80 seats/line (2026-08-10, Jaideep)
