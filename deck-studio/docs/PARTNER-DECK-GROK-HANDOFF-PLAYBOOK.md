# Partner Deck Grok Handoff Playbook

This repo copy mirrors the workspace skill `partner-deck-grok-handoff`. Use it when existing partner/economics assets need deterministic Deck Studio artifacts for Grok to create or bind a live deck.

> **2026-06-21 upgrade — read this first.** The first Grok-built decks (e.g. the Bolt sandbox) failed parity: they were whole-file copies of the gold Grab deck with a few text boxes poked, leaving Grab's logo, Grab's Singapore routes, and Grab's economics numbers in place, with brand fonts reset to Arial-black and text overflowing. Root cause was **not** a Grok capability gap — it was that the handoff told Grok *what* to say but not *how* to edit. Going forward, Tasklet emits a deterministic **object-keyed edit plan** and Grok applies it verbatim. See `DECK-PARITY-DIAGNOSIS-2026-06-21.md` and `DETERMINISTIC-DECK-EDIT-PLAN-CONTRACT.md`.

> **2026-07-23 upgrade — copy tone & completeness.** The DiDi/inDrive Mexico, Egypt and Brazil rebuilds shipped *mechanically* clean but read as **internal drafts, not partner pitches**: hedged "route-by-route / candidate markets / review" framing, a phased-review ask, dropped **Three C's** and confident **Partner Proposal** slides, thin bullet-list econ slides instead of the 3-column table, a prize ladder missing its **platform** tier, an Atlas link pointed at the wrong country, and model/QA jargon (`census g=`, "monotonic", "(MID)") plus the gold deck's Grab/Singapore/SEA **speaker notes** left in the file. None of these tripped the six mechanical gates. The rules below add the missing **copy-tone and content-completeness** gates. The confident bar-setter is the **99 × Navier Brazil** gold deck — match its register, not a "review" register.

## Deck archetypes

Pick the archetype **before** building the edit plan — it sets the route rule, economics frame, and slide content:
- **Mobility / super-app distributor** (Grab, Bolt, Careem, Yango): use the standard sequence in this playbook as-is. City-mobility TAM, contested capture band, airport/commute/premium use cases.
- **Hotel/resort operator-developer** (Minor, Aman, Four Seasons, Constance, …): use [`OPERATOR-DEVELOPER-ARCHETYPE.md`](./OPERATOR-DEVELOPER-ARCHETYPE.md) — captive property-graph routes only (gateway→property, property↔property, property→excursion), captive economics (capture ~0.85–0.90, LB-254), headroom = WIDTH (keys/openings/clusters). Keeps the slide skeleton and all base rules; overrides only the content frame of slides 2, 3, 4, 5, 7, 9.

## Steps

