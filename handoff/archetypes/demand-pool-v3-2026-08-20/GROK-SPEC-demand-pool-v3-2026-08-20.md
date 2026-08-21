# GROK SPEC — Demand pool v3: render what we already author

**Date:** 2026-08-20 · **Owner split:** Tasklet authors data + gates; Grok implements template + reseal.
**Scope:** `employer-hub/template/archetype.js` (`renderDemandPool`) + `employer-hub/hubs/{city}/fleet-investors.json`.

---

## 1 · Why this exists

Fleet-investor pages are meant to answer "who actually rides these corridors". The data pipe already
exists — every city's `fleet-investors.json` has a `demand_pool` block, and the template renders a
five-column table. But the authored data and the renderer have drifted apart, so most cities show
nothing useful.

Audited state of all 15 cities, 2026-08-20:

| Renders correctly | Authored richer than the renderer | No employer rows at all |
|---|---|---|
| Boston (9 rows) | Seattle (16), Miami (10), Washington DC (8) | **Bay Area, New York** |

Plus nine cities — Istanbul, Bahrain, Abu Dhabi, Dubai, Jeddah, Ras Al Khaimah, Red Sea Global,
Saudi Eastern Province, San Diego — put stop/cluster rows into an employer-shaped table, so the
Employer column renders blank.

Three concrete defects:

1. **`value` and `note` are authored and silently dropped.** Seattle authors `value` (`"~12,000 workers"`,
   `"5,076 employees (2025 city data)"`) and a plain-English `note` on every row. Miami and DC author
   `note` on every row. The renderer reads neither. Seattle therefore renders sixteen rows of "—" in
   both numeric columns, and Miami's walk-time notes — the entire point of those rows — never appear.
2. **`standing_label` never renders from data.** The renderer falls back to `dp._internal.standing_label`,
   but `stripUnderscoreKeys()` in `scripts/build-employer-hubs.mjs` removes every `_`-prefixed key before
   the client sees it. Every one of the 15 pages is therefore showing the hardcoded default string.
3. **No fail-closed guard.** A row with no number and no note still renders as a line of dashes.

Nothing here needs new research. It needs the renderer to catch up with the data.

---

## 2 · Row contract v3

```jsonc
{
  "node":  "Oyster Point Ferry Terminal / Oyster Point Marina",  // exact verified landing label from hub.json stops[].label
  "lines": ["Peninsula Trunk", "Southeast Bay Line"],            // exact line names from hub.json lines[].name
  "employer": "Genentech",
  "value": "~12,000 on site",                                    // OPTIONAL string, never a bare number
  "note":  "The largest employer on the Oyster Point campus — a walk from the terminal.", // OPTIONAL, <=140 chars
  "fn":    "fn12"                                                 // OPTIONAL footnote ref
}
```

**`value` is a string, deliberately.** A `Headcount: 45000` cell asserts a precision we do not have.
`"~45,000 system-wide"` carries the same evidence and its own caveat. Seattle already does this; it is
the standard. `headcount` (number) stays supported for Boston until §6 migrates it.

**`note` carries the walk/shuttle truth.** This is the honesty gate that matters most to an investor:
whether a headcount is a two-minute walk or a seven-mile ground shuttle. It is already authored in
three cities and has never been visible.

---

## 3 · Template changes (`renderDemandPool`)

1. **Demand column** — render `r.value` when present; else format `r.headcount`; else `—`.
   Column header becomes **"Demand pool"**, not "Headcount".
2. **Note** — render `r.note` as a muted second line inside the employer cell, not a sixth column
   (a sixth column breaks the table on mobile). Omit the element entirely when absent.
3. **Standing label** — read `dp.standing_label` top-level. **Delete the `dp._internal.standing_label`
   fallback**: it is dead code, the build strips `_` keys. Keep the hardcoded default as last resort.
4. **Plain-English header** — rename the `Node` column to **`Stop`**. "Node" is on the banned-jargon
   list for external copy and is currently rendering on every page.
5. **Fail closed** — skip any row where `value`, `headcount` and `note` are all empty. Do not render
   a row of dashes.
6. **Footnotes** — render `r.fn` as a superscript ref bound to the page's existing footnote block.
7. **Stop-led variant** — support `data.table_variant: "employer" | "stop"` (default `"employer"`).
   When `"stop"`, drop the Employer column and render `Stop · Line(s) · Demand pool · Note`. Apply
   `"stop"` to the nine cities listed in §1 that have no employer-level rows. This removes the blank
   column without inventing employer names for them.

`data.capture_assumption`, `data.headcount_label` and `data.city_total_seats` already render — no change.

---

## 4 · Data in this package

`data/bay-area.demand_pool.json` — 16 rows, city total **3,441 indicative seats**
`data/new-york.demand_pool.json` — 14 rows, city total **2,769 indicative seats**

Drop these blocks in as the `demand_pool` key of the respective `fleet-investors.json`. They are
authored to the v3 contract, bound to real `hub.json` stop labels and line names, and canon-checked
against the landing gate and the verified employer universe. `DROP-LEDGER.md` records every row that
was in the source trackers and did **not** make it, with the reason.

Both blocks set `standing_label` top-level:

> Indicative of demand potential along these corridors — not commitments, commercial relationships,
> or discussions with the organisations named.

---

## 5 · Acceptance gate

- [ ] Seattle's 16 rows render `value` + `note`; no row shows "—" in the demand column.
- [ ] Miami's and DC's notes are visible on every row.
- [ ] Bay Area and New York render 16 and 14 rows, with city totals 3,441 and 2,769.
- [ ] The nine stop-led cities render no blank Employer column.
- [ ] `standing_label` on every page comes from data, not the hardcoded default. Verify by changing
      one city's string and confirming the page follows.
- [ ] Column header reads "Stop", not "Node", on all 15 pages.
- [ ] No row renders with all of `value`, `headcount`, `note` empty.
- [ ] Kill-scan the rendered DOM: `trigger` · `not yet operate` · `none committed` · `anchor` ·
      `canon` · `fail closed` · `.md` · `catchment` · `node` · dock-securing language. Zero hits.
- [ ] Full-length screenshots of `/fleet-investors/bay-area`, `/new-york`, `/seattle`, `/miami`
      at desktop and mobile widths, checked for reflow and clipping.

---

## 6 · Follow-on, not in this pass

Boston, Miami, Washington DC and San Diego should migrate from `headcount`/`seats` numbers to the v3
`value` string shape, so all fifteen cities read the same way. Boston is the only city currently
rendering a per-row `seats` column; that column is `headcount × 3%` applied row by row, which stacks a
modelled number on top of a directional one. The recommendation is one clearly-labelled city total
instead — which is what the Bay Area and New York blocks in this package do. See `MIGRATION-5-CITIES.md`.

**Do not action §6 in the same PR as §3.** Template change and city content are separate hand-backs.
