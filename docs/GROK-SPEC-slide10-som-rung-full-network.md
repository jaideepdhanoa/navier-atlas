# GROK SPEC — Slide 10 ladder: SOM rung shows full-network SOM (floor × greenfield)

**Owner:** Grok (deterministic builder + model-to-deck sealing lane)
**Author:** Tasklet (handoff)
**Decision by:** Jaideep, 2026-06-24
**Scope:** The **slide-10 TAM ladder** SOM rung, across partner decks. Propagate to **builder scripts**,
**source JSONs**, and the **Atlas proposal page**.
**Companion:** `docs/GROK-SPEC-ow-greenfield-captive-rescope.md` (greenfield 4.9→3.0, journey 3.0→5.0)
and `docs/GROK-SPEC-data-driven-capture.md` (capture % rendered from data).

---

## 1. Decision

On the **slide-10 TAM ladder**, the **SOM rung should display the full-network SOM**, i.e. the floor
**after** greenfield is applied — not the pre-greenfield floor. This makes the ladder a clean,
sequential build-up:

```
SOM (full network, today, +greenfield)
  ×  induced demand        →  SAM (full network, mature)
  ÷  capture (1/capture)   →  TAM (whole sea-transfer market)
  ×  whole-journey multiple→  Journey GMV
```

**Definition (read both factors from the model engine — do not hand-type):**
```
SOM_rung_slide10 = SOM_floor (pool × capture) × greenfield_factor
```

## 2. What changes vs. what does NOT

**Changes (Grok seals these):**
- **Slide-10 ladder SOM rung value** → full-network SOM (`floor × greenfield`).
- Builder logic that emits the slide-10 ladder, so the SOM rung binds to the full-network value rather
  than the floor value.
- The **slide-10 ladder** values in `deck-economics-values-*.json` (`slide10_tam.rungs[]`) and the econ
  binding, plus the **Atlas proposal page** ladder.

**Does NOT change (leave alone):**
- **Slide-3 floor KPI cards stay at the floor value** (e.g. OW `$8M floor`, "today's trips, ~capture").
  Slide 3 is the "what's real today" proof; the floor framing there is intentional. **Only the
  slide-10 ladder rung moves.** Do not "fix" slide 3 to match slide 10 — they are deliberately
  different views (floor proof vs. network build-up).
- SOM floor, capture, induced demand, greenfield factor, journey multiple — **the model parameters are
  unchanged by this spec.** This only changes **which** SOM figure the slide-10 rung *displays*.
- Live decks are not rebuilt/full-replaced. Apply the single rung value via targeted Slides API edit
  (or, if Jaideep already edited the live rung, just bring JSON/builder/proposal page to parity).

## 3. Labeling

- Keep the **`SOM` acronym visible** as the rung label (SOM/SAM/TAM/GMV stay per standing rule).
- Plain-English descriptor alongside it, e.g. *"SOM · Today — Navier fares across the full network,
  today, at ~46% capture."* Keep partner-facing copy plain English; the data-driven-capture spec
  renders the `~XX%` from the model (no hard-coded literal).
- Internal annotation framing (Jaideep's words): **"SOM full network (~XX% capture, today,
  +greenfield)"** — replaces the old internal **"SOM floor — Navier transport rev/yr (PUBLISHED)"**
  framing on the slide-10 rung.

## 4. Ocean Whisperer — worked example (confirmed target)

Using OW with the companion spec applied (greenfield **3.0**, journey **5.0**, capture **45.55% → ~46%**,
pool **$16,964,015**, induced **1.8**):

| Rung | Old display | New display | Build-up step |
|---|---|---|---|
| **SOM** (full network, today, +greenfield) | $8M (floor) | **$23M** | `floor $7.7M × 3.0 greenfield` |
| **SAM** (full network, mature) | $68M | **$42M** | `× 1.8 induced demand` |
| **TAM** (whole sea-transfer market) | $150M | **$92M** | `÷ capture (×2.2)` |
| **Journey GMV** (food, stays, experiences) | $449M | **$458M** | `× 5.0 whole-journey` |

Exact (mid): SOM `23,181,326` · SAM `41,726,387` · TAM `91,605,681` · GMV `458,028,405`.
Slide-3 OW floor cards remain `$8M`.

## 5. Other decks (Bolt, Grab Thailand, Minor)

This is a builder-level rule, so it applies to every partner deck's slide-10 ladder. For each deck,
Grok computes `SOM_rung = floor × greenfield_factor` **from that deck's own model engine** (each has its
own capture and greenfield). Record the per-deck before→after SOM rung in the sealing receipt. Do not
hand-type; if a deck is missing a greenfield factor in the model, **fall back to the floor and flag it**
(null beats confidently-wrong) rather than guessing a multiplier.

## 6. Files to update (per deck)

- Builder script slide-10 ladder emit logic (bind SOM rung to full-network value).
- `deck-studio/decks/<partner>/deck-economics-values-*.json` → `slide10_tam.rungs[]` SOM value.
- `deck-studio/decks/<partner>/economics-binding.json` → slide-10 SOM object value.
- `deck-studio/decks/<partner>/deck.editplan.json` → rendered slide-10 SOM (clean copy + value together;
  note the OW editplan is separately flagged on PR #101 for jargon — clean both at once).
- Atlas proposal page slide-10 ladder bindings.

## 7. Acceptance

1. Slide-10 SOM rung = `floor × greenfield` everywhere (proposal page, source JSONs, live deck).
2. OW slide-10 ladder reads **SOM $23M · SAM $42M · TAM $92M · GMV $458M**; build-up = ×1.8 → ÷capture →
   ×5.0; OW slide-3 floor card still reads **$8M**.
3. SOM acronym label retained with a plain-English descriptor; capture % rendered from data, not a
   literal; no internal taxonomy ("floor / transport rev/yr / PUBLISHED") leaks into partner-facing copy.
4. Live decks not rebuilt/full-replaced; single rung value applied via targeted Slides API edit.
5. Cascade recorded in the transparent sheet + master tracker per the partner-model-cascade flow.
