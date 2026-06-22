# Autonomous Deck Build Contract (Grok operator)

**Purpose:** make Grok the independent deterministic operator for the full deck loop —
the way it already runs the financial/economics loops — so Tasklet is no longer in the
hand-build path. Tasklet's residual job shrinks to: guardrails, scope corrections,
and **exact-bind evidence** (sealed Atlas `city_id` ↔ live Slides `object_id`). Everything
deterministic below is **Grok-owned**.

This contract sits above `GROK-RUNBOOK.md`, `LIVE-DECK-RULES.md`, `IMAGE-RULES.md`,
and `assets/IMAGE-ROLE-CONTRACT.md`. Where any of those conflict, the safety rules
(no PPTX round-trip, no full-deck replace, exact-bind only, null beats confidently-wrong,
human review for external sends) always win.

---

## 0. Division of labor (read this first)

| Work | Owner | Why |
|---|---|---|
| Pull economics from sheet / partner JSON / finance recal | **Grok** | pointers already in `content-source.json` |
| Generate market images, N30 composite, upload to Drive, record stable URL | **Grok** | deterministic + reproducible from saved inputs |
| Reuse already-covered market assets (e.g. UAE/Dubai) instead of regenerating | **Grok** | `ASSET-REGISTRY.json` is keyed by `atlas_city_id` |
| Build `deck.editplan.json` from inputs (not hand-authored) | **Grok** | derived from golden map + registry + economics |
| Generate the Grab golden-template-map (live object inventory) | **Grok** | `deck_studio pull --mode full` |
| Apply via Slides API, run QA gates, export render receipts | **Grok** | deterministic |
| Provide scope guardrails + corrections (e.g. Bolt ≠ Malaysia) | Tasklet | judgment / source-of-truth |
| Provide exact `city_id ↔ object_id` evidence when a bind is ambiguous | Tasklet | exactness gate |
| Approve external sends | Human | review gate |

If an input Grok needs is genuinely missing (no economics pointer, no city_id),
Grok holds the field **null** with a status, and does **not** improvise.

---

## 1. The independent loop (per deck)

```
[0] refresh golden map  ──► [1] resolve economics ──► [2] resolve images ──►
[3] build deck.editplan.json ──► [4] copy gold deck (drift gate) ──►
[5] apply editplan verbatim ──► [6] QA gates + render review ──► [7] receipts/commit
```

Gate: **no Slides write** until steps 0–3 produce a validated, non-empty plan.

### [0] Refresh the golden template map (Grok-owned, no Tasklet dependency)
The golden map is the reference object-ID surface Grok targets. **Grok generates it itself:**
```
python -m deck_studio pull --root deck-studio --deck grab --mode full --out deck-studio/decks/grab/golden-template-map.json
```
This yields slide-by-slide `object_id`s. Grok then annotates each object with its **role**
(`cover_hero`, `navier_logo`, `partner_logo`, `value_prop_bg`, `tam_bg`, `partner_roles_bg`,
`econ_market_bg`, plus text roles: `slide3_kpi_*`, `slide7_econ_*`, `slide10_tam_*`, `opex_line_1..6`)
using `assets/IMAGE-ROLE-CONTRACT.md` and the existing `ASSET-REGISTRY.json` `used_by[].target_object_id`
entries as seeds. Target deck object IDs come **only** from a full pull of *that* deck — never from
memory and never copied blindly from Grab.

### [1] Resolve economics (Grok pulls; never hand-typed)
Each deck's `content-source.json` already carries the pointers:
- `source_files[]` → partner pitch JSON, `data-clean` JSON, `finance/recal/agg-*.json`, `finance/recal/growth-*.json`
- `economics_url` → the deck's transparent Google Sheet (e.g. Bolt `1XkD0x-PfDyY34ZBy5jX2u1LqoibAd_xMiyO-Re2UWUk`)
- `economics_by_route_id`, `economics_table`, `model_link`

