# GROK SPEC — Make the capture-% in deck captions data-driven

**Owner:** Grok (deterministic model-to-deck generation lane)
**Author:** Tasklet (handoff)
**Scope:** `deck-studio/builders/*` + per-market economics data files. Bolt, Grab Thailand, Minor Hotels, Ocean Whisperer.
**Status:** spec / not yet implemented

---

## 1. Problem

On the SOM/SAM/TAM/GMV ladder (slide 10) and the network-KPI ladder (slide 3), the **dollar
values are calculated** from the model (each market's economics file), but the **capture
percentage inside the caption sentence is a hard-coded string literal**.

Example, today, in `deck-studio/builders/deck_bolt_wave2.py`:

```python
SLIDE10_TAM_CAPTIONS = {
    "som_caption": "SOM · Today — Navier fares on Bolt's network, serving 10% of current trips",
    "sam_caption": "SAM · Near term — faster, quieter boats grow the market; 25% capture at maturity",
    ...
}
```

The model already *uses* a capture assumption to compute the SOM dollar floor
(`provenance_note: "grounded floor = demand x fare x ~10% capture"`), but that number is **not
stored as a field and not read by the caption**. Result: if a market's true capture is 8% or 15%,
the **dollar figure updates but the sentence still says "10%"** — silent drift between prose and math.

**Goal:** the capture % shown in caption text must be **read from the model**, per market, so the
words always match the numbers. No hard-coded percentages in caption literals.

---

## 2. Current architecture (two patterns — both must be migrated)

### Pattern A — sidecar captions (Bolt, Minor Hotels, Ocean Whisperer)
- **Values** come from `deck-studio/decks/<partner>/deck-economics-values-<partner>.json`
  → `slide10_tam.rungs[].value` and `slide3_kpi.network_cards[].value`.
- **Captions** are fixed literals in the builder's `SLIDE10_TAM_CAPTIONS` dict and in the
  sidecar's `network_cards[].meaning`. Rendered by `slide10_tam_text_map()` /
  `slide3_kpi_text_map()`.

### Pattern B — inline captions (Grab Thailand)
- `deck-studio/builders/deck_grab_thailand.py` → `slide10_tam_map()` and `slide3_kpi_map()`
  build captions as inline string literals (e.g. `"SOM — Navier fare … 10% capture"`), values
  pulled live from `finance/recal/growth-*.json` + the KPI file.

In **both** patterns the object-id → field mapping is stable (e.g. `som_value`/`som_caption`
bound to `g3eec5122801_0_570` / `_571`). We change **what fills `*_caption`**, not the geometry.

---

## 3. Required change

### 3.1 Add a capture field to the data layer (model engine output)
Every market's economics data must carry the capture rates it already implies, as **numbers**, not prose:

```json
"capture": {
  "som_today_pct": 10,          // integer percent used for the SOM grounded floor
  "sam_mature_pct": 25,         // integer percent used for the SAM maturity rung; null if "contested"/not modeled
  "basis": "modeled",           // provenance tag; e.g. "modeled" | "captive_55" | "contested"
  "source": "finance/recal/agg-<partner>.json"
}
```

- Place it where the rest of the ladder lives:
  - **Pattern A:** add `capture` under `slide10_tam` in `deck-economics-values-<partner>.json`.
  - **Pattern B:** emit `capture` into the KPI/growth artifact the builder already reads.
- **The number must be the same one the model used to compute the SOM/SAM dollar figure** — read it
  from the engine, do not re-type it. If a market does not model a maturity capture (Grab's
  "contested"), set `sam_mature_pct: null`.

### 3.2 Render captions from a template, not a literal
Replace the per-deck caption literals with a shared template that interpolates the field. Preserve
the **exact plain-English format Tasklet shipped** (`LABEL · Phase — descriptor`):

```python
def som_caption(partner_network: str, cap: dict) -> str:
    pct = cap.get("som_today_pct")
    if pct is None:                      # null beats confidently-wrong
        return f"SOM · Today — Navier fares on {partner_network}"
    return f"SOM · Today — Navier fares on {partner_network}, serving {pct}% of current trips"

def sam_caption(cap: dict) -> str:
    pct = cap.get("sam_mature_pct")
    if pct is None:
        return "SAM · Near term — faster, quieter boats grow the market"
    return f"SAM · Near term — faster, quieter boats grow the market ({pct}% at maturity)"
```

- `TAM` and `GMV` captions stay as-is (no capture % in them).
- Keep `SOM/SAM/TAM/GMV` as the visible label (partner-approved). Keep all descriptors plain English.
- **null beats confidently-wrong:** if the field is missing/null, drop the percentage clause entirely
  rather than defaulting to 10%.

### 3.3 Also fix the slide-3 KPI card + provenance note
Same rule applies to:
- `slide3_kpi.network_cards[]` SOM-floor card `meaning` (currently `"… ~10% capture"`).
- `_meta.provenance_note` (`"… x ~10% capture"`).

These should interpolate `som_today_pct` too, so a single field drives every place the number appears.

---

## 4. Guardrails (do not regress these)

- **Plain-English only on slides.** No internal taxonomy in caption text (mesh, sealed, captive,
  induced, `% capture` as a bare internal phrase, Bucket-X, anchor corridor, etc.). The
  `deck-studio/qa/partner_copy_lint.py` gate already enforces this and is wired into `deck-studio apply`
  (hard, pre-seal) and `deck-studio qa`. `SOM/SAM/TAM/GMV` are allow-listed labels.
- After migration, **add a lint rule** that flags any hard-coded `NN% capture` / `NN% of current
  trips` *literal* in builder/caption source, so the only legal source for the number is the data
  field. (Tasklet can add this rule on request once the field name is final.)
- **Don't rebuild the four live decks from this change.** Tasklet has already direct-edited the live
  slides to the correct copy; this spec makes the *source/builders* consistent so a **future**
  regeneration stays correct. Per standing instruction: corrected data files first, no forced Grok
  rebuild of already-edited live decks.
- **ID-match only / no geometry change.** Object-id→field bindings are unchanged.

---

## 5. Acceptance

1. Each of the 4 markets has a numeric `capture` block sourced from the model engine.
2. No builder or caption file contains a hard-coded capture percentage literal (grep clean for
   `\d+% capture` and `\d+% of current` in `deck-studio/builders/` and the caption literals).
3. Regenerating each deck's editplan reproduces the current live wording **when** the field equals
   today's value (10% / 25%), and changes the sentence automatically when the field changes.
4. A market with `sam_mature_pct: null` renders the SAM line with **no** percentage clause (Grab).
5. `partner_copy_lint.py --all` stays clean.

---

## 6. Reference (current values, for parity check)

| Deck | SOM today | SAM maturity | Notes |
|---|---|---|---|
| Bolt | 10% | 25% | sidecar pattern |
| Grab Thailand | 10% | null ("contested") | inline pattern |
| Minor Hotels | 10% | (confirm) | sidecar pattern; hospitality $1M/vessel basis |
| Ocean Whisperer | confirm (live shows ~46% on one row; OW capture basis is **55%**, captive-style not FP-flat) | confirm | OW basis needs reconciliation — see note |

> **OW open item (separate from this spec):** an OW economics row shows ~46% capture; the agreed OW
> basis is **55%** (captive-style, not FP-flat). That's an economics correction, not a templating
> change — reconcile the field value when wiring `capture.som_today_pct` for OW.
