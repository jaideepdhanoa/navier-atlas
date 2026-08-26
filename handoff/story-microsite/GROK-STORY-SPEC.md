# /story microsite — SPEC v2 (2026-08-26)

**Supersedes GROK-STORY-SPEC.md (v1) in full.** v1 is retired: its headlines were authored fresh for
/story and its section order had no narrative arc. v2 fixes both by construction.

## The two v2 laws

1. **No new slogans.** Every headline is copied VERBATIM from an existing approved surface. Each
   section in `story.json` carries a `source` citation (file + field) or a `headline_source` binding
   ("copy verbatim from X"). If a headline cannot be sourced, the section ships without one — never
   write copy. Functional labels (Contact / Watch / Read) exempt but plain.
2. **The /invest arc, public-safe.** Chapter order mirrors /invest: **hero (thesis) → 01 problem →
   02 proof → 03 product → 04 dual-use → 05 network vision → films/press → contact.** /story is the
   public top of the ladder (/story → /teaser → /invest).

## Section order (binding)
`hero` → `problem` → `proof` → `product` → `dual-use` → `network` → `deeper` → `talk`
— exactly as in `contracts/story.json` v2. Do not add, remove, or reorder sections.

## Visual system (visual-first is the point of /story)
- Every chapter anchored by real photography or film; copy blocks are short and never stand alone.
- **FILMED/RENDER badge on every visual** (map component exempt — data viz, not imagery).
- Ambient loops: muted autoplay, ≤15s, native aspect, never upscale (te263 montage is 826×720 with
  dark letterbox — keep native).
- Films: click-to-play with strong poster frames; never autoplay with sound.
- **Text never sits on a photo background** (scrim per brand system on hero only).
- **Press cards:** outlet wordmark + verbatim article headline + external link, opening in new tab.
  Article headlines render exactly as authored in `story.json` — never re-titled.
- No text under 24px at 1280/1440/2560. No ellipsis/truncation on any headline.

## Kill-list (fail the build on any hit — 31-term scan unchanged from v1, plus)
- Robb Report: never linked or named anywhere on /story.
- 400V / 100 kW chip: defense-only, never on /story.
- No round, valuations, TAM, pipeline entity names, "royal office", Gulf counterparties, energy /
  sea-grid / floating power / ocean data center content, N30D, no launch-trigger or demand-gated
  mechanics language.
- No LC-180. No unit economics. No fare/seat pricing.
- Run `scripts/` leak scan with the v1 31-term list + the above before any deploy.

## QA gate (before URL is shippable)
1. Screenshots at 1280/1440/2560, every section.
2. Leak scan (above) = 0 hits.
3. Badge check: every visual carries FILMED or RENDER.
4. Headline diff: every rendered headline byte-equal to its cited source field.
5. All press links resolve (200) and open externally.
6. Analytics events per v1 spec unchanged.

## Contracts
- `contracts/story.json` — v2 (this PR). Renderer renders authored strings only.
- `contracts/assets.json` — v2 (this PR). All paths repo-verified 2026-08-26; two interior plates
  land with PR #400 (soft dependency, note in assets file).
- `contracts/site.json` — unchanged from v1 (route `/story`, no gate).
