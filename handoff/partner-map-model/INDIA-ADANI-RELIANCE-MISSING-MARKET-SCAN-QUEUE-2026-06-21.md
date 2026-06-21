# India Adani/Reliance — missing market scan queue

Date: 2026-06-21  
Status: **Tasklet research lane reopened for broader India market scan.**

## Correction

The prior Tasklet note saying the Adani/Reliance research lane was complete was too narrow. It completed only the four **existing Atlas display-ready India markets** in the current sealed crosswalk:

- Mumbai / Konkan
- Goa
- Kerala / Kochi backwaters
- Andaman & Nicobar

That is not the same as completing the planned broad India scan.

## Why only four markets landed

The PR #61 handoff constrained display scope to existing sealed Atlas India city IDs and then source-hardened only those four. This followed the exactness rule, but it incorrectly collapsed the broader scan backlog into `roll_up_markets` / candidate-only notes instead of producing a separate market scan queue for Grok and Tasklet.

## Markets that still need broad-footprint-first scan

Priority A — named by plan / user:

- Kolkata / Hooghly river / Sundarbans access
- Chennai / Ennore / ECR / Mahabalipuram / Puducherry coast

Priority B — strongly implied by Adani/Reliance assets and India coastal footprint:

- Gujarat port spine: Mundra, Kandla/Tuna, Dahej, Hazira, Surat/Bharuch
- Dighi / Raigad / Agardanda / Konkan industrial-coast spine
- Vizhinjam / Trivandrum passenger context beyond Kerala backwaters
- Visakhapatnam / Kakinada / KG-D6/Gadimoga east-coast context
- Odisha / Dhamra / Bhubaneswar-Puri-Chilika context
- Lakshadweep access from Kochi/Vizhinjam

## Scan rule

For each candidate market, Tasklet should produce only research/rationale inputs:

- official route / ferry / waterway / port / tourism source if available
- official or high-confidence demand proxy if available
- official fare/tariff if available
- partner relevance to Adani/Reliance
- Atlas status: existing ID / exact-bind candidate / mint required / hold
- unsupported economics fields stay `null`

Grok still owns financials, model building, sealing, render QA, sheets and master cascade.

## Immediate next step

Run a bite-sized scan for Kolkata and Chennai first, then append Gujarat/Dighi/east-coast markets as additive scan batches.
