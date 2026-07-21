# Phase 3 economics cascade — MX/EG expansion (2026-07-21)

Tasklet → Grok handoff. Path 2 (accurate TAM) per Jaideep 2026-07-20: source real demand for the
owed markets, cascade through the model, produce a comprehensive DiDi Mexico TAM ladder.

## What changed in canonical source (`finance/model/corridors.json`)
Two source-grounded corridors added (from the Grok seal #315 gold geometry):

| route_id | market | corridor | dist (sealed) | demand (gross one-way/yr) | fare | source |
|---|---|---|---|---|---|---|
| `rn-8e76868a5b01` | mexico-caribbean | Chiquilá ↔ Isla Holbox | 8.35 nm | 1,000,000 | $12 | QRoo state tourism (363k tourists Jan–Aug 2024 → ~500k arrivals ×2, captive-access island) |
| `rn-66e2241ca732` | mexico-pacific | Santa Cruz Marina ↔ Nine Bays | 1.42 nm | 360,000 | $20 | SEMAR port master plan Huatulco 2022–2027 (~180k tourists/yr ×2) |

Both fares Jaideep-confirmed (Holbox $12 seal-confirmed; Huatulco $20 approved 2026-07-20).
Puerto Vallarta and Marsa Alam/Wadi El Gemal were researched but **fail closed** (no published
passenger volume) — they remain display-only. Egypt gains nothing groundable → **inDrive/DiDi
Egypt ladders unchanged**.

## Cascade run (Tasklet, verified)
- Country-reference fail-closed gate: **PASS** (28 active corridors; only unrelated Argentina held).
- `aggregate.py --partner didi` → `finance/recal/agg-didi.json` refreshed. Grounded floor
  **$106.14M → $109.51M** (+$3.37M, exactly the two new corridors).
- DiDi Mexico ladder rebuilt via Mexico-only rollup (leaking `--markets` flag avoided) →
  `didi-mexico-growth-2026-07-21.json`.
- Transparent sheet (2nd engine) agrees on both corridors (dist/fare/tier match) — golden rule #7 ✓.

## New DiDi Mexico TAM ladder (MID) — uniform +18.6% over the 2026-07-20 confirmed ladder
| Rung | Confirmed | New MID |
|---|---|---|
| SOM Full Mapped Network | $138.0M | **$163.6M** |
| SAM (Navier transport rev) | $631.7M | **$749.7M** |
| Marine mobility TAM | $2.53B | **$3.00B** |
| TAM journey GMV | $7.58B | **$9.00B** |
| Partner platform take (18%) | $341.1M | **$404.9M** |
| grounded SOM floor (published) | — | $30.0M |

Two drivers: (1) DiDi census refresh during the seal widened the mapped network ($138M→$153.8M,
+11.4%); (2) Holbox+Huatulco demand ($153.8M→$163.6M, +6.4%). Jaideep approved both.

## Per-city MID unit economics (for Phase 4 deck econ slides)
- **Huatulco** (Santa Cruz ↔ Nine Bays, $20, 1.42nm): $235,136/boat-yr · 65.7% margin · 3.88 yr payback · 3 boats. **Strong.**
- **Holbox** (Chiquilá ↔ Holbox, $12, 8.35nm): $122,232/boat-yr · 29.3% margin · 16.76 yr payback · 9 boats. **Weak per-boat.**

## ⚠ QA flag for Grok — Holbox sealed distance
The sealed Holbox distance is **8.35 nm** (`rn-8e76868a5b01`), but the real Chiquilá↔Holbox ferry
crossing is ~5 nm (~9 km, ~25 min). The 8.35 nm value roughly doubles per-boat opex and is the main
driver of Holbox's weak 16.76-yr payback. **Please confirm whether the 8.35 nm geometry is correct
(e.g. a channel routed around shallows) or a seal artifact.** If it should be ~5 nm, re-seal and
Tasklet will re-cascade Holbox. The TAM ladder (pool-based) is unaffected either way.

## Grok next steps (seal lane)
1. Rebuild the economics sidecar (`economics_by_route_id.json`) into the gold zip from the refreshed
   `finance/recal/agg-didi.json` — new entries for `rn-8e76868a5b01` and `rn-66e2241ca732`.
2. Confirm/repair the Holbox sealed distance per the QA flag above.
3. Front end: the two new markets carry economics now; ensure `economics_url` deep-links resolve.

## Tasklet next (after merge + sidecar)
- Update the "Navier × DiDi Mexico" Drive sheet MID in place (done in parallel with this PR).
- Phase 4: DiDi Mexico deck — TAM slide to new MID ladder; add Holbox + Huatulco city deep-dive +
  econ slides (backup section per playbook). Held until Grok sidecar returns.
