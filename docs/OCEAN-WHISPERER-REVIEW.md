# Ocean Whisperer — proposal review & remediation

**Goal:** bring Ocean Whisperer to FP / UAE (RAKTA) quality. Reviewed against `french-polynesia.json` and `ras-al-khaimah-uae.json` as the gold benchmarks.

**Verdict:** the *bones* are right (clean top-line narrative, full `growth_case`/TAM, captive 55% economics, ABC scale-vision intent). What drags it below FP/UAE is **internal jargon leaking into buyer-facing prose**, a few **precision gaps**, and **missing city briefs** for the three ABC islands. The prose leaks are fixed in this pass; the structural items are itemized below.

---

## A. What was wrong (and what I already corrected)

### 1. Internal jargon in customer-facing narrative — FIXED
The render-pipeline vocabulary had bled into prose a partner actually reads. Eleven strings rewritten into buyer voice (render directives like `roadmap-amber-dashed` were left untouched — those are correctly internal):

| Field | Was (internal voice) | Now (buyer voice) |
|---|---|---|
| `journeys_unlocked[].with_navier` | "A Pioneer-edge / Quanta-LR network leg — the standardization story, island-to-island (roadmap)." | "A direct island-to-island sea link — today served only by a small turboprop — extending one premium standard across the Dutch Caribbean as the network grows." |
| Klein Curaçao leg | "(seasonal — flagged amber for swell)" | "a seasonal route, offered in the calm-water months" |
| `objections[].response` | "a Quanta-LR roadmap leg … never faked on a 70 nm boat" | "served by the long-range Quanta-LR as the network scales — each leg matched to the right vessel for the distance" |
| `the_ask.next_step` / `why_navier_now` | "charging — their 145A/400V 3-phase is not enough, to be specified" | "a charging upgrade to be specified with the operator" |
| `proof_points`, `phases[2].narrative`, `range_gate_note` | "flagged amber", "never faked on a 70nm boat" | calm-water / right-vessel-for-the-distance phrasing |

**Rule applied:** engineering specs (amps/volts/phase), render tags (amber/dashed/roadmap), and pipeline words (silent-drop, faked) never appear in buyer prose. They live in `render`, `_meta`, or `internal` only.

### 2. The ABC scale-vision wasn't rendering — FIXED via PR #97
Separately diagnosed: the Aruba roadmap leg was silently dropped at seal and Bonaire was demoted to a non-roadmap journey, so the map showed only Curaçao. Re-seal spec shipped to Grok (PR #97). That's the "why it only shows Curaçao" fix; this review is the readability/quality fix.

---

## B. What still needs doing (itemized)

### Precision gaps (low-risk, Tasklet can fix; one needs Grok)
1. **Bonaire distance is inconsistent** across the record: `journeys_unlocked` says **33.3 nm**, `objections` say **~38 nm**, the combined brief said **~30 nm**. Pick one. Geometry is Grok's sealed lane → flagged in PR #97 for reconciliation. (Briefs use ~38 nm as the working figure.)
2. **Klein Curaçao `season_days`** — Grok defaulted 120; recommend tightening to ~90 (calm-water quarter) with `weather_uptime_factor` 0.6 kept as the within-window sailable fraction (separate guardrail in the answer already sent).

### Missing city briefs — 3 of 3 ABC now written (this pass)
The ABC islands shared one combined `aruba-curacao-bonaire.json` (tier "starter") even though Ocean Whisperer treats them as three distinct market nodes. Authored three **gold-tier** per-island briefs, grounded:
- **`curacao-curacao.json`** — anchor; 1.57M visitors, 834,890 cruise pax/328 calls, below-the-belt year-round leeward calm.
- **`bonaire-bonaire.json`** — roadmap; 182,181 stay-over (2024 record), ~359K cruise, entire-coast marine park = conservation fit for silent/zero-wake.
- **`aruba-aruba.json`** — roadmap; ~810K cruise pax/~307 calls, 9.2M+ hotel nights, Quanta-LR for the 70 nm reach.

(The old combined `aruba-curacao-bonaire.json` can be retired once the per-island nodes are bound; left in place for now to avoid breaking any current binding.)

---

## C. The systemic problem — and what to do differently

These gaps weren't random: **there was no completeness gate on city briefs**, so partial ones reached decks. A library-wide audit (new `scripts/validate-city-briefs.py`) found **28 of 141 briefs incomplete**, in three repeating failure classes:

| Failure class | What it breaks in the deck | Count |
|---|---|---|
| `use_cases` are bare one-liner strings (not `{archetype,title,body,platform}`) | "Use cases" section renders thin/empty | ~13 |
| `navier_fit` is a flat string (not `{pioneer_ii, quanta_lr}`) | "Why marine mobility here" renders empty | ~13 |
| `demand_signals` < 3 / no `sources` / thin summary | unverifiable, low-credibility brief | ~15 |

**The Grab Thailand briefs you flagged are exactly class 1+2** (`koh-chang`, `koh-larn`, `koh-phangan`, `koh-phi-phi`, `koh-tao`, `krabi`, `pattaya` — all ~2.4–3.3 KB with string `use_cases` and flat `navier_fit`).

### Process changes (so it doesn't recur)
1. **Adopt the gold-standard schema as the definition of done** for any brief: structured `use_cases` (archetype/title/body/platform), `navier_fit` as `{pioneer_ii, quanta_lr}`, ≥3 sourced `demand_signals`, ≥250-char summary, `journeys` with today/with-navier, and `sources`.
2. **Run `validate-city-briefs.py --strict` as a pre-handoff gate** before any brief enters a deck or partner proposal — fails CI if any brief is incomplete. (Mirrors the proposal-parity definition-of-done, extended down to the brief layer.)
3. **No "starter"/combined multi-city briefs for partner-facing markets** — if a partner treats places as distinct market nodes (ABC, Côte d'Azur), each node gets its own gold brief. Combined files are fine only as regional overviews.
4. **Jargon firewall:** render tags, engineering specs, and pipeline words stay in `render`/`internal`/`_meta`; the validator can be extended to grep buyer-prose fields for the banned vocabulary.
5. **Division of labor:** Tasklet authors/repairs briefs (research + narrative = source assets); Grok seals geometry/economics. Briefs carry a `_meta.lane` note to keep the boundary explicit.

---

## D. Remaining brief backlog (proposed order)
Per the standing "Thailand first, then all Bolt markets, then the rest" cleanup rule:
1. **Thailand (7)** — the briefs you flagged. *Next batch.*
2. **Côte d'Azur per-city (4)** — Nice, Antibes, Cannes, St-Tropez (Monaco already has its own). **Needs confirmation:** are these distinct Atlas market nodes, or is `cote-dazur-france` still a single node? I'll bind by ID, not guess.
3. **Remaining 17** — Morocco, Philippines, India (sources), USA NE (summaries), etc.

Full machine-readable gap list: `scripts/validate-city-briefs.py` output.
