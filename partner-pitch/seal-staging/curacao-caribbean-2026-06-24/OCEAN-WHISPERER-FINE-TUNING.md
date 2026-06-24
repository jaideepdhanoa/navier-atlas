# Ocean Whisperer × Navier — fine-tuning brief

**What changed:** the generic "Curaçao / ABC trio" build is now a **named fleet-buyer proposal** for
**Ocean Whisperer** (Giovanni & Erika Tonti). We keep the French-Polynesia proposal shape and the
captive-cluster approach — but re-aim the narrative, geography, vessel framing, and demand anchors at
this specific buyer. Sources: the demo-prep doc + theoceanwhisperer.com.

---

## 0. ⚑ Economics guardrail — LOCKED by Jaideep 24-Jun (Grok must seal exactly this)
Two decisions are now final; treat them as hard gates in the cascade, not defaults:

1. **CAPEX tier = $1M hospitality.** Ocean Whisperer is a dedicated hospitality-partner proposal, so it
   takes the **$1M/vessel hospitality tier** (region-independent; overrides the $900K/$600K commercial
   rule). This resolves the §8 open decision — model at **$1M**, not $900K. Scope (a): the $1M tier applies
   only to dedicated hospitality proposals (FP, Ocean Whisperer, Minor's scoped view).
2. **Captive *philosophy* — yes. FP's *flat ladder* — no.** Carry FP's captive, capture-led treatment, but
   **do NOT flat-line the ladder to the floor the way FP does.** FP sits flat *only because* it captures
   **~90%** of major routes (≈no headroom). Curaçao's capture basis is **~55%** (`captive_capture_basis:
   0.55` in `ABC-DEMAND-ANCHORS.json`) → **~45% headroom remains**, so **SOM must sit below SAM/TAM** and
   the ladder must rise. Applying FP's flat treatment here would *under*-state Curaçao. **55% ≠ 90%.**
   (The headroom may be modeled as induced demand + width per §5/LB-254; the hard gate is simply: ladder
   rises, SOM is not pinned to the floor.)

> Reminder on the lane: the **0.55 basis + $1M tier are flagged inputs/specs (Tasklet's lane)**; **Grok
> owns applying them deterministically** in the model→deck cascade. Tasklet does not hand-crank the rungs.

---

## 1. Who the buyer actually is (the unlock)
Ocean Whisperer is **already an ultra-luxury, aviation-grade experience brand** — today flying the
**MD 520N NOTAR** *helicopter* over Curaçao: whisper-quiet, **four guests at a time**, "by private
arrangement," curated signature journeys (Willemstad Prelude, Coastal Sonata, Whisperer's Hour, Sunset
Ceremony), destinations **Baoase · Sandals Royal Curaçao · private residences**, with a reef-preservation
tithe. Founders are **career corporate-aviation professionals** (Giovanni: 25–30 yrs flight ops, command,
safety leadership; Erika: inflight leadership + guest experience).

**The spine of the pitch:** Navier is the **marine extension of an aviation-luxury brand they already
operate** — the same DNA carried from the air to the water:
- whisper-quiet **NOTAR ↔ foiling** ("the quietest in its class")
- four-guests / curated / "by private arrangement"
- aviation-grade reliability + inspection discipline ("they view Navier as an aircraft, not a boat")
- reef / marine-life preservation

> They are **not** buying a boat. They are buying the **water layer of the Navier Network** — and a way to
> **standardize the level of experience** across air, water, and future markets. *"Make it cool to take the water."*

## 2. Narrative re-aim (vs French Polynesia)
- **Hero:** "Navier × Ocean Whisperer — Curaçao, by foil." Quiet luxury, air-to-water, aviation-grade.
- **Why now:** their March-2026 launch + an aviation operator who already owns the luxury-mobility brand
  and the resort/government/port relationships. Curaçao Tourism Board endorsement, Port Authority engaged,
  government contacts live.
- **Differentiation:** Candela / MobyFly / Vessev named in the room → *"nothing quite like Navier"*
  (range + cabin + software-defined fleet + at-scale operating network). Keep this factual, not boastful.
- **Sister thesis = standardization:** one experience standard, replicated route-to-route and market-to-
  market → this is the on-ramp to the broader **Caribbean x Navier** network (see §7).

## 3. Geography — Curaçao core, network as the scale vision
**Grounded / commercial-now (leeward coast, calm ~90% of the time):**
- Willemstad (cruise mega-pier + waterfront / Queen Emma) — gateway + cruise-aggregator feed
- Hato (Curaçao Int'l) airport waterfront — air↔sea transfer
- Piscadera Bay — Marriott / JW-style cluster
- Spanish Water / Santa Barbara — **Sandals Royal Curaçao** (350 rooms, $2K–$8K/night)
- Baoase (south coast, near Willemstad) — existing OW destination
- Jan Thiel — resort/leisure cluster

**Seasonal (amber):** Curaçao ↔ **Klein Curaçao** excursion — real demand but **5–7 ft swell, seasonal**;
flag honestly, do not present as year-round.

**Roadmap / network (Quanta-LR + "standardize across markets"):** Curaçao ↔ Bonaire, Curaçao ↔ Aruba.
These are the **standardization/scale** story here and the **operational core of the separate Caribbean
proposal** (§7) — never faked on a 70 nm boat (amber-dashed).

## 4. Vessel & fleet framing — **N30, 3 → 10 → network**
- Hero vessel = **N30** (their stated product; ~$1M list). Cirrus-SR22-like interface familiarity,
  sport-mode ~30° banking — lean into the "feels like flying" reaction.
- Fleet ladder reframed to the **buyer's** path, not territory saturation:
  **Phase 1 = 3 boats** (pilot, leeward resort transfers + cruise feed) → **Phase 2 = ~10** (full Curaçao
  premium network + seasonal Klein Curaçao) → **Phase 3 = network** (Bonaire/Aruba + standardized
  multi-market Navier Network). Matches their "3 boats, target launch March, scale to global."

## 5. Demand anchors (captive / luxury — replace territory-wide figures)
- Curaçao tourism **~1.7M** annual visitors; OW **cruise-aggregator network ~1M pax/yr**; **min initial
  exposure ~3,000+ pax**.
- Named partners under discussion: **Sandals Royal Curaçao** (350 rooms, $2K–$8K nightly), **Baoase**,
  **BASI / Balasy**, **Marriott / JW-style**.
- Use cases: **resort transfers (CORE revenue driver)**, premium passenger network, Klein Curaçao seasonal
  excursions, nature-preserve routes, VIP curated packages, **light goods / supply** between destinations.
- **Capture = captive (~55%+ FP-style).** Per LB-254: at high capture the floor already ≈ the pool;
  headroom is **induced demand + width** (more guests, more resorts, more islands), NOT a capture ramp.

## 6. The buyer's four concerns → must-answer in the deck
The doc names exactly four concerns + a list of "gaps to address." Bake these into objections/proof:
1. **Sea state** — quantify: leeward Curaçao calm ~90%; Klein Curaçao seasonal swell; foiling ride quality
   + sport mode. (Their #1 instinct as aviators: operability envelope.)
2. **Capacity** — N30 pax + fleet throughput; cruise-feed surge handling.
3. **Range** — N30 range gate (intra-island now; Bonaire/Aruba = Quanta-LR roadmap).
4. **Maintenance plan** — aviation-grade inspection/maintenance discipline; service model.
**Plus** (deck = scale & system, not product basics): operating economics (cost/trip, utilization), fleet
scaling economics 3→10, **software + fleet-ops platform**, **financing paths** (direct sale ~$1M / fleet
financing / lease / hybrid capex+service / infra co-invest), **infrastructure** (charging — their
145A/400V 3-phase is *not* enough, spec it; marina upgrades + a Navier **lounge**), and a **customization
framework** (High: routes, experience, packaging, financing · Medium: SLAs, software branding, interior ·
Low: hydrofoiling, propulsion/redundancy, safety, performance envelope).

## 7. Clean two-proposal division (recommended, matches your two asks)
- **`ocean-whisperer.json` (THIS proposal)** — Curaçao luxury **core** + the standardization narrative.
  archetype `hospitality`, layout `single`, anchor city = Curaçao. ABC/wider-Caribbean appears only as the
  **scale vision**.
- **`caribbean.json` ("Caribbean x Navier")** — the **generic Caribbean network** (the renamed
  caribbean-mobility), where the **full ABC trio promotion** + wider Caribbean live, mirroring FP. The
  Aruba/Bonaire anchors + 3 country-reference rows I already sourced feed **here**.

This resolves both of your requests cleanly and keeps each proposal honest about its scope.

## 8. ~~Open decision~~ → RESOLVED 24-Jun: CAPEX = $1M
**CAPEX / vessel price — DECIDED.** Ocean Whisperer models at the **$1M hospitality tier** (see §0), which
also matches the buyer doc (N30 ~$1M list / "direct sale ~$1M/vessel"). The earlier $900K default is
superseded. *(The generic `caribbean.json` network proposal in §7 is **not** hospitality-scoped and stays
on the $900K commercial tier — keep the two proposals' tiers distinct.)*

## 9. Slide/deck rules carried forward (unchanged)
Slide 2 KPI-free with its **own distinct image** (not the Three C's background); slide 3 = market-overview
KPIs; Careem/French-Polynesia **OPEX = 6-line flush-left**; canonical **N30 compositing**; market-specific
**Curaçao** backgrounds; **no Atlas-generated images**; stable image URLs / no embedded inaccessible
images; **no full-replace / PPTX round-trip** for live decks. Provide the **Ocean Whisperer logo** where
supported (their site has one); else null. Grok owns deterministic model→deck generation.

## 10. Build sequence (the honest dependency)
Per the model-cascade rule, **real route-IDs + economics require Grok to seal geometry first**:
1. **Tasklet** authors corridors + demand records + country-reference + BP spec + proposal narrative.
2. **Grok** seals route IDs / render / map.
3. **Tasklet** cascades economics on the sealed IDs (real numbers) → sheet + master tracker + sidecar.
4. **Grok** builds the economics sidecar into the gold package.
Proposal ships with `economics_status: pending` on journeys until the cascade runs on sealed IDs; the
growth_case ladder is **generated by the cascade, never hand-typed**.
