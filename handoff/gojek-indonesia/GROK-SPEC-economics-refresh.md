# Gojek Indonesia — economics refresh spec (Grok-owned)

**Live deck:** `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs`  
**Partner:** `gojek` · **Deck-studio:** `deck-studio/decks/gojek/`  
**Status:** cascade + deck values generated 2026-06-28; **Slides apply → Tasklet** (`handoff/TASKLET-HANDOFF-slides-lane-2026-06-28.md`)

---

## Scope

Re-cascade the **10 curated sub-proposals** after Lake Toba + Sumba seal-bind, then refresh:

1. **Slide 3** — network KPI cards + 10-market grid (`slide3_kpi`)
2. **Slide 11** — prize ladder rungs (`slide10_tam` in gen output → slide 11 on Grab-gold template)
3. **Slides 8–12** — unit-econ proofs stay on `decks/gojek-indonesia/ECONOMICS-SIDECAR.json` (Tasklet-applied; do not overwrite)

## 10 markets (deck order)

| key | label | seal status |
|-----|-------|-------------|
| jakarta | Jakarta & Thousand Islands | sealed |
| bali-nusa-gili | Bali, Nusa & Gili | sealed |
| lombok | Lombok & Gilis | partial (1 corridor unbound) |
| komodo-flores | Komodo & Flores | sealed |
| sumba | Sumba (Nihi) | sealed 2026-06-28 (`rn-33fe0cc24a60`, `rn-c77ad1314ae3`) |
| riau-singapore | Bintan & Riau ↔ SG | sealed |
| singapore | Singapore | sealed |
| raja-ampat | Raja Ampat | sealed |
| likupang | Likupang & Bunaken | sealed |
| lake-toba | Lake Toba (Samosir) | sealed (`rn-db305ed7f029` etc.) |

## Model engine commands

```bash
# Network ladder (growth_case on partner JSON)
./scripts/grok-bite2/run_partner_cascade.sh gojek mobility_ladder

# 10-market deck values
./scripts/grok-indonesia/run_gojek_deck_cascade.sh

# Deck values output
python3 deck-studio/decks/gen_deck_economics.py gojek
```

## Sources (read-only)

| artifact | path |
|----------|------|
| Network growth | `finance/recal/growth-gojek.json` |
| Per-market agg | `finance/recal/agg-gojek-deck-merged.json` |
| Deck binding | `deck-studio/decks/gojek/economics-binding.json` |
| Market scope | `deck-studio/decks/gojek/market-scope.json` |
| Generated values | `deck-studio/decks/gojek/deck-economics-values-gojek.json` |

## Ladder headline (post re-cascade @ 2026-06-28)

- **SOM floor:** ~$22M/yr Navier transport (network, 49 corridors)
- **SAM mid:** ~$372M Navier transport
- **Marine TAM mid:** ~$1.49B
- **Journey GMV mid:** ~$4.47B
- **Platform rev mid:** ~$201M

Per-market floor is in `agg-gojek-deck.json` → `rollup.grounded_floor_by_market`.

## Slides API apply (Tasklet-owned)

See `handoff/TASKLET-HANDOFF-slides-lane-2026-06-28.md` — Workstream A.

**Held null:** Pink Beach Komodo (`pending-bp-seal-pink-beach`); Quanta-LR corridors in `roadmap_quanta_lr_2026plus`; lombok + lake-toba deck KPI cards.

## Map grounding (Grok)

Lake Toba + Sumba lines now sealed — verify render on `/gojek/lake-toba` and `/gojek/sumba` after deploy.