# Ocean Whisperer — content, phases, deck & routing review

**Date:** 2026-06-24 · **Author:** Tasklet · **Benchmark:** FP / UAE partner-ready bar
**Scope:** partner-ready prose + phases (fixed), deck (specified), routing (diagnosed + corrected + Grok handoff)

---

## 1. Headline

One bad assumption in the source brief cascaded through the whole proposal: **`OCEAN-WHISPERER-FINE-TUNING.md` §3 listed "Hato airport waterfront" as a calm *leeward* grounded corridor.** Hato is on the **north / windward** coast. That single error is why:

- the **map is a mess** — three airport→resort legs circumnavigate the island and fan out to a phantom point in open water;
- the narrative quietly **contradicts itself** — selling "calm leeward, ~90% uptime" on legs that round the windward side;
- the same wording leaked into the **deck**.

On top of that, internal jargon ("Pioneer-edge", "flagged amber", "Quanta-LR roadmap leg", "145A/400V 3-phase", `§`-doc citations) was sitting in buyer-facing prose — the readability problem you flagged.

All content fixes are applied; routing is corrected at the source and handed to Grok to reseal.

---

## 2. Routing — the map mess (diagnosed)

The teal fan converging in open water south of Curaçao is **not** bad node coordinates and **not** the corridor source. It is three Hato-origin legs routing the long way around the island:

| route_id | leg | straight | **sealed path** | detour |
|---|---|---|---|---|
| `rn-838ccd054530` | Hato → Baoase | 6.3 nm | **29.2 nm** | **×4.6** |
| `rn-a88f7e7cffc2` | Hato → Spanish Water | 8.7 nm | **30.8 nm** | **×3.5** |
| `rn-a3a94b8dbc88` | Hato → Sandals | 9.4 nm | **30.4 nm** | **×3.2** |

All three dip to **11.98°N** (open water) before doubling back. The other 7 Curaçao legs are clean. The land-only QA gate passed them because `land_km = 0` — but a land-free route can still be a 30 nm circumnavigation.

**What I corrected (source, my lane):** repointed both grounded airport legs to a **leeward embarkation at Piscadera** (air arrival stays the demand source; a short land transfer reaches calm water), set their distance to `null` for reseal, fixed the §3 geography error, and wrote `GROK-ROUTING-GUIDANCE.md`.

**What Grok must do (geometry lane):** reseal the airport legs as short leeward runs, retire the three windward route_ids, add a **detour-ratio + latitude-bbox QA gate**, and re-run the cascade on the new (shorter) distances. Full spec + acceptance criteria in the guidance note.

**Decision for you (flagged, not auto-applied):**
- **Option A (applied):** airport = demand source, embark leeward at Piscadera. Preserves the CORE air-arrival revenue pool, made honest.
- **Option B:** drop air→resort from grounded Navier sea corridors; airport becomes Ocean Whisperer's air domain, Navier's grounded water = cruise-pier→resort + resort→resort + Klein seasonal. Cleaner, smaller. Say the word and I'll switch.

---

## 3. Partner-ready content — jargon → plain (applied)

24 prose edits in `partners/ocean-whisperer.json`; zero residual jargon in buyer-facing fields. Representative:

| Field | Before | After |
|---|---|---|
| multimodal_fit | "A foiling vessel **meets arrivals at Hato airport's waterfront**…" | "Curaçao's two gateways — the Hato air arrival and the Willemstad cruise mega-pier — both feed the calm leeward coast…" |
| journey (Bonaire) | "A **Pioneer-edge / Quanta-LR network leg** — the standardization story…" | "A direct Curaçao–Bonaire sea link — the island-to-island standardization story (on the network roadmap)." |
| journey (Klein) | "…showcase run to Klein Curaçao **(seasonal — flagged amber for swell)**." | "…showcase run to Klein Curaçao — offered seasonally, in the calm-water months." |
| objection (range) | "…a Quanta-LR roadmap leg — **never faked on a 70 nm boat**." | "…a longer-range-vessel roadmap leg — each leg matched to the right vessel for the distance." |
| the ask | "charging — **their 145A/400V 3-phase is not enough**, to be specified" | "charging — a berth-side charging upgrade to be specified with the operator" |
| proof source | "OCEAN-WHISPERER-FINE-TUNING.md **§3/§6**" | "Curaçao marine climatology — leeward coast; below the hurricane belt" |

Internal `render` directives (`roadmap-amber-dashed`) and `_provenance` were intentionally left — they don't render to the buyer.

---

## 4. Phases (applied)

The three-phase ladder (3 → ~10 → network) is sound and matches the buyer's stated path. Fixes:

- **Phase 1** narrative reworded so the air-arrival flow embarks leeward (no longer implies a windward-airport sea hop).
- **Phase 3** narrative de-jargoned ("on the longer-range vessel" instead of "on Quanta-LR … amber-dashed, never faked on a 70 nm boat").
- Phase scope, cities, timelines, use-cases unchanged.

---

## 5. Deck (specified for Grok — live Slides not hand-edited)

The deck text is generated from `ocean-whisperer.json` (`source_pointer`), so the §3 fixes above flow into the deck on the next deterministic regen. Two deck-only strings still need to track the corrected language:

- `g3eec5122801_0_111`: "Airport, cruise-pier and inter-resort legs on **sealed leeward geometry**." → "Airport, cruise-pier and inter-resort legs along Curaçao's calm **leeward coast**."
- `g3eec5122801_0_304`: "Bonaire + Aruba legs **flagged amber-dashed**; Quanta-LR cross-island reach." → "Bonaire and Aruba shown as **roadmap legs** — the longer-range island-to-island reach."

Structural checks against the locked rules: slide 2 stays KPI-free with its own image (not the Three C's background); Three C's framing stays **Cost · Convenience · Comfort**; $1M/vessel economics; Careem/FP 6-line flush-left OPEX block; N30 compositing / market-specific backgrounds / no Atlas-generated images. Regen via Slides API only — no PPTX round-trip, no full-deck replace.

> **Map slide:** must not ship until Grok reseals the airport legs — it currently shows the open-water fan.

---

## 6. What to do differently (so this doesn't recur)

1. **Validate source geography before sealing.** The error entered as prose ("airport waterfront — air↔sea transfer") and was never coast-checked. Every grounded leg in a "calm leeward" set should be confirmed on the correct coast at authoring time.
2. **Detour-ratio QA, not just land-crossing.** `land_km = 0` is necessary, not sufficient. Adopt the ×1.35 detour gate + regional latitude bbox (snippet in the guidance note) as a permanent reseal gate.
3. **Label/geometry consistency check.** Stored `distance_nm` must stay within ±10% of the sealed path; a 9 nm label on a 30 nm line should have failed.
4. **Jargon firewall on buyer prose.** Keep render/engineering vocabulary (`amber-dashed`, `Pioneer-edge`, voltages, `§`-doc refs) out of any field that renders to a partner — same gate we're standing up for city briefs.

---

## 7. Shipped vs. pending

**Applied (this PR):** partner-record prose + phases · corridor-source airport repoint + Klein `season_days: 90` · §3 geography correction · `GROK-ROUTING-GUIDANCE.md` · this review.

**Pending (Grok / you):** reseal airport legs + detour QA gate + cascade rerun (Grok) · Option A vs B decision (you) · deck regen + 2 deck strings + map-slide re-render (Grok) · re-verify the live map.
