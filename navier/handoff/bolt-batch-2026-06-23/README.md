# Bolt sub-proposal batch — seal handoff (2026-06-23)

Tasklet-owned **input** package for five Bolt sub-proposal changes requested by Jaideep. Grok derives
partner-view scope (ID-match), seals geometry, and runs the economics cascade. GitHub `main` stays SoT.

## The five changes
| Sub-proposal | Action | Anchors |
|---|---|---|
| `bolt-ksa-commercial` | **Rescope** → Jeddah + Eastern Province; drop NEOM/AMAALA/Red Sea Global | jeddah-ksa, dammam-khobar-ksa, manama-bahrain |
| `bolt-estonia` | **Narrative only** → Tallinn-HQ Nordic-Baltic triangle (already existed) | tallinn-estonia, helsinki-finland, stockholm-sweden |
| `bolt-thailand` | **Net-new** → Phuket / Phang Nga (Andaman island-hopping) | phuket-phang-nga-thailand |
| `bolt-nigeria` | **Net-new** → Lagos Lagoon (urban water-commuter) | lagos-nigeria |
| `bolt-south-africa` | **Net-new** → Cape Town (Table Bay / False Bay heritage + leisure) | cape-town-south-africa |

## Africa decision (Jaideep asked to pick 2 of Lagos / Kenya / South Africa)
- **Lagos — IN (tier A):** the single largest urban water-commuter case on earth; LASWA regulator already in
  place; Bolt is Nigeria's #1 ride-hail brand (>60% share). Strongest of the three.
- **Cape Town — IN (tier B):** premium tourism + high-volume Robben Island heritage ferry; Bolt established in SA.
- **Kenya — DROPPED:** no Atlas brief, Likoni crossing too short to foil, Lamu remote/thin. Per "poor proposals
  are worse than none."

## Contents
| Path | What |
|---|---|
| `GROK-SEAL-PROMPT.md` | Mandate, per-proposal scope, acceptance gate |
| `inputs/bolt-subproposals-delta.json` | The 5 affected sub-proposals (full objects) |
| `inputs/bolt-scope-map.json` | Per-proposal action + anchor_cities (+ removed giga nodes) for scope derivation |

## Notes
- Tallinn already existed as `bolt-estonia` with the Tallinn→Helsinki→Stockholm triangle — strengthened, not
  duplicated.
- All anchors are existing Atlas nodes (no new geography to mint). Tasklet changed narrative + node-ids + scope
  only; the economics cascade is Grok's to re-run against the new gold.
