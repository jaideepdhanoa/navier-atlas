# Tasklet handoff — Slides API lane (Gojek ladder + AirAsia deck)

**Updated:** 2026-06-28 post **PR #134** merge (`deck-studio-record-sync-2026-06-28`)  
**Baseline:** `main` after merge + deploy  
**Grok model engine:** complete · **Tasklet Slides lane:** open

---

## PR #134 merged — what changed

| Item | Status |
|------|--------|
| Gojek `deck.config.json` + `slide-manifest.json` | Synced to **live 16-slide** deck `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` |
| AirAsia MOVE logo | **Banked** — `assets/logos/partners/airasia-move/logo-airasia-move.png` + `LOGO-SOURCE.json` |
| AirAsia `deck.config.json` | Logo `status: banked`; economics **model-pass-complete** (Grok 2026-06-28) |
| `GROK-SPEC-gojek-p3-economics-refresh.md` | Tasklet spec on file; **Grok cascade already run** — see values below |

---

## Workstream A — Gojek: apply refreshed ladder (Slides API)

### Do not redo
- Slides 8–12 unit-econ deep-dives (Bali, SG, Riau, Komodo, Likupang)
- Cover logo, `/gojek/*` links, 16-slide structure
- `decks/gojek-indonesia/ECONOMICS-SIDECAR.json`

### Apply now (in place, style-preserving)

| Slide | Content | Source |
|-------|---------|--------|
| **3** (overview) | 4 network KPIs + **10-market grid** | `deck-studio/decks/gojek/deck-economics-values-gojek.json` → `slide3_kpi` |
| **11** (The Prize) | 5 ladder rungs | same → `slide10_tam.rungs` |

**MID ladder values (cite these):**

| Rung | Value |
|------|-------|
| SOM floor | **$22M** |
| SAM | **$372M** |
| Marine TAM | **$1.5B** |
| Journey GMV | **$4.5B** |
| Partner platform revenue | **$201M** |

**Hold null on deck:** `lombok` + `lake-toba` per-market KPI cards (`kpis: null` in values file).

**Method:** pull live OID inventory first; text-replace only; `partner_copy_lint.py` blocking; update `decks/gojek-indonesia/BUILD-LOG.md`.

---

## Workstream B — AirAsia MOVE: create/bind deck

### Ready (no longer blocking)
- Logo **banked** (PR #134)
- Economics **model-pass-complete** — floor ~$18M, SAM ~$356M, TAM ~$1.42B (`finance/recal/growth-airasia-move.json`)
- PH 18 corridors sealed (PR #132)

### Tasklet steps
1. Duplicate Grab Thailand `11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo` → write `deck_id` to config + manifest
2. Apply copy from `content-source.json` / `partner-pitch/partners/airasia-move.json`
3. Economics slide (7): use `growth_case.revenue_potential.rungs` — arriving-seat basis, plain English
4. Cover: Navier + banked AirAsia MOVE logo (`logo-airasia-move.png`)
5. Route appendix: sealed PH + SG/MY/TH/ID; **PP↔El Nido** `rn-81f865bba3ac` = Quanta-LR roadmap (not floor)
6. Images per `image-manifest.json`; `partner_copy_lint.py` green before done

**Prep:** `deck-studio/decks/airasia-move/` · prompt: `handoff/partner-map-model/airasia-move-2026-06-28/GROK-PARTNER-DECK-CREATION-PROMPT.md`

---

## Tasklet handback contract

Branch · PR · commit SHA · `deck_id`(s) · QA thumbnails · `partner_copy_lint` · BUILD-LOG · explicit nulls.

**Null beats wrong.**