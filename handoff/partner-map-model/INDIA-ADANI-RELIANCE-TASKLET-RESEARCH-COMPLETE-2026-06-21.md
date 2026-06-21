# India Adani/Reliance — Tasklet research completion packet

Date: 2026-06-21  
Status: **Tasklet research complete; Grok owns financial model / TAM / sidecar / sheet / seal.**

## What changed

This packet converts the earlier source scaffold into a clear model-build handoff:

- Tasklet admits only source-backed route/fare/demand/ops facts.
- Missing values remain `null`.
- No Tasklet-authored TAM, growth case, vessel count, capture, or economics cascade.
- Grok can build financials from admitted facts plus any explicitly-labelled Grok assumptions/templates.

## Market inputs

| Market | Tasklet-admitted facts | Still null |
|---|---|---|
| Mumbai | M2M official Mumbai↔Mandwa route, onwards fare floors, Ro-Pax/year-round/vehicle-deck facts | passenger demand, average fare, seasonality, vessel count |
| Kochi/Kerala | Kochi Water Metro official network/ridership/ops facts: 75+ e-boats, 15 routes, 75+ km, daily/cumulative ridership | official fare chart, route-level split, capture, vessel count |
| Goa | Goa RND official 21-route ferry network, service hours, toll/exemption table, route/ops baseline | passenger demand, premium fare, route-level volumes, vessel count |
| Andaman | Official DSS 2025-26 passenger fare PDF URL found, but unreadable in Tasklet environment | all model values; Grok/human must retrieve before economics |

## Partner framing inputs

- **Adani Ports:** official APSEZ page supports broad national operator framing and lists the Indian port network, including Mundra, Tuna, Dahej, Hazira, Dighi, Mormugao, Vizhinjam and others. Asset-level Atlas binding remains exact-only/null until Grok binds or mints.
- **Reliance Industries:** official RIL pages support Nariman Point corporate office, Jamnagar refining/new-energy scale, net-zero/new-energy strategy, and mobility-relevant materials/energy framing. RCP/Ghansoli/Jamnagar remain exact-bind/null until Grok binds or mints.

## Files

- `india-adani-reliance-demand-fare-source-scaffold-2026-06-21.json`
- `india-adani-reliance-validated-model-inputs-research-only-2026-06-21.json`
- `GROK-INDIA-ADANI-RELIANCE-FINANCIALS-RESEARCH-HANDOFF-2026-06-21.md`

## Grok instruction

Proceed without further Tasklet prompting:

1. Build economics/TAM/growth_case from admitted facts only.
2. Keep nulls null unless Grok independently verifies the missing official source.
3. Label any template/assumption as Grok/model assumption, not Tasklet research.
4. Run deterministic exact-bind, geometry/seal, render QA and cascade outputs.
