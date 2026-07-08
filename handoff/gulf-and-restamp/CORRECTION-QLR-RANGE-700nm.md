# CORRECTION — Q-LR range ceiling is ~700 nm, not 180 nm

**Date:** 2026-07-06
**Raised by:** Jaideep
**Impact:** Reclassifies the lost-corridor set. Genuine restore **57 → 79**; correct drops **59 → 37**.

## The error
My corridor-loss classification used a **180 nm** ceiling for Quanta-LR and dropped everything above it as "out of range." That was wrong. **Quanta-LR range is ~700 nm.** The 180 nm cut wrongly benched 22 legitimate Q-LR corridors — including the entire Gulf trunk.

## Corrected classification (Q-LR ceiling = 700 nm)
| Bucket | Count | Disposition |
|---|---|---|
| N30 short-range (3–60 nm) | 35 | Restore |
| **Q-LR (60–700 nm)** | **44** | Restore if water-clean |
| Hygiene (<3 nm / self-ref) | 36 | Correct drop |
| **Beyond Q-LR range (>700 nm)** | **1** | Correct drop |
| **GENUINE RESTORE** | **79** | |
| **CORRECT DROPS** | **37** | |

## The only true out-of-range drop
- **Jakarta ↔ Penghu (Taiwan) — 1,936 nm.** Genuinely beyond Q-LR. Stays dropped.

## The 22 corridors wrongly benched by the 180 nm cut (now Q-LR restore candidates)
**Gulf trunk (aspirational Q-LR overlay — cross-border render policy applies):**
- Abu Dhabi ↔ Manama (242) · Dubai ↔ Manama (256) · RAK ↔ Manama (290)
- Abu Dhabi ↔ Doha (242) · Doha ↔ Dubai (195) · RAK ↔ Doha (240)
- Abu Dhabi ↔ Muscat (224) · Dubai ↔ Muscat (206) · RAK ↔ Muscat (195)

**Caribbean:** Cartagena ↔ Aruba (401) · San Blas ↔ Cartagena (203) · Samaná ↔ Turks & Caicos (214)
**Indonesia inter-island:** Banda ↔ Wakatobi (371) · Lombok ↔ Sumba (257) · Raja Ampat ↔ Banda (244) · Karimunjawa ↔ Jakarta (217) · Lombok ↔ Komodo (206)
**Med:** Amalfi ↔ Sardinia (224) · Split ↔ Venice (218) · Sardinia ↔ Nice (184)
**India:** Goa ↔ Mumbai (206)

## Caveats for Grok (still gate before minting)
1. **Water-clean geometry** — every Q-LR restore still needs the hand-waypoint / no-land-crossing check (Split↔Venice across the Adriatic, Gulf trunk offshore routing, etc.).
2. **Endpoint quality** — drop any junk/business-POI endpoints (as with the in-range bucket).
3. **Label/pair QA** — one entry labelled "Bangkok ↔ Koh Samui" carries pair `['koh-chang-thailand','koh-phangan-thailand']` (212 nm) — reconcile label vs. endpoints before minting.
4. **Caspian guardrail unaffected** — none of these are Caspian; Baku↔Aktau (~250 nm) stays un-minted per its own rule (enclosed-sea / N30 policy), independent of Q-LR range.

## Net
Restore lists in `GROK-SPEC-corridor-restore-JUL2-2026-07-06.md` expand accordingly. Full reclassified register: `handoff/LOST-CORRIDORS-RECLASSIFIED-700nm.json`.
