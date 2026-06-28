# Grok handback — Tasklet AFK run (2026-06-28)

**Baseline:** `main` @ `4a924286`  
**Production:** https://navier-atlas.vercel.app (deploy `234e2ef5` PH seal; deck-prep + gojek sidecar on `4a924286`)

---

## 1 · Gojek deck P3-D (live Slides — Tasklet done; Grok partial)

### Tasklet (do not redo)
- Live deck `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs`: stale `/grab/…` links → `/gojek/bali|singapore|jakarta`; slide-4 markets-neutral; Komodo + Likupang unit-econ deep-dives live (5 proofs before Prize ladder).

### Grok done
- **`decks/gojek-indonesia/ECONOMICS-SIDECAR.json`** — added model-grounded marquee rows:
  - Komodo `rn-871e5ff3b6a7` → $588K / 87% / 1.17 yr
  - Likupang `ics-c142307006` → $548K / 86% / 1.27 yr
  - Now 5 corridors: Bali, Singapore, Riau↔SG, Komodo, Likupang

### Grok held (your machine / model engine)
- **10-market data pack** + full **ladder re-cascade** (prize ladder rungs) — spec referenced in Tasklet handoff not yet in git; run via `finance/recal/` + `deck-studio/decks/gen_deck_economics.py gojek` when ready
- **Lake Toba / Sumba grounding** — Toba routes sealed (`rn-db305ed7f029` etc. on main); Sumba corridors still greenfield per `TASKLET-HANDOFF-PHASE3-PENDING.md`
- Maps: Tasklet left map drops to you

---

## 2 · AirAsia MOVE Phase 2 — PR #132 ✅ MERGED + DEPLOYED

| Field | Value |
|-------|-------|
| Branch | `airasia-move-phase2` → merged to `main` |
| Commit | `234e2ef5` (seal), base phase2 `0024f20b` |
| PR | #132 (merged locally + pushed; gh merge API timed out) |
| Script | `scripts/grok-airasia/seal_airasia_philippines.py` |
| Receipt | `handoff/airasia-move-2026-06-27/AIRASIA-PHILIPPINES-SEAL-RECEIPT.json` |

### Seal summary
- **18 PH corridors** bound (10 reuse + 8 mint) across manila/cebu/boracay/palawan/siargao
- **38 bindings** (journey + growth_case duplicates) in both `data-clean/` + `partner-pitch/` mirrors
- **`manila-philippines`** promoted `priority_city` → `city[]`
- PH `network_footprint` **render: geometry** (5 markets)
- **`_philippines_seal`** block added
- **`_map_scope`**: 40 cities via `partner-scope.mjs`
- **Preflight:** PASS · **linkage:** 0 gaps · **deploy:** https://navier-atlas.vercel.app @ `234e2ef5`

### Explicit nulls / held
| Item | Status |
|------|--------|
| PH + SG `growth_case` numerics | `model-pass-pending` |
| PP↔El Nido 125nm | `rn-81f865bba3ac` minted, `_roadmap` / Quanta-LR |
| SG↔Tioman | `ics-1a53f8237d` roadmap (inherited) |
| SEAL hash | FEATURES_BY_TYPE + ROUTES differ — Tasklet re-seal advisory |

---

## 3 · AirAsia MOVE deck — PR #133 ✅ PREP MERGED; create/bind PENDING

| Field | Value |
|-------|-------|
| Commit | `9119c606` (merge), prep `20253a18` |
| Artifacts | `deck-studio/decks/airasia-move/{deck.config,slide-manifest,content-source,image-manifest}.json` |
| Handoff | `handoff/partner-map-model/airasia-move-2026-06-28/GROK-PARTNER-DECK-CREATION-PROMPT.md` |
| Template | Grab Thailand `11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo` |
| `deck_id` | `pending-grok-create-or-bind` |

### Grok held
- **Slides API create/bind** — needs Google OAuth (skipped per backlog)
- **AirAsia MOVE logo** — `needs_sourcing`; bank under `assets/logos/partners/airasia-move/`
- **Economics slide** — frame-only; `model-pass-pending` (no invented TAM/capture)
- **Route appendix** — now includes sealed PH corridors from §2; run `partner_copy_lint.py` before seal

---

## Review surfaces (Jaideep)

1. **PR #132** — merged; live at `/airasia-move/manila|cebu|boracay|palawan|siargao|singapore`
2. **Gojek live deck** — 5 unit-econ proofs; ladder re-cascade + Toba/Sumba maps still open
3. **PR #133 deck-prep** — ready for Grok create/bind when OAuth + logo land

---

*Grok seat · No self-certified deck completion · Null beats wrong*