# Claude Cowork — Front-End QA Plan (v5 · expanded build)

**Updated:** 2026-05-31 · self-contained canonical plan. Supersedes the earlier
`_ingest/BRIEF-FOR-COWORK-pitch-flow.md` and `COWORK-TEST-BRIEF.md`.
**Role:** demanding, first-time **partner-facing** viewer. Observe-and-report; don't edit.

## Two surfaces to test (this is new)
1. **Aggregate (internal)** — `https://navier-atlas.vercel.app/` — every partner + every city; the region nav; the place to verify breadth and isolation.
2. **Partner pages (what a partner is actually sent)** — `https://navier-atlas.vercel.app/<slug>` — each contains **only that partner's** data, locked. **The §E quality bar is judged here.**
   Slugs (10): `grab` `careem` `uber` `dubai-rta` `abu-dhabi-itc` `qatar` `saudi-pif` `red-sea-global` `singapore-mpa` `hawaii`.

**Cite every finding by deep-link** + lane tag:
- camera: `…/#camera=<lng>,<lat>,<zoom>` · partner phase: `…/<slug>#/partner/<slug>/phase/<n>`
- **`[RENDER]`** = Claude Code (labels, panels/carousel, camera/focus, region nav, isolation, deep-links, console errors). **`[DATA]`** = Tasklet (route geometry/existence, BP placement/names, narrative/KPI/journey content, missing/var-region briefs, phase city-id mismatches).

## What's new since the last round (focus here)
- **Per-partner pages at `/<slug>`** — isolation is now testable (was deferred last round).
- **10 partners** (added `uber`, `qatar`, `saudi-pif`, `hawaii`; `careem` is UAE-only now); **phase counts vary (2–4)** — don't assume 3.
- **78 city briefs** incl. **US expansion** (Hawaii, Florida, SF Bay) + Caribbean.
- **Region nav: data-driven chips next to Global** (auto-built from the data — was just MENA/SEA).
- **Richer partner sections** (schema v2): Their world · Why now · Journeys we unlock · Into your stack · Phased rollout · Why Navier · Proof points · Questions you might have · The ask.
- **Boarding-point geocoding pass** — several old inland-BP offenders should now be fixed (re-check in §E.2).

---

## Gate 0 — confirm you're on the v5 build (60s)
1. `/` → click **Singapore** → a **rich pitch panel** (demand signals / use-cases), and the top nav shows **region chips next to Global** (East Asia / MENA / North America / … — more than just MENA/SEA). Routes draw: **mint solid (Pioneer II)** + **amber dashed (Quanta-LR)**.
2. `/grab` (the partner page) → loads a **Grab pitch carousel** with **only Grab** in view; the URL has no `?partner=`.
- If `/` shows a plain name panel or chips, hard-refresh (Cmd/Ctrl-Shift-R). If `/grab` 404s or shows other partners, **stop and report** "v5 not served / isolation broken".

## A. Region nav + Stories browser (new — quick)
1. **Region chips next to Global** (data-driven). **PASS** = a chip per live region (expect ~7: MENA, Southeast Asia, East Asia, South Asia, Turkey, North America, Latin America & Caribbean). Click one → map **fits to that region** and the chip goes **active** (Global de-activates). The least-populated regions collapse under a **More ▾** chip — open it and confirm those jump too.
2. Spot-check a **new** region (e.g. **North America** → US coasts/Hawaii frame; **Turkey** → Aegean/Marmara). `[RENDER]` if a region chip is missing or jumps to the wrong place; `[DATA]` if a region label looks wrong/duplicated.
3. **Stories ▾** opens a **filterable card dialog** (not a long dropdown). **PASS** = a grid of all stories (~12), the filter box narrows by title, clicking a card opens that story, and ✕ / Esc / click-outside close it.

## B. Route-label correctness (on `/`)
3. Hover/click ~15 routes across regions. **PASS** = clean `Origin → Destination`; no underscores, raw slugs, or `Bp 643f1f62a7`. A bare **"boarding point"** endpoint = acceptable `[DATA]` "name this BP", not a render bug.
4. Every **amber/dashed (Quanta-LR)** route reads City → City and is **long-haul** (flag any that look <~70 nm — those should be solid Pioneer II). Expect **0** QLR ≤70 nm.
5. **Exclusion:** confirm **no** NEOM↔Eilat / Sharm↔Eilat routes anywhere (must be 0).

## C. Rich city panels (78 briefs; sample ~15 on `/`)
6. Click a spread incl. **new markets**: **US** Honolulu (Oʻahu), Maui, SF Bay, Palm Beach; **MENA** Dubai, Abu Dhabi, Doha, Jeddah; **SEA** Singapore, Bali, Phuket, Bangkok; **Red Sea** NEOM/Sindalah, Red Sea Global. **PASS** = hook/tagline, demand signals, use-cases (archetype-badged), Navier fit (Pioneer II + Quanta-LR), signature routes + live routes, transport-authority angle.
7. A city with **no clickable node** (some future-market briefs exist without a graph node yet — Turkey/Korea/Japan/etc.) is **known state**, not a bug. A clicked city that shows the **lightweight** panel (no brief) → `[DATA]` "missing brief".

