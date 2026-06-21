# Grok prompt — India Adani/Reliance financials and seal handoff

Date: 2026-06-21  
Owner split: **Tasklet is done with research. Grok owns financial model construction, TAM/growth_case, economics sidecar, sheet/master cascade, exact ID binding, geometry/seal and render QA.**

## Required inputs in this PR

- `partner-pitch/partners/adani-ports.json`
- `partner-pitch/partners/reliance-industries.json`
- `handoff/partner-map-model/india-adani-reliance-demand-fare-source-scaffold-2026-06-21.json`
- `handoff/partner-map-model/india-adani-reliance-validated-model-inputs-research-only-2026-06-21.json`
- `handoff/partner-map-model/india-adani-reliance-sealed-atlas-crosswalk-2026-06-21.json`
- `handoff/partner-map-model/GROK-INDIA-ADANI-RELIANCE-SEAL-PROMPT-2026-06-21.md`

## Non-negotiables

1. Do **not** ask Tasklet for more financial-model work. Tasklet's lane is research only and the research packet is complete.
2. Use only `admitted_model_inputs` / `inputs_by_market` as Tasklet-sourced facts.
3. Null beats confidently wrong.
4. If a model needs a missing value, either:
   - independently verify an official source, or
   - use a clearly labelled Grok/model assumption/template.
5. Do not attribute assumptions/templates to Tasklet research.
6. Andaman is route-candidate-only from Tasklet; no Andaman economics row from Tasklet facts unless the DSS PDF is independently retrieved.

## Admitted research summary

### Mumbai

- Source: M2M Ferries official website.
- Admit: Mumbai↔Mandwa route, passenger fare floor ₹400 onward, motorcycle ₹210, 4-wheeler ₹1,020, bicycle ₹110, bus ₹4,500; year-round Ro-Pax; vehicle-deck capacity fact.
- Null: passenger demand, average fare, seasonality, capture, vessel count.

### Kochi / Kerala Backwaters

- Source: Kochi Water Metro official website and schedule page.
- Admit: 75+ e-boats, 15 routes, 75+ km, daily ridership 5,873 on 2026-06-19, cumulative 7,070,083 passengers, terminal list.
- Null: official fare chart, route-level split, capture, vessel count.

### Goa

- Source: Government of Goa River Navigation Department Citizens' Charter.
- Admit: 21-route ferry network, 18–20 hour regular service, on-request service, foot/two/three-wheeler exemptions, vehicle/cargo toll baseline, ferry roster.
- Null: passenger demand, premium fare, route-level volumes, capture, vessel count.

### Andaman

- Source: official DSS passenger-fare PDF URL found but unreadable in Tasklet environment.
- Admit: route candidate only.
- Null: fare, demand, ops, vessel count.

### Kolkata / Hooghly waterfront

- Source: West Bengal Transport official ferry-route roster; PIB/GoI and World Bank West Bengal Inland Water Transport project documents; West Bengal Tourism river/cruise context.
- Admit: active official Hooghly route roster; $105M GoI/WB waterways project; around 30M project-area population; KMA daily passenger volume ~25M expected to reach 32M by 2025; 165 ferries / 57 KMA ferry points / more than 145M annual ferry passengers at KMA system level.
- Null: route-level demand, official tariff, premium fare, exact BP IDs, route IDs, distances and capture.
- Model warning: `145000000` is KMA ferry-system context only, not a route-level Navier demand input.

### Chennai / ECR / Cuddalore / Puducherry coast

- Source: Poompuhar Shipping Corporation official EOI; PIB Chennai cruise release; ET Infra water-metro feasibility report; Puducherry Port EOI context.
- Admit: PSC official EOI for ferry service and cruise tourism involving Cuddalore to Chennai and in/around Chennai; proposed locations include Chennai Port and Cuddalore Port; Chennai Port 2026 cruise context includes 3,600 passengers in one day, 21 announced voyages over three months, 4,103 sqm premium terminal and 800 passengers/hour flow.
- Null: ferry demand, ferry fare/tariff, official route-level volumes, final water-metro route approvals, exact BP IDs, route IDs, distances and capture.
- Model warning: cruise passenger event/terminal facts are premium infrastructure context only, not ferry TAM.

## Financial/model work requested from Grok

- Build/refresh partner economics for Adani and Reliance at Grab/Careem parity using the admitted research packet.
- Add complete `growth_case` blocks and economics provenance.
- Produce economics sidecar into the gold export/package.
- Update transparent sheet/master tracker only through the approved in-place path if real Sheet IDs exist.
- Run exact-bind/seal/render QA and commit results to this PR branch.

## Exact-binding rules still apply

- Use only exact Atlas IDs or mint via deterministic Grok lane.
- Existing display-ready India city IDs: `mumbai-india`, `goa-india`, `kerala-backwaters-india`, `andaman-india`.
- All unbound assets stay null until exact-bound/minted.
- Do not recreate existing `adani-ports` shell.
