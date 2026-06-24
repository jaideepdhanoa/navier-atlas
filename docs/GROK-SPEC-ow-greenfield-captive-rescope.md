# GROK SPEC — Ocean Whisperer: greenfield 4.9 → 3.0 + journey multiple 3.0 → 5.0 (captive partner)

**Owner:** Grok (deterministic model-to-deck sealing lane)
**Author:** Tasklet (handoff)
**Decision by:** Jaideep, 2026-06-24
**Scope:** Ocean Whisperer only. Propagate to the **Atlas proposal page** and the **underlying source JSONs**.
**Status:** approved decision — Jaideep has already updated the model + the live slides. Grok seals the rest.

---

## 1. Decision

Two OW model parameters change:
- Greenfield-corridor width factor: **4.9× → 3.0×**
- Whole-journey GMV multiple: **3.0× → 5.0×**

**Why:** the 4.9× factor is derived from a **Grab national super-app census** (sourced vs greenfield
corridor counts). OW is a **captive single-island resort mesh** (Curaçao + sister-island lanes), not a
national network — it does not have ~4.9× latent greenfield corridors. 3.0× is the captive-appropriate
width: real expansion is *more resorts / more lanes on Curaçao + sister islands*, not national greenfield.

The width factor is applied **exactly once** in the ladder (see §3). This change does **not** alter
that structure — it only changes the value of the multiplier.

---

## 2. What changes vs. what does NOT

**Changes (Grok seals these):**
- OW greenfield factor `4.9 → 3.0` in the OW model parameter block, and everything downstream that the
  model recomputes from it: SAM and the marine-mobility TAM rung.
- OW whole-journey GMV multiple `3.0 → 5.0`, which recomputes the journey-GMV rung.
- The **Atlas proposal page** numbers for OW.
- The **underlying source JSONs** for OW (economics values sidecar, economics binding, partner JSON).

**Does NOT change (leave alone):**
- **SOM stays $7.7M** — the SOM floor is *before* greenfield (sourced corridors, today), so it is
  unaffected by the width factor.
- **SAM and TAM** depend only on greenfield (not the journey multiple), so they move with gf=3.0 only.
- **Capture rate stays as the model has it (45.55%).** The separate "OW should be 55% captive-style"
  item is **NOT** part of this change — do not fold it in. (Still an open reconciliation item; if/when
  it lands it shifts SOM and everything above it again, as a distinct decision.)
- **Induced demand (1.8×) is unchanged.**
- **The live OW slides** — Jaideep already edited these. Per standing rule, do **not** rebuild or
  full-replace the live deck. Bring the *source/JSONs* into parity with the already-correct live slides.

---

## 3. The ladder, before vs after (mid case — for parity verification)

Pool `M_today_transport_spend_yr` = **$16,964,015**; capture **0.4555**; induced **1.8**.
OLD params: gf **4.9**, journey mult **3.0**. NEW params: gf **3.0**, journey mult **5.0**.

| Rung | Formula | OLD (gf 4.9, jm 3.0) | NEW (gf 3.0, jm 5.0) |
|---|---|---|---|
| **SOM** — Navier fare, sourced lanes, today | `pool × capture` | **$7.7M** | **$7.7M** (unchanged) |
| **SAM** — Navier fare, full network, mature | `SOM × gf × induced` | $68.2M | **$41.7M** |
| **TAM** — whole sea-transfer market, full network | `pool × gf × induced` | $149.6M | **$91.6M** |
| **Journey GMV** — whole island journey | `TAM × jm` | $448.9M | **$458.0M** |

Exact NEW values to seal (mid): SOM `7,727,109` · SAM `41,726,388` · TAM `91,605,681` · GMV `458,028,405`.

Note: GMV lands near its old value (`$458.0M` vs `$448.9M`) because the smaller TAM (gf 3.0) is offset
by the larger journey multiple (5.0). SAM and TAM, which the journey multiple does not touch, drop as
shown.

**Greenfield is applied once.** (For the record: the old ladder was *not* double-counting 4.9 — the
SOM→TAM jump of ~19× was `(1/capture 2.2) × (gf 4.9) × (induced 1.8)`. With gf=3.0 the jump becomes
`2.2 × 3.0 × 1.8 ≈ 11.9×`.)

---

## 4. Band note (needs Grok/model handling, not a guess)

The model stores greenfield as a low/mid/high band: previously `{low 3.44, mid 4.9, high 6.36}`.
This decision sets **mid = 3.0**. Grok should rescope the low/high band consistently for the captive
partner (e.g. scale the band by `3.0/4.9`, or adopt a captive band) so `low ≤ mid ≤ high` holds — do
**not** leave `{3.44, 3.0, 6.36}` where mid falls below low. The displayed ladder uses **mid**, so the
public numbers in §3 are the mid case regardless of how the band is set.

---

## 5. Files to update (OW)

Read the model output as source of truth; do not hand-type rung values into prose.

- `finance/recal/growth-ocean-whisperer.json` — `parameters_used.greenfield_corridor_factor` (→3.0) and
  the whole-journey GMV multiple (→5.0), plus the recomputed `grounded` / `estimated_total` rung blocks.
- `finance/recal/agg-ocean-whisperer.json` — recomputed aggregates.
- `deck-studio/decks/ocean-whisperer/deck-economics-values-*.json` — `slide10_tam.rungs[].value`,
  `slide3_kpi` cards.
- `deck-studio/decks/ocean-whisperer/deck.editplan.json` — rendered values (note: this editplan is
  separately flagged on PR #101 as still carrying jargon; clean copy + values together when sealing).
- `partner-pitch/partners/caribbean.json` / OW partner record — any surfaced SAM/TAM/GMV.
- Atlas proposal page bindings for OW.

---

## 6. Acceptance

1. OW greenfield factor reads **3.0** (mid) everywhere; band satisfies `low ≤ 3.0 ≤ high`.
2. OW ladder on the proposal page and in all source JSONs matches §3 mid values
   (SOM $7.7M · SAM $41.7M · TAM $91.6M · GMV $274.8M).
3. SOM is unchanged ($7.7M); capture unchanged (45.55%); induced + journey multiple unchanged.
4. Live OW slides are **not** rebuilt; source JSONs match the already-corrected live deck.
5. Cascade recorded in the transparent sheet + master tracker per the partner-model-cascade flow.
