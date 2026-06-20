# India partner derivative — Grok-ready packet draft (2026-06-20)

Status: **draft only**. Do not execute until Noon seal/render output is reviewed and India Atlas alias/crosswalk scope is confirmed.

## Source artifacts now banked on PR #58

- `handoff/partner-map-model/INDIA-MARKET-EVIDENCE-BANK-2026-06-20.json`
- `handoff/partner-map-model/INDIA-PARTNER-NARRATIVE-DRAFTS-2026-06-20.md`
- `handoff/partner-map-model/UBER-INDIA-CITY-EVIDENCE-EXTRACT-2026-06-20.json`
- `handoff/partner-map-model/INDIA-MARKET-SUBPROPOSAL-BLOCKS-2026-06-20.md`
- `handoff/partner-map-model/INDIA-DEMAND-ANCHOR-QUEUE-2026-06-20.json`
- `handoff/partner-map-model/ADANI-RELIANCE-EXACT-BIND-QUEUE-2026-06-20.json`
- `handoff/partner-map-model/INDIA-PARTNER-ASSEMBLY-SPECS-2026-06-20.json`

## Intended deterministic outputs

1. `partner-pitch/RAPIDO-INDIA-ANCHOR-CITY-CROSSWALK.json`
2. `partner-pitch/OLA-INDIA-ANCHOR-CITY-CROSSWALK.json`
3. `partner-pitch/UBER-INDIA-DERIVATIVE-ANCHOR-CITY-CROSSWALK.json`
4. Draft partner JSONs only if Atlas city IDs/market hierarchy resolve:
   - `rapido-india` draft
   - `ola-india` draft
   - `uber-india-derivative` draft
5. Render QA ledgers per draft.

## Scope gates

- Start with Goa, Mumbai/Navi Mumbai, Kerala/Kochi, and Kolkata-Haldia.
- Chennai/Tamil Nadu can be brief-only / scale candidate unless terminal/city IDs are clean.
- Andaman is marine-demand supported but platform-local evidence pending; keep conservative.
- Gujarat and Vizag remain exact-bind backlog unless Atlas matches exist.
- Adani/Reliance are excluded from footprint and economics.

## Hard prohibitions

- No invented route IDs.
- No invented boarding points.
- No destructive edits to global Uber.
- No non-marine footprint card grid.
- No economics cascade until route seal + render QA pass.
- Null beats confidently wrong.

## Assembly notes

- Use `coverage_note` prose for broad India reach.
- Display only markets that inherit from existing Atlas hierarchy/geometry.
- For Uber derivative, only exact official city rows may become city-supported candidates; state/country rows alone do not create new geography.
- Rapido/Ola remain country-supported unless local service evidence is later sourced.