## D. Partner page = GUIDED CHAPTERED TOUR (rebuilt — test the flow on each `/<slug>`)
The partner page is no longer a long scroll. It opens with a **large dialogue**, then steps through chapters.
8. **Opening dialogue** auto-opens on load: hero + **"Your world"** (second-person) + "Why now", large and readable. **PASS** = "Take the tour →" closes it to the map; **"About ▾"** (top, where "Stories" sits on the aggregate) **reopens** it; Esc / "Skip to the map" / click-outside also close.
9. **End-state first:** the first chapter is **"The network"** — the **whole** partner network lit (all markets), with a markets/vessels/phases stat strip. **PASS** = noticeably more cities/routes lit here than in any single phase (this is the "where this goes" wow).
10. **Chapter spine:** a sticky **‹ Chapter X of N ›** stepper + dots drives both panel and map: end-state → **phase 1..N** (each flies the camera, lights that phase, dims the rest, swaps narrative/KPIs/featured-routes) → **Why Navier · your questions** (differentiation + proof + FAQ) → **The ask** (+ close). Deep-link `…/<slug>#/partner/<slug>/phase/2` (and `…/chapter/ask`) + reload restores that chapter and **skips** the opening dialogue.
11. **Isolation probe (still critical):** `/grab` loads **only Grab's** data (~360 routes, not ~1,567); `/grab?partner=uber` must **stay Grab**. Any other partner's data/name = **`[RENDER]` leak — flag loudly.**
12. **City drill-down + return:** click a lit city → its brief opens with a **"← Back to the proposal"** button at the top → returns to the current chapter. (Clicking empty water also returns.)
13. **Panel ergonomics:** drag the panel's **left edge** to resize (persists on reload); the collapse chevron shows **›** when open (hides it) and **‹** when hidden (reveals it).
14. On `/` (aggregate) `?partner=<slug>`: the opening dialogue carries an **"Open <partner>'s dedicated page →"** link to `/<slug>`; it's **absent** on the locked page.
15. **Known gap:** journey cards are **not yet clickable** (pending route ids from data) — not a bug this round.

## E. ⭐ Partner-page QUALITY — the core (judge on each `/<slug>`)
For **each partner × phase**, decide: *could the partner present this page as-is?* Read the panel, then inspect the lit map (zoom in, hover/click lit routes, zoom to endpoint POIs). Score 1–5:
1. **Route accuracy (geography)** — each lit route is City→City, on water, crosses no land/islands, ends at a real coastal place (marina/terminal/jetty), not mid-ocean; platform·distance·ETA plausible (Pioneer II ≤70 nm; Quanta-LR longer/hybrid). *Geometry → `[DATA]`.*
2. **POI / boarding-point placement** — each lit endpoint is on the coast/water, not inland. **Re-check the previously-flagged offenders** (Dubai Creek marinas, Abu Dhabi/Ghantoot, Phuket) — a geocoding pass should have fixed several; confirm fixed or still off. *Placement → `[DATA]`.*
3. **Market fit** — routes suit the archetype (super-app = dense commuter/cross-border; transit authority = inner-harbour + intercity; tourism/hospitality = resort hops; Hawaii = inter-island incl. the ʻAlenuihāhā channel). Phasing reads as a credible rollout (beachhead → scale → region).
4. **Narrative ↔ map coherence** — panel claims match the map; **journeys** and **featured-routes** text correspond to routes you can actually find lit; KPI/boat counts ≈ what's drawn.
5. **Brief cross-check** — click each phase city → its brief's signature routes/use-cases match what's drawn (same corridors, same platform).

**Per-partner deliverable:** one line — "present as-is? yes/no" + top 3 fixes, each `[RENDER]`/`[DATA]`. **Cover all 10.**

## F. Regression guard
12. Flagship labels (Doha/Dubai/Abu Dhabi/Muscat/Singapore) don't stack at world view; **Singapore always labelled**.
13. Route lines render everywhere sampled; **no console layer-validation errors**.
14. Colour = **platform** (Pioneer II mint / Quanta-LR amber), never trip-purpose; legend ↔ map parity.
15. Cold-load OK; panels **frame** the map (don't blanket it); stats not occluded. Same on a `/<slug>` page.

## Known state (don't file as bugs)
- ~18 future-market briefs exist **without a clickable node yet** (Turkey/Korea/Japan/Vietnam/Taiwan/Cambodia secondary cities, Eastern Province) — content ahead of the graph.
- Region labels are alias-merged for the dropdown (e.g. `SEA`==`Southeast Asia`); source-label cleanup is a tracked `[DATA]` nit.
- `trip_purpose` is sparse — irrelevant to colour (colour = platform).
- "boarding point" endpoint fallback = a `[DATA]` naming gap, not a render bug.

## Report format
Per check: **PASS / FAIL** + 1-line note + screenshot + deep-link + lane tag. End with a **partner-ready verdict for all 10** (Grab · Careem · Uber · Dubai RTA · Abu Dhabi ITC · Qatar · Saudi-PIF · Red Sea Global · Singapore MPA · Hawaii), and a short list of the **top cross-cutting `[RENDER]`** vs **`[DATA]`** themes.
