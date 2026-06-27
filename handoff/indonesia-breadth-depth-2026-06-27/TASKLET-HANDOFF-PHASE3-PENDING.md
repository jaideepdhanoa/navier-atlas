# Tasklet handoff — Indonesia breadth & depth (Phase 3 ready)

**Updated:** 2026-06-27  
**Grok handback:** `GROK-HANDBACK-indonesia-frontier-seal.md`  
**Receipt:** `INDONESIA-SEAL-RECEIPT.json`  
**Live:** https://navier-atlas.vercel.app (post-deploy)

---

## Phase 1 — Tasklet DONE

- Gojek 10 Indonesia sub-proposals + Grab mirror
- Footprint: 13 Indonesia geos + Singapore on both partners
- Merged PRs #129 + #130 @ `f39c996d`

## Phase 2 — Grok DONE

See `GROK-HANDBACK-indonesia-frontier-seal.md`:
- Lake Toba minted (3 routes: `rn-db305ed7f029`, `rn-89174b6f31fe`, `rn-35e2eb8d3ca0`)
- lake-toba / likupang / singapore / lombok bindings cleared
- +28 economics stubs (bite2 lane)
- Build 7414 routes; preflight PASS

## Phase 3 — Tasklet owns next

1. **Economics cascade** — replace bite2 stubs with deck-grounded rows per Indonesia market (gojek + grab)
2. **Bind held nulls** where corridor registry completes: Sumba (7), komodo Pink Beach (2), likupang Lembeh (1)
3. **Raja Ampat corridor registry** — register `ics-*` refs into `corridors.json`, full cascade
4. **Roll-up dots** — karimunjawa, banda, derawan, wakatobi: mint ≥1 corridor each for dot+line render
5. Cascade → transparent sheet (in place) + master tracker + economics sidecar
6. Parity QA Gates A–F both partners
7. Decks remain untouched

## Also on main (Grok)

- **P0b Careem fidelity** @ `de43b1e5` — PASS_WITH_FLAGS, 3 hub journeys
- **P0c partner scope live inheritance** — hub maps inherit `CLUSTERS.json` at build

## Held items (do not invent)

| Geo | Gap |
|-----|-----|
| likupang | Lembeh 18nm — no sealed route |
| komodo-flores | Pink Beach — pending BP seal |
| sumba | All corridors — greenfield |
| roll-up dots | No minted corridors yet |

---

*Tasklet may proceed with Phase 3 economics cascade.*