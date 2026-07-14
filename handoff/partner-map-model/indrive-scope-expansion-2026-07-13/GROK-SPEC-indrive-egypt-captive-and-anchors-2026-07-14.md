# GROK SPEC — inDrive Egypt: captive capture + dual unit-economics anchor (2026-07-14)

Follow-on to PR #265 (merged). Two source-side changes approved by Jaideep 2026-07-14. Deterministic
cascade + Slides seal are Grok's lane.

## 1. Captive capture treatment (LB-254)

Egypt's two promoted Red Sea routes are **boat-only destinations** (Giftun Island; Ras Mohammed reef),
so the marine visitor pool is the addressable base. Treat as **captive at ~0.90 floor capture**, not the
prior contested 0.10.

Source changes already made in `finance/recal/corridors-indrive.json` (`markets.indrive-egypt`):
- `capture_rate: 0.90`, `captive: true`, `_capture_basis` added.
- Each promoted corridor (`rn-b06f6971ed47`, `rn-c16a1627130f`) tagged `captive: true`.

Cascade must honor LB-254 exactly:
- `aggregate.py` emits `transport_spend_pool_yr` (Σ demand×fare) and `effective_capture` (= floor/pool ≈ 0.90).
- `growth.py` anchors `M_today = transport_spend_pool_yr`. **Do NOT recover the pool by `floor / 0.10`** — that
  would inflate every rung ~9×.
- Clamp mature capture ≥ floor capture (captive band + thin 0.95 lock-up ceiling). The contested 0.15/0.25/0.40
  ramp is wrong-signed for captive.
- Verify all four surfaces (`growth.py`, `splice_growth_into_partner.py`, `growth_frontend_block.py`,
  `build_transparent_sheet.py`) carry captive capture — no hard-coded 0.10 leaks.
- **CAPEX unchanged:** inDrive is ride-hail; Egypt is non-US/EU → region CAPEX **$600K/vessel**. Do NOT apply the
  hospitality $1M tier. `captive` (capture) and `capex_tier` (CAPEX) are independent levers.

Indicative captive results for the cascade to reproduce (per-boat is fare-driven, capture-independent):

| Route | nm | fare | pax/boat/yr | rev/boat | opex/boat | EBITDA/boat | margin | payback | pool | captive floor (90%) | fleet |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `rn-b06f6971ed47` Giftun | 6.6 | $32 | 7,588 | $242,827 | $73,959 | $168,868 | 70% | 3.55 yr | $6,000,384 | $5,400,346 | ~22.2 |
| `rn-c16a1627130f` Ras Mohammed | 11.7 | $50 | 5,962 | $298,114 | $74,494 | $223,620 | 75% | 2.68 yr | $2,500,000 | $2,250,000 | ~7.5 |
| **Egypt market** | | | | | | | | | **$8,500,384** | **$7,650,346** | **~29.8** |

`effective_capture` ≈ 0.900. Per-boat OPEX 6-line (Egypt row): energy · crew $21,600 · marina+overhead $8,000 ·
maintenance $10,000 · insurance $15,000 · charging-berth $18,000.

**Sanity gate (LB-254):** captive journey-GMV TAM (~$8.5M) is far below Egypt's tourism economy — no inflation.
Engine replication validated against Rio `rn-1886629dbf0c` (opex $79,094 exact; payback 8.92 vs 8.91).

## 2. Dual unit-economics anchor (Jaideep to pick)

Jaideep asked for **both** Giftun and Ras Mohammed built as the single unit-economics slide so he can choose.
`deck-studio/decks/indrive-egypt/economics-binding.json` now carries `unit_econ_anchor_options` with
`selection: "pending_jaideep"` and full per-boat figures for both.

- Render the single unit-economics slide (new spine) in **two variants**, one per option, for Jaideep's choice.
- Each variant shows that one route's real per-boat economics. Do not blend or invent a composite figure.
- Preserve the new-spine order (cover → why-partner → market overview → one slide per city → one unit-economics
  slide → TAM → rollout/next steps). Reserve Atlas screenshot slots for Jaideep's insertion — no visible
  placeholder text/labels on any partner-facing slide.
- Partner copy stays plain English; must pass `scripts/audit_partner_copy.py`. `captive`/LB-254 are internal
  config words — never surface them on a slide.

## 3. Held / excluded (unchanged)
- Held (null): `rn-3d161664de08` Sahl Hasheesh, `rn-173d32792c07` Soma Bay, `rn-285fc16b29dc` Sharks Bay.
- Cairo excluded (Nile/river). Alexandria candidate/null — see the separate Alexandria geography spec.

## 4. Corroboration logged (no economics change)
"Boxi Marine" markets itself as Egypt's first public water-taxi with scheduled €25 departures (09:00/11:00/13:00)
to **Hurghada** islands incl. Orange Bay/Giftun (boximarine.com, accessed 2026-07-14). This independently
corroborates the Hurghada→Giftun/Orange Bay corridor as a real, operating marine run. It is **not** a scheduled-
tariff source and does not change the promoted labeled-pool demand or premium fare.
