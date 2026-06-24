# Bolt data-bug spec — rounding + greenfield census rebase

Source: Grok handback 2026-06-24, "Bolt data bugs (from audit)". Tasklet has shipped the two
in-lane data fixes (East Africa narrative parity + Careem registry-key leak); the two below
change **live economics / rendering** and are routed to the cascade + front-end (Grok) lane so
they don't ship silently.

---

## Bug A — floor rounding: $1.54M must not display as "$2M"

**Symptom:** a ~$1.54M grounded floor renders as "$2M". Rounding a grounded floor *up* overstates
the honest number we actually sell — an exactness violation (null/under beats confidently-over).

**Root cause (not in `partners/bolt.json`):** the top-level Bolt `growth_case` floor is $104M, so the
offending $1.54M is a *small-market / single-corridor* figure produced by the money formatter, not a
stored display string in the partner JSON. The formatter rounds sub-$10M values to whole millions.

**Fix:** in the money formatter (`finance/model/growth_frontend_block.py` display builder **and** the
Atlas front-end currency formatter — wherever `$XM` strings are minted), use **one decimal place for
values < $10M** (`$1.5M`, not `$2M`); keep whole-million/`$B` formatting at/above $10M. Never round a
floor up across a whole-million boundary. This corrects every small-market floor at once.

**Acceptance:** a $1.54M floor renders `$1.5M` on the partner page, the deck, and the transparent sheet
(all three engines agree, golden rule #7).

---

## Bug C — ladder rungs must rest on minted corridors, not the shared 341-route census

**Symptom (`partners/bolt.json` → `growth_case._provenance`):**
`greenfield_mode: "census"`, `greenfield_corridors: 341`, `sourced_corridors: 35`. The `som_network`
rung ($507M) is ~4.9× the grounded floor ($104M) — i.e. **Grab's census width**. Per
partner-model-cascade golden rule #3 this is the classic confidently-wrong trap: Bolt has **no census
of its own** and is inheriting a peer's census file, spuriously hitting "Grab parity."

**Fix (cascade lane — re-run, do not hand-edit numbers):**
1. Re-run `growth.py --partner bolt --agg ../recal/agg-bolt.json` with the **labelled global template
   band (3.44 / 4.9 / 6.36)** — NOT a pointer at any peer census file — OR `--greenfield off` for
   grounded-only if we'd rather not show a template band at all.
2. Relabel the network rung basis so it reads as a **template-width assumption pending a Bolt-specific
   census**, not a measured "whole mapped network" count.
3. The grounded **SOM floor ($104M) is greenfield-independent** and must not move (invariant check).
4. Cascade through `splice_growth_into_partner.py` → transparent sheet → master tracker (both cost
   engines must tell the same story, golden rule #7).
5. **Front-end reseal is Grok's lane** — after the cascade, hand the refreshed `agg-bolt.json` +
   partner JSON to the seal lane so the live map/partner page stops showing the borrowed-census rungs.

**Acceptance:** `greenfield_mode` no longer points at a peer census file; the network/SAM/TAM rungs
carry an honest template-band label; floor unchanged; deck + sheet + tracker agree.

---

### Lane note
Bug B (Careem `registry_key` leak → `bolt-uae`) and the East Africa narrative are **already fixed in
`partners/bolt.json`** in this PR — a future Grok build reads the corrected inputs; do not rebuild from
a stale source. Bugs A and C above still need the model re-run + front-end reseal.
