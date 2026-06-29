# Tasklet handback — Gojek economics re-cascade apply (PR #135)

**Status:** ✅ RESOLVED (2026-06-29) — PR #135 merged; Grok follow-ups complete  
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
| **SOM ladder rung** | ✅ **$110M** applied live (slide 13) | `SOM_full_network_navier_transport_rev_yr` mid from `growth-gojek.json`; replaces stale $87M. Slide-3 card still shows $22M **floor** (correct split). |
| **Corridor count** | ✅ **43 confirmed** | Grounded-floor ladder count (`agg-gojek.json` / `growth-gojek.json` source_rollup). 49 = scoped total incl. 6 Quanta-LR roadmap (>70nm). |
| **Lombok + Lake Toba KPI cards** | ✅ **estimated tier** | `routes_mapped` + `addressable_pool` only; rev/fleet null — sealed geometry, estimated demand, no grounded floor row. |
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