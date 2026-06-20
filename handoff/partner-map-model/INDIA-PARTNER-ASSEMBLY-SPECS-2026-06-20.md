# India partner assembly specs — 2026-06-20

Status: **ready for deterministic assembly after Atlas seal/crosswalk**.

## Rapido India

Use Rapido as the high-frequency first/last-mile layer. Evidence is country-supported unless local service rows are sourced. Lead with Goa, Mumbai/Navi Mumbai and Kerala/Kochi. Keep Andaman and expansion markets conservative.

## Ola India

Use Ola as the national airport/hotel/outstation mobility layer. Lead with Goa airport/resort packaging, Mumbai land+water transfers and Kochi terminal/backwater premium routes. Chennai and Kolkata-Haldia are scale candidates after exact terminal cleanup.

## Uber India derivative

Create a derivative/draft; do **not** replace global Uber. Use the official Uber India city roster extract. City-supported candidates still need Atlas alias review and render-safe city IDs.

## Exclusions

Adani and Reliance stay overlay-only. Gujarat, Vizag and some Tamil Nadu rows remain brief-only until exact route/terminal support is sealed.

## Next deterministic packet requirements

1. Build partner JSON drafts for `rapido-india`, `ola-india`, and `uber-india-derivative`.
2. Carry `route_id: null` until sealed.
3. Attach `coverage_note` prose for unsupported broader reach.
4. No non-marine footprint grid.
5. Keep economics pending until model/sheet cascade.
