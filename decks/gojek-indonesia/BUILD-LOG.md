# Gojek × Navier — Indonesia deck · BUILD-LOG

**Deck (live):** https://docs.google.com/presentation/d/13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs/edit
**Status:** ✅ 16 / 16 slides live. Economics refreshed to the 2026-06-28 post-frontier-seal model re-cascade.
**Method:** Duplicate of the live Grab Thailand deck, then **edited in place via the Slides API**. No full-replace, no PPTX round-trip. Imagery and the gold/navy visual system inherited from the Grab gold deck and preserved throughout.

---

## Round 2026-06-28 — economics re-cascade apply (Tasklet Slides lane)

Applied Grok's post-seal model re-cascade to the two aggregate slides, in place, style-preserving via scoped `replaceAllText` (per `pageObjectIds`, `matchCase:true`). Source of truth: `deck-studio/decks/gojek/deck-economics-values-gojek.json` cross-checked against `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json`.

### Slide 4 — network overview (page `g3eec5122801_0_0`)
| shape | field | old → new |
|---|---|---|
| `g3eec5122801_0_6` | premium water corridors | **60 → 43** |
| `g3eec5122801_0_10` | premium sea-transfer spend / yr | **$127M → $169M** |
| `g3eec5122801_0_18` | SAM · near term | **$280M → $372M** |

### Slide 13 — "The Prize" ladder (page `g3eec5122801_0_562`)
| shape | rung | old → new |
|---|---|---|
| `g3eec5122801_0_570` | SOM (full network ~14% +greenfield) | **$87M → HELD** (see flag) |
| `g3eec5122801_0_574` | SAM · near term | **$280M → $372M** |
| `g3eec5122801_0_578` | marine-transfer TAM (midpoint) | **$1.12B → $1.5B** |
| `g3eec5122801_0_582` | journey GMV | **$3.36B → $4.5B** |
| `g3eec5122801_0_586` | partner platform revenue | **$151M → $201M** |

Reported `occurrencesChanged`: 1/1/2/1/1/1 — exactly as scoped (the bare `60→43` matched once, no collateral). Post-apply re-pull confirmed all new values present and **no stale token** (`$127M`/`$280M`/`$1.12B`/`$3.36B`/`$151M`/`60`) remaining anywhere on the two pages. Gold Exo 2 bold (RGB .772/.615/.372) on every value cell preserved; descriptors untouched. No title/label/caption text changed — partner-copy lint scope unaffected (numeric tokens only).

### Held / flagged (honest — null beats confidently-wrong)
1. **SOM ladder rung ($87M) — HELD.** The values file maps `$22M` (a ~10%-capture *floor*) onto this rung, but the live rung is the **"SOM full network (~14% capture, today, +greenfield)"** metric per the standing SOM convention. Swapping in the floor would silently change the metric basis and lower the headline while the descriptor still reads "~14% +greenfield." The re-cascade did **not** supply an updated full-network SOM at the +greenfield basis. → Grok to provide post-seal full-network SOM (+greenfield basis) **or** confirm redefining the rung as the floor (which also requires the descriptor rewrite).
2. **Corridor count (43).** Applied from the purpose-built deck-values sidecar (card meaning = "premium water corridors mapped from real demand"). Note the data pack's `corridors_bound: 49` is the *total bound* count including roadmap/Quanta-LR corridors held null; 43 = grounded "today" subset. Flagged for Grok confirmation of which count the card should display.

### Not touched (per handoff scope)
- Slides 8–12 unit-econ deep-dives (Bali, Singapore, Riau, Komodo, Likupang) — already shipped.
- Lombok + Lake Toba per-market KPI cards — `kpis:null`, no grounded floor; held off-deck.
- Map backgrounds (Thailand artifact) — Jaideep's insert lane.

---

## Earlier round (unit economics + cover logo)

### Slides 8–10 — "What one boat earns" (unit economics)
Filled the three marquee unit-economics tables, replacing the inherited Thailand/Phuket placeholders with Indonesia-grounded numbers. Source: `data-clean/economics_by_route_id.json` (market-tagged, physics-grounded, partner-agnostic records). Each table's lines tie internally (revenue = seats × fare × legs; opex sums; EBITDA; payback = capex ÷ EBITDA). Run-cost basis is the sealed model stack (crew $21.6k, marina $10k, maintenance $10k, insurance $15k, charging $18k, $600k capex, 274 operating days). Full breakdowns captured in `ECONOMICS-SIDECAR.json`.

| slide | cluster | marquee corridor | route_id | rev/boat/yr | margin | payback |
|---|---|---|---|---|---|---|
| 8 | Bali | Benoa → Six Senses Uluwatu | `rn-c256a044c8be` | $865,810 | 91% | 0.76 yr |
| 9 | Singapore | ONE°15 Sentosa Cove → Harbour Bay | `rn-76264638fa6b` | $430,980 | 82% | 1.7 yr |
| 10 | Riau ↔ Singapore | Riau Islands → ONE°15 Sentosa | `rn-2568d40ee060` | $391,820 | 80% | 1.9 yr |

> Slide 10 marquee was switched from Jakarta's own intra-city water economics (honest but weak — ~14-yr payback) to the **Riau ↔ Singapore cross-border** corridor, a flagship-strength example that still sits inside the deck's footprint. Decision: Jaideep, 2026-06-27.

Style preservation verified on the live deck after a delete+insert edit (title gold Exo2, headline white 22pt, corridor sand Poppins, summary centered, value cells END-aligned) — runs retain color/font/weight/alignment.

### Slide 1 (cover) — partner logo
Swapped the inherited Grab mark for the **Gojek white wordmark** in the top-right partner-logo slot (`p1_i5`), re-fit to the wordmark's 4.2:1 aspect, anchored top-right opposite the Navier wordmark. Rendered cover logo verified byte-identical to the banked asset. Logo provenance + banking: `assets/logos/partners/gojek/LOGO-SOURCE.json`.

## Held / null (honest)
- 20 shared/unbound corridors on the partner page carry `-shared` or `null` `route_id` — left null for Grok seal-bind (not invented).
- No model derivation performed here; economics are deck-application of already-sealed per-corridor records.

## Provenance
- Partner page: `partner-pitch/partners/gojek.json` (route_id discipline clean; archetype chips plain English).
- Economics sidecar: `decks/gojek-indonesia/ECONOMICS-SIDECAR.json`.
- Deck values: `deck-studio/decks/gojek/deck-economics-values-gojek.json`.
- Data pack: `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json`.
- Logo: `assets/logos/partners/gojek/logo-gojek.png` + `LOGO-SOURCE.json`.
