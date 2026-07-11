# Post-#224 Swing / DiDi release verification

**As of:** 2026-07-11 04:38 UTC  
**Scope:** source → model → live workbook → live Slides → deck record

## Decision

- **DiDi:** economics parity **verified**. Release remains held until PR #226 merges and the post-merge country/demand gates are replayed. No live-slide number correction is required.
- **Swing:** **release held**. The country correction reached the model and workbook, but the live deck did not regenerate. The independent engines also retain a $3 SOM-floor delta that should close to zero.

## DiDi verification

- Model / proposal: **$38,163,982** modeled transport revenue; **$386,158,495** current passenger-spend pool.
- Live workbook: exact match; four economics holds are visible (Costa Rica ×2, Argentina ×2).
- Live slide 9: rounded display matches the workbook — **$38.2M**, **$386.2M**, **$3.41B**, **$10.22B**, **$459.8M** — and links to the registered DiDi workbook.
- Live inventory: 12 slides at the required 9144000 × 5143500 EMU.
- Gates replayed on the controlled source: country-reference PASS (12 active, 4 held), partner copy PASS, geometry inheritance PASS, finance-spine inheritance PASS.
- Remaining hold: PR #226 corrects Argentina totals from production-eligible wording to benchmark-only and nulls unsupported annual one-way passenger fields. It does not change current totals because those corridors are already excluded.

## Swing verification

- Source aggregate: **$10,453,754** modeled transport revenue; **$104,537,675** current passenger-spend pool.
- Live workbook: **$10,453,757** modeled transport revenue; **$104,537,675** pool, explicitly using South Korea costs. The $3 floor delta is small but violates the zero-difference parity gate.
- Live slide 11: rounded ladder values remain source-consistent (**$51M / $231M / $922M / $2.77B / $124M**).
- Live slides 8–10 fail release parity. The current South Korea-costed midpoint model gives:
  - Jeju → Seogwipo Jungmun: **$87,754 revenue / $232,451 OPEX / −$144,697 EBITDA**.
  - Busan → Busan/Geoje Cluster: **$211,622 revenue / $230,800 OPEX / −$19,178 EBITDA**.
  - Incheon Coastal Passenger Terminal → Muuido Island Ferry Berth: **$68,957 revenue / $233,483 OPEX / −$164,526 EBITDA**.
- Live deck currently claims all three are profitable and uses old cost/fare/distance values. Those claims are unsupported after the country correction.
- Slides 8–11 link to workbook `1v0ywh…`, not registered Swing workbook `1PxUt…`.
- Slides 8–10 fail the six-line OPEX presentation rule by combining marina with charging and maintenance with insurance.

## Required next action

Reconcile the $3 model/workbook delta, regenerate Swing slides 8–10 deterministically from `finance/recal/agg-swing.json`, preserve slide 11’s current rounded ladder unless the source changes, replace all stale model links, replay copy/visual QA, then re-pull the live inventory and synchronize `deck.config.json` plus `slide-manifest.json`. Exact inputs are in `SWING-POST-223-DECK-REGEN-BRIEF.json`.
