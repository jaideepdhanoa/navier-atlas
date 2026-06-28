# Grok handback — held workstreams (2026-06-28)

## 1 · Slides lane

**Gojek apply — Tasklet handback received, PARKED**

→ `handoff/gojek-indonesia/TASKLET-HANDBACK-PR135-2026-06-28.md`  
PR #135 @ `93971c98` · live deck `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` · slides **4+13** applied

**Grok follow-ups when we return:**
- SOM rung basis ($87M vs $22M floor vs new +greenfield SOM)
- Corridor count confirm (43 vs 49)
- Lombok + Lake Toba KPI cards (null)
- Map backgrounds (Jaideep)
- Merge PR #135 BUILD-LOG receipt

**Still open (Tasklet):** AirAsia MOVE deck create/bind — see `handoff/TASKLET-HANDOFF-slides-lane-2026-06-28.md`

---

## 2 · Gojek — DONE (model engine)

| Item | Status |
|------|--------|
| Sumba seal | `rn-33fe0cc24a60`, `rn-c77ad1314ae3` + bindings |
| Lake Toba | prior seal confirmed in receipt |
| Network re-cascade | `growth-gojek.json` — floor ~$22M, SAM ~$372M |
| 10-market deck pack | `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json` |
| Economics spec | `handoff/gojek-indonesia/GROK-SPEC-economics-refresh.md` |
| Deck bindings | `deck-studio/decks/gojek/{market-scope,economics-binding}.json` |
| Deck values | `deck-studio/decks/gojek/deck-economics-values-gojek.json` |

**Held:** Slides apply → Tasklet; map QA on `/gojek/sumba` + `/gojek/lake-toba`

---

## 3 · AirAsia — DONE (model pass)

| Item | Status |
|------|--------|
| Economics cascade | `scripts/grok-airasia/run_econ_cascade.sh` |
| Demand apply | `apply_airasia_demand.py` (FLAG hub assumptions) |
| growth_case | **filled** — floor ~$18M, SAM ~$356M, TAM ~$1.42B |
| PP↔El Nido | `rn-81f865bba3ac` → `roadmap_quanta_lr` (excluded from floor) |
| SEAL hashes | `update_seal_hashes.py` run |

**Held:** AirAsia deck create/bind → Tasklet (+ logo sourcing)

---

## Scripts added

- `scripts/grok-indonesia/build_gojek_deck_corridors.py`
- `scripts/grok-indonesia/run_gojek_deck_cascade.sh`
- `scripts/grok-airasia/apply_airasia_demand.py`
- `scripts/grok-airasia/run_econ_cascade.sh`