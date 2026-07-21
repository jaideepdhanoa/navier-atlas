# Grok spec — DiDi Mexico deck Phase 4 (economics cascade + Holbox/Huatulco backup)

**From:** Tasklet · **To:** Grok · **After:** #318/#319 (Phase 3 cascade + Holbox reseal) and #308 (country-deck standardize) merged
**Deck:** `1XwKRuJtMrou8NtBdc1oY3LL2Dk83dCs9MCLvNKgwq0c` (DiDi × Navier — Mexico mobility review, live 14 slides)
**Editing mode:** Slides API only. Duplicate the Voi chassis city/econ layouts; substitute source-backed fields only.

## What Tasklet already did (no action needed, just verify)
1. **THE PRIZE (slide 10) refreshed LIVE** to the cascade MID ladder — verified readback:
   - SOM · Today **$163.8M** · SAM **$749.7M** · TAM **$3.0B** · GMV **$9.0B** · DiDi platform **$404.9M**
   - Please confirm on your inventory pull; no-op if already correct.
2. **DiDi Mexico Drive sheet updated in place** (`1AtoSyNtAZtYiW-duU0oxZTgdtpWW4Al3xuUAHnqlFg0`): Holbox resealed to 5.5 nm (10.64 yr), greenfield band set to the DiDi census (5.45), ladder verified live.
3. **`generated-deck-economics.json` regenerated & committed** from the updated `economics-binding.json` via `gen_deck_economics.py` (clean, `published_total_reconciled: true`, 5 grounded routes / 99 vessels / $30,047,216 floor). Confirm the committed `source_sha256` matches your re-run.

## Grok to do

### A. Market overview (slide 3, `g3eec5122801_0_0`) — refresh counts + narrative
From the updated `market-scope.json` / `generated-deck-economics.json`:
- **6** coastal cities in scope (Cancún–Isla Mujeres, Playa–Cozumel, Isla Holbox, Bahías de Huatulco supported; Puerto Vallarta, Los Cabos display/held)
- **5** supported routes with economics
- **$30.0M** supported annual route revenue (was $28.2M)
- **99** vessels at full network maturity (was 88)
- Narrative to name Isla Holbox and Bahías de Huatulco alongside the existing crossings; keep clean partner English.

### B. Generate 4 BACKUP slides (append after close; indices 15–18)
Per the locked country-deck spine (backup = new/secondary city deep-dives + one econ slide each). Use the Voi city chassis; do not author a new layout.

| # | Slide | Source |
|---|---|---|
| 15 | **Isla Holbox** city deep-dive | Chiquilá → Isla Holbox, 5.5 nm, sole passenger crossing to car-free Holbox. Route box canonical format (amber ▸, no vessel names). Atlas map slot **human-only**. |
| 16 | **WHAT ONE BOAT EARNS · HOLBOX** | `rn-8e76868a5b01`: rev **$141,082**/boat-yr · margin **40%** · payback **10.64 yr** · fare **$12**. 6 flush OPEX lines (Energy $5,505 · Crew $25,200 · Marina+overhead $11,000 · Maintenance $10,000 · Insurance $15,000 · Charging berth $18,000). |
| 17 | **Bahías de Huatulco** city deep-dive | Marina Santa Cruz → Bahía Maguey, 1.42 nm, nine-bays coastal hop. Route box canonical format. Atlas map slot **human-only**. |
| 18 | **WHAT ONE BOAT EARNS · HUATULCO** | `rn-66e2241ca732`: rev **$235,136**/boat-yr · margin **66%** · payback **3.88 yr** · fare **$20**. 6 flush OPEX lines (Energy $1,421 · Crew $25,200 · Marina+overhead $11,000 · Maintenance $10,000 · Insurance $15,000 · Charging berth $18,000). |

All econ numbers bound from `generated-deck-economics.json` — never hand-typed. MID scenario. N30 market composites (`holbox_city_n30`, `huatulco_city_n30`) are `needs_sourcing` — source market-specific approved imagery, register in `ASSET-REGISTRY.json`, no Atlas-generated images.

### C. Close-out
- Run `deck-studio/qa/partner_copy_lint.py` and `scripts/audit_partner_copy.py` as **blocking** gates.
- Pull full live inventory; sync `slide-manifest.json` (slides 15–18) with real object IDs; set `slide_count` 18.
- Return a QA receipt: deck ID, slide count, per-slide econ source-map, image provenance ledger, copy-lint result, no-op replay.

## Guardrails
- Holbox is a single-crossing island; keep it in the **backup**, not the main marquee.
- Do not touch slides 1–2, 4–9, 11–14 except the market-overview counts on slide 3.
- Fail closed: Puerto Vallarta and Los Cabos stay display (economics `null`); do not borrow another route's numbers.