1. Read partner JSON, data-clean partner JSON, finance/growth assets, economics Sheet URL, and current handoff status.
2. Build `deck.config.json` with pending or live deck ID, source paths, rules, and economics URL if known.
3. Build `slide-manifest.json` and `content-source.json` (narrative source map).
4. Build `image-manifest.json` with per-object image classes (`brand_logo` vs `market_background`/`n30_composite`), `ASSET-REGISTRY.json` keys, fallbacks, and mandatory provenance.
5. **Build `deck.editplan.json`** — the deterministic, object-keyed Slides API batchUpdate plan, validated against `schemas/deck-editplan.schema.json`. This is the artifact Grok applies. It must:
   - reference `golden-template-map.json` (extracted once from the gold deck);
   - use the **style-preserving replace** form (deleteText → insertText → updateTextStyle per run → updateParagraphStyle) so brand fonts/colors survive;
   - keep every captured `autofit` unchanged;
   - keep every string within its object `char_budget`;
   - rebuild multi-run KPI lines from the economics sidecar (never hand-typed, never left as the gold partner's numbers);
   - emit full unit-economics header eyebrows (`WHAT ONE BOAT EARNS · {MARKET}`) — never truncate
     market labels to fit shorter gold-template sample budgets on duplicated slides;
   - wire slide **13** body phrase (`Navier × {Partner} Atlas`) as a white underlined inline Atlas hub
     link via `close_atlas_link` in `slide-link-bindings.json` (`link_style: inline_phrase`);
     title stays `Explore the {Partner} marine network` (not linked);
   - wire market-slide route lists (slides 4–6, 14–18) via `decks/{deck}/market-route-bindings.json`:
     four marquee routes, amber `▸` bullet only, white body text, blank line between routes
     (`builders/deck_market_routes.py`);
   - mark every gold slide `edit | hold | remove` (no silent truncation);
   - swap brand logos (hard requirement) and either composite/replace market backgrounds or fall back to the approved generic Navier hero — **never inherit the prior partner's image**;
   - attach a `qa.leak_denylist` and `qa.expected_object_ids` for Grok's gates.
6. Add batch queue/status/prompt files under `handoff/partner-map-model/{batch}/`.
7. Validate all Deck Studio JSON schemas.
8. Tell Grok: copy gold deck → assert object-id baseline (drift gate) → apply `deck.editplan.json` via Slides API batchUpdate verbatim → run the thirteen QA gates (six mechanical + seven copy/tone/completeness) → return a receipt with deck id, op count, leak/style/budget/image/hedge/jargon/notes/spine/econ/link/image-completeness scan results, and slide thumbnails.

## Non-negotiables

- No PPTX round-trip or full replace.
- No Atlas-generated images.
- No invented route IDs, city IDs, BPs, economics, sheet URLs, or market claims.
- Null beats confidently wrong — a held/neutral slide always beats a leaked prior-partner route or number.
- A deck must never carry another partner's logo, routes, economics, or market name.
- Brand fonts (Exo 2 / Poppins) and captured colors must survive every edit; no Arial-14-black resets.
- Deck-prep complete is not proposal complete.

### Copy, tone & completeness (partner-facing register)

These are the failures the six mechanical gates do not catch. The deck is a **confident pitch to the partner**, not an internal review.

- **Confident register, never a hedge.** Banned copy anywhere a partner can read it: "route-by-route", "candidate market(s)", "held/pending until confirmed", "consider a pilot only once…", "phased review", and any cover/section title framed as a "…mobility review". Write the assertion, not the caveat.
- **The Ask is fixed and forward.** Always **Next steps → ① working session · ② vessel demo · ③ pilot scope**. Never a VERIFY / PILOT / SCALE hold-flow or a "joint route review is the next step" line.
- **No internal model/QA jargon on a slide or in notes.** Banned strings: `census g=`, "monotonic", "SOM Full ≤ SAM", "(MID)" / "(THIN)" / "(FULL)", "Mid basis", and any sidecar field name or basis/tier annotation. These live in the sidecar, never in partner-visible text.
- **Scrub speaker notes.** Notes inherited from the gold deck (Grab / Singapore / SEA / "Jaideep direction" commentary) must be **removed**, not just the on-slide text. A clean slide with a dirty note still leaks.
- **Spine must include the confidence slides.** A render-complete mobility deck carries the **Three C's** (Cost · Comfort · Convenience), the confident **Partner Proposal** ("Your world / Where you are today / What you're up against / Where Navier fits / Why now"), and the confident **close**. Missing any = not complete (this is a spine gate, per `SLIDE-SPINE-AND-VARIANTS.md`).
- **Prize ladder is always five tiers** — SOM · SAM · TAM · GMV · **Platform revenue**. Never drop the platform rung; if the sidecar leaves `partner_platform_rev_on_navier` null, compute it as **18% × journey GMV** rather than omitting the tier.
- **Econ slides are the 3-column table** — **Revenue build · Annual run cost · The result** — every line item tying to the economics sidecar. Never a thin bullet list. A longer-range / sub-30%-margin corridor is titled and framed **honestly** ("a longer-range corridor"); never claim "self-funding" on a 25-plus-year payback.
- **Atlas link resolves to this deck's own `/{partner}/{country}`** — never the gold's path (the Mexico deck shipped pointing at `/didi/brazil`).
- **Placeholder cities are de-hedged, not economics-faked.** Until the four-input gate clears (**route ID · distance · fare · anchored demand**), a market slide uses confident "corridors mapped, sourcing underway" copy and carries **no** econ card. Once all four clear, it graduates to a full sourced city slide **and** its own "WHAT ONE BOAT EARNS" card, and the country ladder is re-rolled to include it.
- **Every background role is declared and deck/city-specific — no template-inherited images.** The deck's `image-manifest.json` must enumerate **all** background roles (not just cover + Atlas slots) bound to live object ids, and `slide-image-bindings.json` **must exist** (its absence is what let backgrounds drift). `partner_roles_bg` / `tam_bg` / `value_prop_bg` / `close_bg` are **one composite per deck**; `econ_market_bg` is **one per city** (city-keyed, reusable). A deck is not render-complete if any background role is undeclared, the bindings file is missing, two city econ slides share one plate, or any background still resolves to the gold/template chassis or a sibling deck's asset. Per `IMAGE-ROLE-CONTRACT.md`; unresolved image roles stay `needs_generation`/`needs_sourcing`, never a borrowed plate.

## QA gates Grok must pass (returned in the receipt)

1. Drift gate — all plan object ids exist on the fresh copy.
2. Leak scan — zero hits on `qa.leak_denylist`.
3. Style-reset scan — no Arial-14/default-black runs where the golden map specifies Exo 2/Poppins.
4. Budget scan — no edited text exceeds `char_budget`.
5. Image-inheritance scan — no image still resolves to the gold deck's source asset.
6. Render thumbnails attached for human spot-check.
7. Hedge scan — zero hits on the banned-copy list ("route-by-route", "candidate market", "held/pending until confirmed", "phased review", "…mobility review" titles) across slides **and** notes.
8. Jargon scan — zero hits on `census g=` / "monotonic" / "SOM Full ≤ SAM" / "(MID)"/"(THIN)"/"(FULL)" / "Mid basis" / sidecar field names, across slides **and** notes.
9. Notes-clean scan — no speaker notes inherited from the gold deck (Grab / Singapore / SEA / internal-direction commentary).
10. Spine-completeness — Three C's, Partner Proposal, the ① / ② / ③ Ask, and the close are all present; prize ladder carries all **five** tiers incl. Platform revenue.
11. Econ-format — every unit-econ slide is the 3-column table (Revenue build · Annual run cost · The result) with line items tying to the sidecar; no thin bullet variant; no "self-funding" claim on a 25-plus-year payback.
12. Atlas-link — resolves to this deck's own `/{partner}/{country}`, not the gold's.
13. Image-completeness — `image-manifest.json` declares every background role bound to a live object id, `slide-image-bindings.json` exists, no per-deck background (`partner_roles_bg`/`tam_bg`/`value_prop_bg`/`close_bg`) or per-city `econ_market_bg` is shared across two slides, and no background resolves to the gold/template chassis or a sibling deck's asset.
