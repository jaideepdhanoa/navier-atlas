# Tasklet handback — Gojek economics re-cascade apply (PR #135)

**Status:** ⏸ PARKED — receipt recorded; merge + Grok follow-ups deferred  
**Date:** 2026-06-28  
**Lane:** Tasklet Slides API (in-place, style-preserving)

---

## Receipt

| Field | Value |
|-------|-------|
| **PR** | [#135](https://github.com/jaideepdhanoa/navier-atlas/pull/135) |
| **Branch** | `gojek-economics-apply-2026-06-28` |
| **Commit** | `93971c98` |
| **Deck (live)** | `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` |
| **Slides edited** | **4** (network overview) + **13** (The Prize ladder) |
| **PR diff** | `decks/gojek-indonesia/BUILD-LOG.md` only |
| **Lint** | Numeric tokens only — no title/label/caption changed; partner-copy scope unaffected |

---

## Applied live (numeric)

### Slide 4 — network overview
| Field | old → new |
|-------|-----------|
| premium water corridors | 60 → **43** |
| premium sea-transfer spend / yr | $127M → **$169M** |
| SAM · near term | $280M → **$372M** |

### Slide 13 — The Prize ladder
| Rung | old → new |
|------|-----------|
| SAM · near term | $280M → **$372M** |
| marine-transfer TAM (midpoint) | $1.12B → **$1.5B** |
| journey GMV | $3.36B → **$4.5B** |
| partner platform revenue | $151M → **$201M** |

Source: `deck-studio/decks/gojek/deck-economics-values-gojek.json` cross-checked against `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json`.

---

## Held / null (Tasklet → Grok)

| Item | Status | Notes |
|------|--------|-------|
| **SOM ladder rung ($87M)** | HELD | Values file maps `$22M` floor; live rung descriptor reads "~14% capture +greenfield" — metric basis mismatch. Need post-seal full-network SOM at +greenfield basis **or** descriptor rewrite to floor basis. |
| **Corridor count (43)** | FLAG | Applied from deck-values sidecard; data pack `corridors_bound: 49` includes roadmap/Quanta-LR held null. Confirm which count the card should display. |
| **Lombok + Lake Toba KPI cards** | NULL | `kpis: null` in values file — no grounded floor; held off-deck. |
| **Map backgrounds** | Jaideep lane | Thailand artifact plates; Indonesia map insert not in Tasklet scope. |

---

## Not touched (per scope)
- Slides 8–12 unit-econ deep-dives (already shipped)
- Cover logo, `/gojek/*` links, 16-slide structure
- `decks/gojek-indonesia/ECONOMICS-SIDECAR.json`

---

## When we return

1. **Merge PR #135** (BUILD-LOG receipt onto `main`)
2. **Grok:** resolve SOM rung basis ($87M vs $22M floor vs new +greenfield SOM)
3. **Grok:** confirm corridor count 43 vs 49 for slide 4 card
4. **Jaideep:** map backgrounds on live deck
5. **Parked separately:** Google Sheets economics publish for gojek/airasia-move