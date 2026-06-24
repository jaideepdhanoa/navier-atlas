# Ocean Whisperer — ABC scale-vision re-seal (silent-drop fix)

**Owner of the fix:** Grok (geometry seal lane). Tasklet supplies this spec + the source legs already exist.
**Date:** 2026-06-24
**Trigger:** Buyer-facing map renders **Curaçao only**; the ABC scale-vision does not appear.

---

## 1. What's wrong (root cause = silent drop at seal, NOT a positioning change)

The locked two-proposal division stands and is unchanged:
- `ocean-whisperer.json` = Curaçao captive **core** + standardization narrative; ABC/wider-Caribbean appears **only as the scale vision** (roadmap-amber). $1M hospitality, 55% captive.
- `caribbean.json` ("Caribbean × Navier") = the generic full-ABC network ($900K commercial).
- Curaçao geometry is **sealed once**; both proposals scope to it. **Do NOT duplicate corridors or convert OW into the network proposal.**

Tasklet's source (`ocean-whisperer-corridors.json`) correctly specifies **2 roadmap-network-amber legs**:
1. **Curaçao (Spanish Water) → Bonaire (Kralendijk town pier)** — ~38 nm, Pioneer II, `render: roadmap-amber-dashed`, `tier: roadmap`.
2. **Curaçao (Spanish Water) → Aruba (Oranjestad / Renaissance Marina)** — ~70 nm, Quanta-LR, `render: roadmap-amber-dashed`, `tier: roadmap`.

But the **sealed `ocean-whisperer.json`** dropped them:
- Only **4 journeys**; the **Aruba roadmap leg is entirely missing**.
- The Bonaire leg is present (`rn-0f8e77cfef46`) but listed as a plain ~33.3 nm journey, **not** flagged/rendered as a roadmap-amber network leg.
- All **3 phases** carry `cities: ["curacao-curacao"]`; Phase 3 ("standardized multi-market network") never lists `aruba-aruba` / `bonaire-bonaire`.
- `end_state.addressable_market_count: 1`, `end_state_cities: ["curacao-curacao"]`.

This breaches the seal-manifest (`roadmap_amber: 2`) and the **"0 silent drops"** acceptance gate.

## 2. The fix Grok should seal (additive, scoped-view only)

1. **Seal both roadmap-amber legs** onto the shared Curaçao geometry and bind them to `ocean-whisperer` as the **scope-(a) captive view**:
   - Bonaire leg: surface as `tier: roadmap`, `render: roadmap-amber-dashed` (not a plain grounded journey). Use the sourced node ids `curacao-curacao__spanish-water-jan-thiel → bonaire-bonaire__kralendijk-town-pier`.
   - Aruba leg: **add** it — `curacao-curacao__spanish-water-jan-thiel → aruba-aruba__oranjestad-renaissance-marina`, Quanta-LR, `roadmap-amber-dashed`. Never grounded on a 70 nm boat.
2. **Phase 3** (`cities`) → add `bonaire-bonaire` and `aruba-aruba` as **roadmap** markets (route_scope cross-border for the inter-island legs). Phases 1–2 stay Curaçao-only captive core.
3. **end_state** → `addressable_market_count: 3`, `end_state_cities: ["curacao-curacao","bonaire-bonaire","aruba-aruba"]`, `addressable_regions: ["caribbean"]` (unchanged). Keep the steady-state framing honest: Curaçao captive core + ABC roadmap.
4. **Economics (Grok cascade, not hand-typed):** Curaçao captive core stays the **grounded SOM floor at 0.55 capture**; the 2 roadmap-amber legs are **roadmap-labeled, NOT added to the grounded SOM floor**. Ladder still rises per the locked `_cascade_inputs` (SOM < SAM < TAM; not FP-flat).

## 3. Acceptance (mirror the seal-manifest gate)
- ABC scale-vision **renders**: Aruba + Bonaire roadmap legs visible as amber-dashed on the OW map.
- Curaçao remains the captive anchor; OW is **not** duplicated into `caribbean.json`; no corridor double-count.
- 0 silent drops: every sourced corridor either sealed or in a drop-ledger with a reason.
- Ladder rises (captive-but-rising), not flat-lined.

## 4. Logo asset (Tasklet deliverable — done)
Per fine-tuning brief §9, the Ocean Whisperer logo is delivered for deck use (where supported):
- Stable URL: `https://drive.google.com/uc?export=download&id=1v8v6PYYwX1-o9rH071WzVrT7nEns4cA6`
- Transparent PNG, 305×154, gold wings + wordmark. Use on cover/title where the deck-builder supports a partner logo; else null (do not guess).