Grok reads those, then emits the styled numeric runs for:
- **slide 3** market-overview KPIs
- **slide 7** route economics
- **slide 10** TAM
- **OPEX** = exactly **6 flush-left lines**, read live per slide (OPEX field-ID family can split;
  read IDs from the live slide, do not assume Grab's IDs)

**Leak denylist (hard fail):** Grab-specific strings (`Marina Bay`, `Sentosa`, `$480,870`, Grab route IDs),
stale scope strings (`Malaysia`, `Mexico`, `Morocco` for Bolt), and any number with no source pointer.
`null` beats a confidently-wrong number.

### [2] Resolve images — **reuse first, generate second, publish, link**
For every role in `IMAGE-ROLE-CONTRACT.md`, resolve in this order:

1. **Reuse:** look up the market in `ASSET-REGISTRY.json` by sealed `atlas_city_id`.
   If a `checked_in` asset exists (with `drive_file_id` + `source_url`), **reuse it** — do not regenerate.
   This is how an already-covered market (e.g. **UAE / Dubai**, Singapore, Phuket) is shared across decks.
2. **Generate on miss:** if the role is unresolved, Grok generates the market-specific background
   (no Atlas imagery), runs the deterministic N30 composite
   (`builders/images/n30_composite.py`), and saves source+vessel+mask+args for reproducibility.
3. **Publish:** upload the composite to the Navier Drive deck-assets folder, capture `drive_file_id`
   and a stable `source_url` (`https://drive.google.com/uc?export=download&id=<id>`).
4. **Record:** write the asset back into `ASSET-REGISTRY.json` (role, scope, `atlas_city_id`,
   `local_path`, `drive_file_id`, `source_url`, provenance, `used_by[]`), so the next deck reuses it.
5. **Bind:** map `asset_ref → target_object_id` from the deck's full pull.

Rules: **no embedded blobs, no `googleusercontent` temp links, no Atlas images.** Logos are the only
non-composite assets. Territory/no-logo covers (Caribbean, French Polynesia, Hong Kong) carry
`partner_logo: null` intentionally — never a guessed badge.

### [3] Build `deck.editplan.json` (Grok builds it — this replaces the empty CLI stub)
Inputs: golden map (step 0) · economics runs (step 1) · resolved image refs (step 2) ·
`content-source.json` · `slide-manifest.json` · partner logo ref.
Output: a `deck.editplan.json` validating against `schemas/edit-plan.schema.json` with:
- non-empty `operations[]`, each with a real `slide_object_id` + concrete `google_slides_request`
- style-preserving text edits (3-phase: delete → insert → re-apply Exo 2 / Poppins per run)
- correct cover `partner_logo` (or null for territory decks)
- image ops referencing stable `source_url`s only
- `safety` block all-true; `qa_gates[]` populated
- leak-denylist assertions embedded

The `deck_studio plan` CLI is currently a scaffold (emits `operations: []`). Until it generates real
ops, Grok authors the operations; the CLI's job is schema + safety validation (`apply` already refuses
unknown `slide_object_id`s and forbidden request keys).

### [4]–[7] Copy → apply → QA → receipts
Copy the gold/template deck (drift gate), `apply` the editplan **verbatim**, then run the 6 QA gates
(`object_id_check`, logo check, image-URL check, economics/source check, leak-denylist, render/thumbnail
review). Commit `golden-template-map.json`, `deck.editplan.json`, updated `ASSET-REGISTRY.json`, and the
QA receipt. External sends stay human-reviewed.

---

## 2. Pilot order

1. **Grab** = golden reference harness only (generate the golden map from it; do not re-pitch).
2. **Bolt** = first partner-ready build. **Scope: Europe/Gulf source baseline only** — Greece/Aegean
   (recommended beachhead), plus validated Croatia/Dalmatia, Italy, France/Côte d'Azur, UAE, and
   Saudi/Jeddah–Red Sea where supported. **No Malaysia, Mexico, or Morocco.** Exact-bind only.
3. Then the remaining banked decks per the queue, reusing market assets as they accumulate.

## 3. What still blocks a *clean-room* run (open, not yet done)

These are the honest gaps; none are Grok-capability gaps, they are missing inputs/contracts:
- **Partner logo bank** — `assets/logos/partners/` is empty (README only). Logos must be banked
  (path + Drive URL + provenance) before cover binds; territory decks stay null.
- **Per-deck economics-binding** — pointers exist in `content-source.json`; an explicit
  field→object_id binding per deck still has to be emitted during the per-deck build.
- **Golden map** — not yet generated; it is step [0] of the first real run.
- **Branch consolidation** — the `golden-template-map.json` / `LOGO-MANIFEST.json` /
  `CONSOLIDATED-DECK-GENERATION-QUEUE` / edit-plan contract Grok referenced from "PR #71/#72" are
  **not present in this canonical repo**. This branch (`asset-pack-grab`) is the real source of truth.
  Grok should operate from here, not from a local-only copy.
