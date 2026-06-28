# Tasklet handoff — Slides API lane (Gojek ladder + AirAsia deck)

**Updated:** 2026-06-28 post Tasklet handback (**PR #135** receipt)  
**Baseline:** `main` @ `abd7c599` · PR #135 OPEN @ `93971c98`  
**Grok model engine:** complete · **Tasklet Gojek apply:** ✅ slides 4+13 live · **AirAsia deck:** open

---

## PR #134 merged — what changed

| Item | Status |
|------|--------|
| Gojek `deck.config.json` + `slide-manifest.json` | Synced to **live 16-slide** deck `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` |
| AirAsia MOVE logo | **Banked** — `assets/logos/partners/airasia-move/logo-airasia-move.png` + `LOGO-SOURCE.json` |
| AirAsia `deck.config.json` | Logo `status: banked`; economics **model-pass-complete** (Grok 2026-06-28) |
| `GROK-SPEC-gojek-p3-economics-refresh.md` | Tasklet spec on file; **Grok cascade already run** — see values below |

---

## Workstream A — Gojek: apply refreshed ladder (Slides API) — ✅ DONE (partial)

**Handback:** `handoff/gojek-indonesia/TASKLET-HANDBACK-PR135-2026-06-28.md`  
**PR #135** @ `93971c98` · BUILD-LOG updated · merge **parked**

### Applied live (2026-06-28)
| Slide | Content | Result |
|-------|---------|--------|
| **4** (network overview) | corridors, spend, SAM | 60→43 · $127M→$169M · $280M→$372M |
| **13** (The Prize) | ladder rungs (except SOM) | SAM $372M · TAM $1.5B · GMV $4.5B · platform $201M |

Numeric tokens only — no title/label/caption changed; partner-copy lint unaffected.

### Held → Grok
| Item | Notes |
|------|-------|
| **SOM rung ($87M)** | $22M floor in values file vs "~14% +greenfield" descriptor on live rung |
| **Corridor count** | 43 applied vs 49 in data pack — confirm card meaning |
| **Lombok + Lake Toba KPIs** | `kpis: null` — held off-deck |
| **Map backgrounds** | Jaideep lane |

### Do not redo
- Slides 8–12 unit-econ deep-dives (Bali, SG, Riau, Komodo, Likupang)
- Cover logo, `/gojek/*` links, 16-slide structure
- `decks/gojek-indonesia/ECONOMICS-SIDECAR.json`

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