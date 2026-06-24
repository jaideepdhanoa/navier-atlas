# GROK HANDOFF — Bolt Bug C: greenfield census rebase + reseal (end-to-end)

**Owner: Grok (cascade + reseal lane), end-to-end.** Jaideep directed the whole of Bug C to Grok on
2026-06-25. This is a corrected-economics reseal — **no new geography / no new BPs**, so no BP zip is
required; it's a re-cascade of Bolt's growth ladder + a partner-surface reseal.

## Mandate
Bolt's `growth_case` network rung rests on a **borrowed peer census**, not Bolt's own:
- `partners/bolt.json → growth_case._provenance`: `greenfield_mode: "census"`,
  `greenfield_corridors: 341`, `sourced_corridors: 35`.
- `som_network` ($507M) ≈ **4.9× the grounded floor** ($104M) — i.e. **Grab's census width**. This is
  the golden-rule-#3 trap (partner-model-cascade): a non-Grab partner with no census of its own
  inheriting Grab's width and spuriously hitting "Grab parity." Confidently-wrong.

## Required fix (deterministic)
1. **Re-cascade** Bolt's growth ladder with the **labelled global template band (3.44 / 4.9 / 6.36)** —
   NOT a pointer at any peer census file:
   `growth.py --partner bolt --agg recal/agg-bolt.json` (default labelled-template upside).
   - If you'd rather not surface a template band at all, the acceptable fallback is `--greenfield off`
     (grounded floor only). Pick template-band per the standing directive unless it can't be labelled
     honestly.
2. **Relabel the network rung basis** so it reads as a **template-width assumption pending a
   Bolt-specific census**, not a measured "whole mapped network" count. The `greenfield_mode` must no
   longer point at a peer census file.
3. **Floor is invariant.** The grounded SOM floor ($104M) is greenfield-independent and must NOT move.
   Use it as the sanity check.
4. **Cascade both engines** (golden rule #7): `splice_growth_into_partner.py` → transparent sheet →
   master tracker must all tell the same story.
5. **Reseal the front end** so the live map/partner page stops showing the borrowed-census provenance
   (`data-clean/partners/bolt.json` must no longer carry the 341/Grab-width census provenance). Rebuild
   the route-keyed econ sidecar against the new gold.

## Acceptance
- `greenfield_mode` no longer references a peer census file; `_provenance` reads as a labelled template
  band (or grounded-only).
- Network / SAM / TAM rungs carry an honest template-width label (no "Grab parity" artifact).
- Floor unchanged at ~$104M across deck + transparent sheet + master tracker (all three agree).
- Live partner surface resealed; no stale census provenance in `data-clean/partners/bolt.json`.
- QA counts: before→after network/SAM/TAM rung values + the floor-unchanged proof.

## Do NOT rebuild from stale source
Bug B (Careem `registry_key` → `bolt-uae`) and the **East Africa parity narrative** are already fixed in
`partners/bolt.json` (PR #103). Read the corrected partner JSON as the input; do not regenerate it from a
pre-#103 source.

## Related (separate, NOT in this handoff)
- **Bug A** ($1.54M rendering as "$2M"): front-end/formatter one-decimal-under-$10M fix. Specced in
  `handoff/GROK-SPEC-bolt-data-bugs.md`; can ride the same reseal but is independent of the cascade.

Refs: `handoff/GROK-SPEC-bolt-data-bugs.md` (PR #103); partner-model-cascade golden rule #3;
grok-seal-handoff two-worlds rule.
