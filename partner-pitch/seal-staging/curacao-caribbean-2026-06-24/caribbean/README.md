# Caribbean × Navier — generic ABC network source-asset package (Tasklet-authored)

**Status:** Tasklet source assets COMPLETE. Geometry `PENDING_SEAL` (Grok). Economics `PENDING_CASCADE` (Grok, post-seal). Narrative authored; growth ladder **not** hand-typed.

Renamed from *"Caribbean Mobility Partner × Navier"* → **"Caribbean × Navier"** (Jaideep 24-Jun): a **generic Caribbean Navier network proposal**, NOT an aggregator-led pitch. Structural twin of `french-polynesia.json`.

## What's here (Tasklet's lane)
| File | What it is | Splices into |
|---|---|---|
| `caribbean-corridors.json` | ABC-trio economic corridors (7 grounded + 1 seasonal amber + 2 roadmap), cost inputs + modeled fares, all `route_id:null / PENDING_SEAL` | `finance/model/corridors.json` (market `caribbean`) |
| `caribbean-demand-anchors.json` | ABC 2024 volumes (cruise/stayover/dive/inter-island air), capture 0.55 | model demand inputs |
| `caribbean-country-reference-rows.json` | 3 L3-COUNTRY rows (Aruba/Curaçao/Bonaire) | `finance/model/country-reference.json` |
| `caribbean-boarding-point-spec.json` | 12 BPs across 3 island nodes + corridor split | Atlas seal (Grok) |
| `caribbean.json` | Proposal narrative — FP twin; `_economics_status: pending`; `growth_case` = cascade-input stub | `partner-pitch/partners/` |

## Locked guardrails (Jaideep 24-Jun — ABC-BUILD-PLAN.md)
- **CAPEX = $900K commercial tier** (generic network; NOT $1M hospitality, NOT $600K OCT). Stays **distinct** from Ocean Whisperer's $1M.
- **Capture ~55% (FP-style)** BUT **rising ladder, NOT FP's flat treatment** — ABC has genuine network width (3 islands, multi-corridor) → SOM floor < SOM network < SAM < TAM.
- **Generic network framing** — not aggregator-led; mirror FP.
- **Split the lumped `aruba-curacao-bonaire` node** into 3 island nodes (`aruba-aruba` / `curacao-curacao` / `bonaire-bonaire`) and **reconcile/retire** the old `caribbean-mobility` stub — shared network, scoped view, never copied.
- **Curaçao is a SHARED node** — sealed ONCE; both Caribbean × Navier (broad) and Ocean Whisperer (captive-luxury scoped view) reference the same geometry.
- Grounded spine = Curaçao↔Bonaire + intra-island; **Klein Curaçao = seasonal amber**; **Aruba legs = Quanta-LR roadmap amber**, never grounded on a 70nm boat.
- Below the hurricane belt = **year-round operability** (the headline thesis).

## Grok dependency order
1. **Grok seals geometry** — split node → 3 island nodes; ID-match/mint 12 BPs; build BP↔BP routes with water gates; bind `route_id`s; 0 silent drops; Aruba legs render amber-dashed roadmap; reconcile/retire the `caribbean-mobility` stub.
2. **Tasklet cascades economics** on the sealed route_ids → rising growth ladder (capture 0.55, $900K) → sheet + tracker + `economics_url`.
3. **Grok builds the economics sidecar** against the new gold.

> Curaçao geometry is shared with Ocean Whisperer — seal once, scope both views.
