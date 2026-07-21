# GROK-SPEC — Per-partner-country census methodology + four-deck TAM cascade (2026-07-21)

**Decision owner:** Jaideep (2026-07-20/21). **Rule:** greenfield census is **per-partner** — but for a
**country-specific proposal / Google Sheet**, it is **per-partner-COUNTRY**. A Brazil proposal uses the Brazil
census for BOTH DiDi and inDrive (so the two Brazil sheets are identical). Mexico uses Mexico; Egypt uses Egypt.

## Two methodology bugs fixed in the shared generators (adopt going forward)

### Bug 1 — apples-to-oranges greenfield dedup (the big one)
`greenfield_census.py` counted **sourced** corridors by unique `route_id` but counted **greenfield** by unique
`(from,to)` **node-label pair**. Many ROUTES carry only coarse cluster labels ("Rio de Janeiro & Costa Verde"),
so 55 distinct sealed Brazil greenfield route_ids collapsed to 6 label-pairs — a ~9× undercount that made Brazil's
census look artificially thin.
**Fix (shipped):** count greenfield by unique `route_id`, symmetric with the sourced side (atlas ROUTES are already
undirected-unique at seal time). Any cascade / sheet / TAM-ladder builder that recomputes a census MUST count both
sides the same way.

### Bug 2 — whole-partner census leaking into country sheets
`build_transparent_sheet.py` previously fell back to the Grab-Asia template (4.9×) and, when hand-patched, used the
**whole-partner** census (DiDi LatAm-wide 5.45). For a country deck this over- or under-states width.
**Fix (shipped):**
- `greenfield_census.py` gains `--country <Country>`: scopes sourced corridors (agg `country` field), corridor
  endpoint resolution, and geography to that one country; greenfield self-scopes via the country's city set.
- `build_transparent_sheet.py` gains `--greenfield-json <path>` (mirrors `growth.py`) so a country sheet consumes
  the per-partner-country census, and both cost engines (golden rule #7) tell one story.

**Going-forward rule for Grok's cascade + sheet + TAM-ladder builders:** for a country-scoped artifact, always load
`finance/recal/greenfield-census/<partner>-<country-slug>.json`; never the whole-partner `<partner>.json` and never
a peer's census. Two Brazil partners → one Brazil census file value.

## Authoritative per-partner-country censuses (committed)
| File | sourced | greenfield | g (low/MID/high) |
|---|---|---|---|
| `didi-mexico.json` | 5 | 52 | 3.451 / **4.922** / 6.393 |
| `didi-brazil.json` | 12 | 55 | 2.146 / **2.833** / 3.521 |
| `indrive-brazil.json` | 12 | 55 | 2.146 / **2.833** / 3.521 (= DiDi Brazil ✓) |
| `indrive-egypt.json` | 2 | 32 | 3.661 / **5.258** / 6.855 |

## Corrected MID TAM ladders (deterministic — verified in growth.py AND the transparent sheet)
Backing Sheets already updated in place (URLs preserved). Grok: re-render THE PRIZE / TAM-ladder slides on the four
decks to match. **SOM Full = SOM Full Mapped Network** (the headline rung); DiDi carries the platform-take rung,
inDrive stops at Journey GMV.

| Deck | census | SOM Full | SAM | Journey GMV | Platform take |
|---|---|---|---|---|---|
| DiDi Brazil | 2.833 | **$220.8M** | $1,007.1M | **$12.09B** | $543.8M |
| inDrive Brazil | 2.833 | **$220.8M** | $1,007.1M | **$12.09B** | — |
| DiDi Mexico | 4.922 | **$147.9M** | $677.1M | **$8.13B** | $365.6M |
| inDrive Egypt | 5.258 | **$39.0M** | $70.2M | **$0.241B** | — |

Grounded SOM floors (greenfield-independent, unchanged): DiDi/inDrive Brazil $77.9M; DiDi Mexico $30.0M;
inDrive Egypt $7.4M.

## Backing Sheets (updated in place — verified greenfield-factor input cell)
| Deck | Sheet ID | g cell (lo/mid/hi) |
|---|---|---|
| DiDi Brazil | `13BViN3uXgVK8uO8KXRIVwgAZnPrDedNfaRnTIjhpbLA` | 2.146 / 2.833 / 3.521 |
| DiDi Mexico | `1AtoSyNtAZtYiW-duU0oxZTgdtpWW4Al3xuUAHnqlFg0` | 3.451 / 4.922 / 6.393 |
| inDrive Brazil | `1N1pPyZrJFa_mV_3MTMxw1eEs6yC-oeBl2jyd93kvvWY` | 2.146 / 2.833 / 3.521 |
| inDrive Egypt | `1qD2uF6v3ZnPhLtDnmwnf-hV70nq745PYXiF11p_ZpUU` | 3.661 / 5.258 / 6.855 |

## Grok actions
1. **Adopt** the two methodology fixes in the deterministic cascade + Google-Sheet + TAM-ladder builders (per-country
   census discovery; route_id-symmetric greenfield count). Never revert a country artifact to the whole-partner census.
2. **Re-render** THE PRIZE / TAM-ladder slides on the four live decks to the corrected MID ladders above.
3. **inDrive Egypt Phase-4** ladder refresh uses the Egypt census (g 5.258): SOM Full $39.0M / Journey GMV $0.241B.
4. **Rebuild the economics sidecars** (`economics_by_route_id.json`) into the gold zips from the refreshed
   `agg-*.json` (per-corridor unit economics are census-independent and unchanged — only the ladder rungs move).

## Reproduce (deterministic)
```
# census (per country)
python3 finance/model/greenfield_census.py --partner didi --country Brazil --json finance/recal/greenfield-census/didi-brazil.json
# sheet (per country)  — engine #2, must match growth.py
uv run --with openpyxl python3 finance/build_transparent_sheet.py --partner didi \
  --corridors finance/recal/corridors-didi-brazil.json --agg <brazil-agg> \
  --greenfield-json finance/recal/greenfield-census/didi-brazil.json --out <out>.xlsx
# ladder (engine #1)
python3 finance/model/growth.py --partner didi --agg <brazil-agg> \
  --greenfield-json finance/recal/greenfield-census/didi-brazil.json --json <growth>.json
```
Scoped corridors + per-country census files are committed under `finance/recal/`.
