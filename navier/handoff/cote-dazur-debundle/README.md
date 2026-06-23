# Côte d'Azur de-bundle — seal handoff (2026-06-23)

Tasklet-owned input package. **GitHub `main` is source of truth; this is an input for Grok's seal.**

## Why
Côte d'Azur was a single P0 cluster "stub" while Monaco was already de-bundled into its own rich node —
inconsistent, and under-built for a premium market. Jaideep approved de-bundling **all four** towns and
folding Monaco into the cluster, then representing the markets in the Bolt sub-proposal.

## Contents
| Path | What | Grok does with it |
|---|---|---|
| `GROK-SEAL-PROMPT.md` | The de-bundle seal mandate + acceptance gates | Executes it |
| `node-map.json` | Deterministic node mint list + POI re-key label→node map + Bolt scope | Re-key POIs, derive scope_city_ids |
| `briefs/nice-france.md` | Gateway node (Nice airport, year-round corporate base) | Authoritative node def |
| `briefs/cannes-france.md` | Event-surge node (Film/Yachting Festival, Lérins) | Authoritative node def |
| `briefs/antibes-france.md` | Superyacht-capital node (Port Vauban) | Authoritative node def |
| `briefs/saint-tropez-france.md` | Seasonal-peak node (road-bypass, regatta) | Authoritative node def |
| `briefs/cote-dazur-france.md` | Reworked **cluster parent** (5-node family incl. Monaco) | Cluster def |
| `bolt-france-riviera.subproposal.json` | Updated Bolt sub-proposal (anchor_cities, journeys, phases, narrative + St-Tropez) | Reseal Bolt view; re-run cascade |

## Sources locked (exactness over coverage)
- Nice Côte d'Azur Airport — France's 3rd-busiest; **~14.19M pax 2023**, ~15.23M 2025 (airport/Wikipedia).
- Port Vauban, Antibes — **Europe's largest yacht harbour, ~1,500+ berths**; Quai des Milliardaires **~18–19 superyacht berths up to ~160 m**, IYCA.
- Cannes Yachting Festival — **Europe's top in-water boat show, 700+ boats / ~680 exhibitors**; Vieux Port + Port Canto.
- Les Voiles de Saint-Tropez — late-Sept/early-Oct classic regatta, ~300 yachts; canonical summer road gridlock.

## Out of scope here
- Boarding-point binary splits: re-key existing sealed POIs (deterministic, Grok). No new BP JSON minted.
- Economics cascade: Grok-owned model re-run after seal (boats/capture unchanged pending it).
