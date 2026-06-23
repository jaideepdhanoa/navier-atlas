# Bolt East Africa coastal cluster — research + seal handoff (2026-06-23)

Net-new coastal cluster for Bolt: **Kenya coast + Tanzania mainland + Zanzibar/Pemba/Mafia archipelago**.
Follow-on to PR #83. Reusable for Uber / Yango / East-Africa hospitality.

**Status:** research-complete / seal-needed (geometry) + cascade-needed (economics). Nothing here is a
final/sealed number; external copy stays a draft until human review.

## Contents
| Path | What | Owner / next |
|---|---|---|
| `research/bolt-east-africa-coverage-research.json` | Source-led footprint, evidence tiers, market anchors | Tasklet (done) |
| `inputs/candidate-boarding-points.json` | 21 candidate BPs + gazetteer hints (coords null by design) | Grok geocode+seal |
| `inputs/candidate-signature-corridors.json` | 11 candidate corridors + range-gate + demand/fare anchors | Grok seal geometry |
| `inputs/country-reference-additions-east-africa.json` | Kenya + Tanzania opex/grid/crew/marina/CAPEX rows | Tasklet finance confirm → cascade |
| `BOLT-EAST-AFRICA-SUBPROPOSAL-NARRATIVE.md` | Sub-proposal narrative (DRAFT) | Human review |
| `GROK-EAST-AFRICA-SEAL-HANDOFF.md` | Grok seal instructions | Grok |

## Headline findings
- Bolt is the **#1 rides player in Tanzania** (+68% YoY, 8 cities, 30k+ drivers) and **licensed in
  Zanzibar** (Aug/Sep 2025); live on the **Kenyan coast** (Mombasa, Diani, southern Kilifi).
- **Dar ↔ Stone Town** (~41 nm) and **Mombasa ↔ Diani** (~16 nm) are the two marquee N30 legs.
- **Zanzibar 917k arrivals in 2025** (+24%); Dar–Zanzibar ferry runs 4 slots/way/day at ~$45 foreign.
- Kenya grid is **~90%+ renewable** → marquee zero-emission story on the Kenya legs.

## Two-worlds reminder
Geometry seals first (Grok), economics cascade second (Tasklet, after seal). Don't generate economics from
the candidate fare anchors — they're cascade inputs, not sealed numbers.
