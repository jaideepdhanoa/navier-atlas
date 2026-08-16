# Archetype microsite polish review — Boston pilot (2026-08-15)

**Verdict:** Employer page = the bar (punchy hero + stat chips, planner up front, clean copy). Public Partners = decent skeleton, wordy, leaks internal method. Fleet Investors = fails the bar: renders internal provenance verbatim, P&L is paragraph soup, jargon everywhere. Root cause is split — fix both sides before any city replication.

---

## A · Root cause 1 — TASKLET (authored data + spec contract)

The v1 spec said *"status labels render verbatim."* Right instinct (fail-closed honesty), wrong surface (that's internal-doc discipline applied to a partner page). Result: BLS methodology paragraphs, file names, validation dates, and QA notes on a public page.

**Confirmed leaks (authored by us, rendering today):**
1. `Sources: REVENUE-LEVER-BENCHMARKS.md + CARGO-LAYER-BENCHMARKS.md` — internal file names on page.
2. Crew opex row: full BLS OEWS citation, ECEC multiplier, May-2023 date, `handoff/archetypes/CREW-COST-BENCHMARKS.md` path.
3. Demand pool: `Capture assumption: 3.0% of on-site headcount (tracker's own stated input)... verify before quoting` + `5 of 10 tracked nodes have zero sourced headcount — pools understate` + BOS-5 phasing QA note.
4. Maintenance row: `N45 NOT validated — N30 canon ($65K/yr) floor...` — "canon" is internal vocabulary; "NOT validated" is internal status.
5. Stack layer IDs `L1/L2/L3/U1/U2` + per-layer italic provenance sentences (`Benchmark-anchored; canon-consistent; no Boston operations yet`).
6. Fleet phasing: `Derived, not published. No spares margin included.` / `illustrative capacity-ceiling planning tool, not a timetable` — modeling-methodology voice.
7. Hero sublines lead with disclaimers (`never the base case`, `no anchor subsidy in any case`) — defensive, not selling.
8. Public Partners: `per-stop verification status intentionally omitted from this page (fail closed)` and `Bodies whose posture is unverified... intentionally omitted (fail closed)` — we rendered the *description of our honesty process* instead of just being honest.
9. Raw URLs inline in body copy; `(hub topology / node inventory)` source parentheticals; `(attributed to Länsstyrelsen, the county administrative board)`.
10. Speed-rule section: our ask is right but 4 paragraphs of regulatory exegesis; 323 CMR 2 detail belongs in one line + footnote.
11. Line IDs (`BOS-1, BOS-2`) in demand-pool table — humans get line names.

**Fix — data contract v2 (authored by Tasklet, done):**
- Every renderable object gets at most: `title` (≤6 words), `value`/figures, `note` (≤140 chars, partner-clean plain English), `status` (enum: `market_priced` | `modeled` | `upside`), `fn` (optional footnote key).
- ALL provenance, validation history, internal caveats move to `_provenance` / `_internal` fields (underscore = never render; already contract).
- One consolidated `footnotes` block per page: short, numbered, plain English (e.g. *"Pricing benchmarked to Boston operators' published fares, 2025–26. Navier has not yet operated in Boston."*). This carries the honesty load in one calm place instead of stamping every module.
- Heroes rewritten to sell first, qualify once: stat chips (employer-page pattern) + a single small-print line.
- Economics module restructured as **table rows** (`line`, `per_mo_low/high`, `note`, `status`), not paragraphs — deck unit-econ grammar.
- Scenario table + toggle stays (it worked). Payback = the gold number.
- Demand pool: line names, seats column, one footnote for the indicative label + capture assumption. Node-coverage QA lives in `_internal`.
- Jargon kill-list enforced by scan: canon, tracker, MECE, fail closed, L1/L2/L3/U1/U2, phase-3 line, BLS/OEWS/ECEC, file names/paths, validation dates, "not validated", "placeholder".

## B · Root cause 2 — GROK (template changes to request)

1. **Never render `_`-prefixed fields** (already contract — reaffirm) and render only `title/value/note/status/fn` from v2 objects. Drop all per-module italic caveat lines.
2. **Footnote system:** superscript markers on `fn` refs → one "Notes & assumptions" section above the contact form. Small, numbered, no links to internal docs.
3. **P&L component (the big one):** replace layer-cards + opex-paragraph-table with a deck-style unit-econ table: revenue rows (right-aligned $ ranges) → gross subtotal → opex rows → net → payback band. Status enum renders as small chips (gold `MARKET-PRICED`, gray `MODELED`, outlined `UPSIDE`). Upside rows visually separated below net (never summed into base). Scenario toggle stays; per-scenario stat chips stay.
4. **Hero stat chips** on both new pages (employer-page pattern): Fleet = `$2.5M / vessel · ~4.3 yr mid payback · 60–80 seat launch trigger · 5 corridors`. Public = `18 stations · 0 terminals to build · 0 subsidy ask · 1.5M harbor riders 2025`.
5. **"The model" section** → five compact role cards (grid), ≤18 words each, not stacked full-width sentences.
6. **Sources:** inline raw URLs → small domain chip or footnote marker. Never a naked URL in body copy.
7. **Speed-rule relief (Public Partners):** collapse to headline + 3 chips (Wake ✓ measured · Noise ✓ electric · Precedent ✓ Stockholm) + one-sentence ask + footnote. Keep the expander for detail.
8. **Fleet phasing table:** keep, but launch/full-build framed as `Launch fleet 3–6 vessels · $7.5–15M` vs `Full network 19 vessels · $47.5M` stat pair + table; methodology text becomes one footnote.
9. **Section rhythm:** match employer page — each section = headline + ≤2 lines of copy + a visual object (chips/table/map/cards). No section with >3 consecutive paragraphs.
10. **Typography parity** with employer page (same scale, spacing, gold accents).

## C · Division of labor
- **Tasklet (done in this pass):** contract v2 in spec §5; both Boston JSONs rewritten to v2 (copy, footnotes, provenance split, table-structured P&L); jargon scan added to QA gates.
- **Grok:** template changes B1–B10; rebuild Boston pilot pages from v2 JSONs; then QA re-run against spec §7 (updated).

**Rule going forward:** no city replication until Boston passes the employer-page bar side-by-side.
