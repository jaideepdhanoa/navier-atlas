# Grok note — promote bolt-estonia + stand up new Bolt views (2026-06-23)

## Why this note
Jaideep reports `bolt-estonia` **is not visible on the front-end website**. It exists in
`subproposals-enriched-2026-06-20.json` with full narrative + journeys + phases, but evidently has no
derived partner-view scope / `PARTNER_VIEWS` entry on the live Atlas. Same gap will apply to the three
**net-new** Bolt markets from PR #83. This note is the deterministic stand-up + cleanup mandate.

## Mandate (deterministic only — no narrative invention)

### A. Promote `bolt-estonia` to the live front-end
- It is an **existing** sub-proposal, not new. Derive its partner-view scope by **ID-matching** the
  anchor markets to gold city nodes: `tallinn-estonia`, `helsinki-finland`, `stockholm-sweden`.
- Stand up / repair the Bolt **Estonia (Nordic-Baltic triangle)** view so it renders alongside the
  other Bolt sub-views. Confirm in the QA report **why** it was missing (no `scope_city_ids`? no
  `PARTNER_VIEWS` entry? unsealed view skeleton?) so we can regression-guard it.

### B. Stand up the three net-new Bolt views (from PR #83)
Derive `scope_city_ids` by ID-match (never hand-typed) and stand up each view skeleton:
| Sub-proposal | Anchor node(s) to bind |
|---|---|
| `bolt-thailand` | `phuket-phang-nga-thailand` |
| `bolt-nigeria` | `lagos-nigeria` |
| `bolt-south-africa` | `cape-town-south-africa` |

### C. Bind the rescoped KSA view
- `bolt-ksa-commercial` anchors are now **`jeddah-ksa`, `dammam-khobar-ksa`, `manama-bahrain`** only.
- Ensure no NEOM / AMAALA / Red Sea Global nodes are bound to the Bolt KSA view (they are scoped out;
  they may legitimately remain in other Navier-only / sovereign contexts, just **not** on this Bolt view).

### D. Apply the Lagos + Cape Town junk-POI trim
- Apply `inputs/lagos-capetown-junk-trim.json`: **12 high-confidence drops** (Lagos 7, Cape Town 5) —
  non-maritime name-keyword junk (restaurants, deli, medical, guesthouse, bank, pharmacy, bus, salon,
  engineering co.). Same approved rule class as the UAE cleanup (PR #82). Drop by **exact POI id**.
- Acceptance: **0 silent drops** — each id either removed with the logged reason or kept with a note.
  This is conservative: all plausible jetties / marinas / yacht clubs / terminals are **kept**.

### E. Run the economics cascade
- Re-run the cascade for the five affected Bolt views against the new gold; refresh aggregate/growth/
  sheet/sidecar so the deck's economics slide and TAM ladder resolve. No hand-cranked numbers.

## Acceptance gate (QA report must show)
- `bolt-estonia` view renders on the live front-end; root-cause of prior invisibility named.
- `bolt-thailand`, `bolt-nigeria`, `bolt-south-africa` views stand up with ID-matched scope.
- KSA view bound to Jeddah + Eastern Province + Bahrain only; 0 giga-project nodes on the Bolt view.
- 12 junk POIs dropped by id (0 silent drops); before→after POI counts for `lagos-nigeria` (59→52) and
  `cape-town-south-africa` (68→63).
- Economics cascade refreshed for all five; sidecar + economics_url resolve.

## Deck narrative source
`BOLT-DECK-NARRATIVE-REFRESH.md` (this package) is the Tasklet-owned narrative for the deck refresh of
these five markets. Deck build remains Slides-API-only and Grok-deterministic; this is input copy, staged
for human review before any live partner deck edit.
