# Deck archetype: hotel/resort operator-developer

Reusable deck-structure + narrative variant for partners that are **hotel developers/operators**, not mobility/ride-hail/super-app distributors. First applied to **Minor Hotels**; reuse for **Aman, Four Seasons, Constance, Six Senses, Banyan Tree**, and similar portfolio operators.

This repo copy mirrors the workspace skill file `partner-deck-grok-handoff/OPERATOR-DEVELOPER-ARCHETYPE.md`. Use it **in addition to** `PARTNER-DECK-GROK-HANDOFF-PLAYBOOK.md` and the deterministic edit-plan contract. Everything in the base playbook still applies unchanged (Slides-API-only, object-keyed `deck.editplan.json`, style-preserving replace, image discipline, N30/N35 compositing, partner-logo-on-cover, 6-line OPEX, QA gates, reporting language). This file only overrides **deck structure, the route rule, the economics frame, and the narrative**.

## When to use this archetype

Pick the operator-developer variant when **all** of these hold:
- the named partner **owns/operates physical destinations** (hotels, resorts, branded residences), and
- the value to Navier is **captive guest throughput at those properties**, not city-wide consumer mobility, and
- headroom comes from the partner **opening more properties** (keys/clusters/pipeline), not from winning a larger share of an open mobility market.

If the partner is a mobility/super-app/ride-hail distributor (Grab, Bolt, Careem, Yango), use the **standard sequence** in the base playbook, not this variant.

## Governing route rule (hardest eval gate)

Routes exist **only inside the partner's own property graph**. Three captive route classes only:
- **(A) gateway → property** (airport/city gateway ↔ a partner hotel)
- **(B) property ↔ property** (intra-portfolio, same operator)
- **(C) property → signature excursion** (operator-owned/partnered destination experience)

Any leg with **no partner-owned endpoint is forbidden**. Encode as the partner's hardest gate — **archetype purity: 0 non-partner-endpoint routes** (Minor's `G1`). Carry it into the Grok seal prompt and `qa.expected_object_ids` as a numeric eval, not prose.

## Captive economics frame

- **Capture is high and bounded** (~0.85–0.90): guests at a partner property are a captive demand pool, not a contested mobility market. (Contrast: super-app partners sit in the **contested** capture band, never captive.)
- **TAM is anchored on guest throughput** (keys × occupancy × trips/stay × fare), **not** city-mobility TAM.
- **Headroom = WIDTH**, never capture-share. Growth comes from more keys / more openings / more clusters / pipeline properties — never from modeling a rising share of an open market.
- **Inherits LB-254** (no 9× ladder inflation). The growth case scales width, not capture multiples.

## Deck-structure deltas (vs. standard 11-slide sequence)

Keep the slide skeleton and count; override the **content frame** of these slides. The KPI lines, route lists, and economics still rebuild from the sidecar via the deterministic edit plan — only the framing changes:

| Slide | Base playbook | Operator-developer override |
|---|---|---|
| 2 — Why this partner | distribution, demand, strategic fit | **Why a hotel operator now**: captive guest throughput + brand-trust transfer; keep slide 2 **KPI-free** (KPIs live on slide 3) |
| 3 — Market-overview KPIs | market size, fleet/route counts, demand/fare anchors | **Portfolio KPIs**: keys · openings/pipeline · clusters (WIDTH metrics), plus throughput/fare anchors from the economics sidecar |
| 4 — Launch-market candidates | exact-bound markets first | **Grounded clusters first** (economics-ready), candidate clusters second |
| 5 — Use cases/journeys | airport/commute/premium/logistics | **The 3 captive route classes only** (gateway→property, property↔property, property→excursion); no commute/open-mobility use cases |
| 7 — Economics | aggregate/growth/sheet/sidecar | **Captive/throughput-bounded** model: capture ~0.85–0.90, headroom = WIDTH, LB-254 inherited; 6-line OPEX rule unchanged |
| 9 — Rollout (prove→scale→mature) | phase economics | **Grounded-first cluster ramp**: economics-ready flagships → grounding-pending flagships → Tier 2/3 clusters as width |

Slides 1, 6, 8, 10, 11 keep their base meaning. Slide 6 still scopes N30/N35 for ≤70nm and Quanta-LR only for range-gated legs.

## Narrative / USP framing

Lead with the canonical **Three C's** (hospitality standard — do NOT rename or substitute): **Cost · Convenience · Comfort** —
- **Cost**: a margin line the operator owns — branded transfers captured in-house instead of leaking to diesel launches and outsourced boats.
- **Convenience**: one operator graph end-to-end (gateway → property → excursion), brand-consistent and on-demand.
- **Comfort**: premium, quiet, wake-free arrival as a brand-grade guest experience — zero-emission and aligned to resort ESG positioning.

> **Naming lock (Jaideep 2026-06-24):** the hospitality value-prop framework is the **Three C's = Cost · Convenience · Comfort**. The earlier "Captive · Calm · Clean · Continuity" variant was reverted and must not be reintroduced. (The separate *captive-economics* frame — capture ~0.85–0.90 — is unrelated and stays.)

Back each prop with a **source-backed proof strip**; slide-level claims need source paths and `null` beats confidently-wrong.

## Validation-gate additions (on top of the base QA gates)

Before reporting deck-prep complete for an operator-developer partner, also confirm:
- the seal prompt + edit plan carry the **archetype-purity numeric gate** (0 non-partner-endpoint routes);
- slide-3 KPIs are **WIDTH metrics** (keys/openings/clusters) resolved from the sidecar — not city-mobility TAM;
- the economics frame is **captive (0.85–0.90) + LB-254**, with headroom expressed as width;
- single-property markets with no corridor partner are **logged as explicit holds**, never seeded.
