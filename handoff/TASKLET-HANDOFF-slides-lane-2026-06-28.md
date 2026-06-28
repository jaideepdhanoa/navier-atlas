# Tasklet handoff — Slides API lane (Gojek ladder + AirAsia deck)

**From:** Grok (model engine complete) → **To:** Tasklet (Slides API apply)  
**Baseline:** `main` @ `1b04ae93`  
**Grok does NOT own:** live deck edits, OAuth, logo sourcing, image publish

---

## Why Tasklet (not Grok)

Jaideep attempted Google OAuth for the Grok/MCP Slides lane; the consent screen showed **"Polished CX"** (the GCP OAuth app's published name on client `533129153761-…`). Tokens were **not** saved (`~/.config/google-drive-mcp/tokens.json` absent). **Tasklet should use its own Slides/Drive credentials** (same pattern as Grab Thailand, Ocean Whisperer, Gojek unit-econ slides 8–10).

---

## Workstream A — Gojek prize-ladder apply (existing live deck)

### Do not redo (Tasklet already shipped)
- Live deck `13nnvUWkTUbLNFLkxRpJPOGgbvDVRVDdXvdybRTseGBs` — slides 8–10 unit-econ proofs (Bali, SG, Riau, Komodo, Likupang)
- Cover logo, link fixes, markets-neutral slide 4
- `decks/gojek-indonesia/ECONOMICS-SIDECAR.json` + `BUILD-LOG.md`

### Tasklet owns now
Apply **model-grounded numbers** from Grok's 10-market re-cascade onto the Grab-gold template deck.

| Slide | What to apply | Source |
|-------|---------------|--------|
| **3** | 4 network KPI cards + **10-market grid** | `deck-studio/decks/gojek/deck-economics-values-gojek.json` → `slide3_kpi` |
| **11** | Prize ladder rungs (5 rungs) | same file → `slide10_tam.rungs` (maps to slide **11** on Grab template) |

**Ladder values (MID, cite these):**

| Rung | Value |
|------|-------|
| SOM floor | $22M |
| SAM | $372M |
| Marine TAM | $1.5B |
| Journey GMV | $4.5B |
| Partner platform revenue | $201M |

**Per-market grid:** 8 markets have KPIs; **hold null** for `lombok` and `lake-toba` (`kpis: null` in values file — honest, not invented).

### Binding + spec (read before edit)
- `handoff/gojek-indonesia/GROK-SPEC-economics-refresh.md`
- `handoff/gojek-indonesia/GOJEK-10-MARKET-DATA-PACK.json`
- `deck-studio/decks/gojek/{economics-binding,market-scope,deck-economics-values-gojek}.json`

### Method
1. Pull full object inventory from live deck (never assume OIDs from Grab Thailand).
2. Style-preserving text replace only (Exo2 gold titles, Poppins body — match existing slides 8–10).
3. Run `deck-studio/qa/partner_copy_lint.py` before calling done.
4. Update `decks/gojek-indonesia/BUILD-LOG.md` with slide 3 + 11 receipt.

### Grok already done (maps)
Sumba + Lake Toba corridors sealed — verify map render on `/gojek/sumba` and `/gojek/lake-toba` if touching map slides; no new mint needed.

---

## Workstream B — AirAsia MOVE deck create/bind (PR #133 prep)

### Template + visual
- **Structure:** Grab Thailand gold `11WCun1Xk1flPmqvvtYrYZXsL5yRb5KQoe0xvTQSppKo`
- **Dressing:** Minor Hotels cinematic full-bleed reference `1p5NtoaORRWyBpcsbfqnSB9PLg9yyTpvuzJAyBMjen4o` (imagery only)
- **Prep artifacts:** `deck-studio/decks/airasia-move/{deck.config,slide-manifest,content-source,image-manifest}.json`
- **Creation prompt:** `handoff/partner-map-model/airasia-move-2026-06-28/GROK-PARTNER-DECK-CREATION-PROMPT.md`

### Tasklet steps
1. Duplicate Grab Thailand → new deck; write real `deck_id` into `deck.config.json` + `slide-manifest.json`.
2. Apply copy from `content-source.json` / `partner-pitch/partners/airasia-move.json` (plain English; no taxonomy leaks).
3. **Economics slide (7):** Grok model pass is **complete** — use `growth_case.revenue_potential.rungs` from partner JSON (floor ~$18M, SAM ~$356M, TAM ~$1.42B). Basis = arriving-seat distribution-capture. Do not invent beyond model output.
4. **Route appendix (10):** include sealed PH corridors (18 from PR #132) + SG/MY/TH/ID sealed legs. Mark PP↔El Nido `rn-81f865bba3ac` as **Quanta-LR roadmap** (not in floor).
5. **Logo:** `needs_sourcing` — bank under `assets/logos/partners/airasia-move/` + `LOGO-SOURCE.json` before cover ships.
6. Images: registry-resolved only per `image-manifest.json`; no Atlas-generated art.
7. Blocking gate: `partner_copy_lint.py` green before seal.

### Model artifacts (Grok — read only)
- `finance/recal/growth-airasia-move.json`
- `finance/recal/agg-airasia-move.json`
- `scripts/grok-airasia/run_econ_cascade.sh` (repro command)
- PH seal receipt: `handoff/airasia-move-2026-06-27/AIRASIA-PHILIPPINES-SEAL-RECEIPT.json`

---

## Tasklet handback contract (both workstreams)

Return: branch · PR link · commit SHA · `deck_id`(s) · slide count · QA thumbnails · `partner_copy_lint` result · BUILD-LOG update · explicit nulls/held items.

**Null beats wrong.** No self-certified completion.